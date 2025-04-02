import os
import json
import logging
from datetime import datetime
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config import NEWS_DATA_DIR, FAISS_INDEX_DIR, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP

# 設定 logging（日誌檔案將存放於容器內 /var/log/update_vector_store.log）
logging.basicConfig(
    level=logging.INFO,
    filename='/var/log/update_vector_store.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 定義 FAISS 索引及 corpus 檔案路徑
FAISS_INDEX_PATH = os.path.join(FAISS_INDEX_DIR, "faiss_index")
CORPUS_PATH = os.path.join(FAISS_INDEX_DIR, "faiss_corpus.json")

def load_news_data_for_rebuild():
    """
    讀取 NEWS_DATA_DIR 下所有 JSON 檔案，並回傳所有新聞內容（用於重建向量庫）。
    """
    all_texts = []
    try:
        for filename in os.listdir(NEWS_DATA_DIR):
            if filename.endswith('.json'):
                file_path = os.path.join(NEWS_DATA_DIR, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    news_data = json.load(f)
                    texts = [content for content in news_data.values() if content]
                    all_texts.extend(texts)
        logging.info(f"Loaded {len(all_texts)} texts from all news files for rebuild.")
    except Exception as e:
        logging.error(f"Error loading news data for rebuild: {e}")
    return all_texts

def load_latest_news_data():
    """
    讀取今日新聞資料 JSON 檔，並回傳新聞內容列表。
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(NEWS_DATA_DIR, f"news_{date_str}.json")
    texts = []
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                news_data = json.load(f)
                texts = [content for content in news_data.values() if content]
            logging.info(f"Loaded {len(texts)} texts from today's news file: {file_path}.")
        else:
            logging.warning(f"Today's news file not found: {file_path}.")
    except Exception as e:
        logging.error(f"Error loading today's news data: {e}")
    return texts

def build_faiss_index(embedding_dim):
    """
    建立一個新的 FAISS 索引。
    """
    index = faiss.IndexFlatL2(embedding_dim)
    return index

def update_faiss_index(texts, rebuild=False):
    """
    更新 FAISS 索引：
      - 若 rebuild 為 True 或索引檔不存在，則從頭建立新索引。
      - 否則將新的向量加入現有索引中。
    """
    if not texts:
        logging.warning("No texts provided for FAISS update.")
        return

    # 初始化文本切分器與向量化模型
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    embedder = SentenceTransformer(EMBEDDING_MODEL)

    # 將新聞內容切分成多個片段
    chunks = []
    for text in texts:
        chunks.extend(text_splitter.split_text(text))
    if not chunks:
        logging.warning("No chunks generated from texts.")
        return

    # 向量化文本片段
    try:
        embeddings = embedder.encode(chunks, show_progress_bar=True).astype("float32")
    except Exception as e:
        logging.error(f"Error during vectorization: {e}")
        return

    embedding_dim = embeddings.shape[1]

    # 根據 rebuild 參數決定是建立新索引或更新現有索引
    if rebuild or not os.path.exists(FAISS_INDEX_PATH):
        index = build_faiss_index(embedding_dim)
        logging.info("Building new FAISS index.")
    else:
        try:
            index = faiss.read_index(FAISS_INDEX_PATH)
            logging.info("Loaded existing FAISS index.")
        except Exception as e:
            logging.error(f"Error loading existing FAISS index: {e}")
            index = build_faiss_index(embedding_dim)
            logging.info("Building new FAISS index due to load failure.")

    # 新增向量至索引中
    try:
        index.add(embeddings)
        faiss.write_index(index, FAISS_INDEX_PATH)
        logging.info(f"FAISS index updated with {len(chunks)} chunks. Rebuild={rebuild}")
    except Exception as e:
        logging.error(f"Error updating FAISS index: {e}")

    # 儲存 corpus 到檔案
    try:
        with open(CORPUS_PATH, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
        logging.info(f"Corpus saved to {CORPUS_PATH}.")
    except Exception as e:
        logging.error(f"Error saving corpus: {e}")

def main():
    try:
        today = datetime.now().day
        # 每月第一天完全重建 FAISS 向量庫；否則只更新當日新聞
        if today == 1:
            logging.info("First day of the month detected. Rebuilding FAISS index from all news data.")
            texts = load_news_data_for_rebuild()
            update_faiss_index(texts, rebuild=True)
        else:
            logging.info("Updating FAISS index with today's news data.")
            texts = load_latest_news_data()
            update_faiss_index(texts, rebuild=False)
    except Exception as e:
        logging.error(f"Error in update_vector_store: {e}")

if __name__ == "__main__":
    main()
