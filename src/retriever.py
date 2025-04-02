import faiss
import numpy as np
import os
import json
from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL

# Docker 內部向量庫存放位置
FAISS_INDEX_PATH = "/faiss_index/faiss_index"
CORPUS_PATH = "/faiss_index/faiss_corpus.json"

class Retriever:
    def __init__(self):
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        self.index = None  # 初始化時不載入索引
        self.corpus = None  # 用於存放文本片段

        # 嘗試載入 FAISS 索引
        if os.path.exists(FAISS_INDEX_PATH):
            try:
                self.index = faiss.read_index(FAISS_INDEX_PATH)
            except Exception as e:
                print(f"❌ 無法讀取 FAISS 索引: {e}")
                self.index = None

        # 嘗試載入 corpus（文本片段），若檔案存在
        if os.path.exists(CORPUS_PATH):
            try:
                with open(CORPUS_PATH, "r", encoding="utf-8") as f:
                    self.corpus = json.load(f)
            except Exception as e:
                print(f"❌ 無法讀取 FAISS corpus: {e}")
                self.corpus = None

    def vectorize_texts(self, texts):
        """將文本轉換為向量"""
        if not texts:
            return np.array([])
        embeddings = self.embedder.encode(texts, show_progress_bar=True)
        return np.array(embeddings).astype("float32")

    def build_index(self, texts):
        """建立 FAISS 向量庫並存儲到磁碟，同時保存文本片段"""
        if not texts:
            print("⚠️ build_index() 收到空文本，將返回空索引")
            self.index = faiss.IndexFlatL2(384)
            self.corpus = []
            return self.index, np.array([])

        embeddings = self.vectorize_texts(texts)
        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        self.corpus = texts

        # 存儲 FAISS 索引
        faiss.write_index(self.index, FAISS_INDEX_PATH)

        # 存儲 corpus 到磁碟
        try:
            with open(CORPUS_PATH, "w", encoding="utf-8") as f:
                json.dump(self.corpus, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving corpus: {e}")

        return self.index, embeddings

    def search(self, query, k=3):
        """在 FAISS 向量庫中檢索最相關的文本塊"""
        if self.index is None:
            print("⚠️ FAISS 索引尚未建立，返回空結果")
            return [], []
        query_embedding = self.embedder.encode([query]).astype("float32")
        distances, indices = self.index.search(query_embedding, k)
        # 除錯輸出：印出距離與索引
        print("檢索結果 - distances:", distances)
        print("檢索結果 - indices:", indices)
        if indices is None:
            return [], []
        return distances, indices
