import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL

# Docker 內部向量庫存放位置
FAISS_INDEX_PATH = "/faiss_index/faiss_index"

class Retriever:
    def __init__(self):
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        self.index = None  # 初始化時不載入索引

        # 嘗試載入 FAISS 向量庫
        if os.path.exists(FAISS_INDEX_PATH):
            try:
                self.index = faiss.read_index(FAISS_INDEX_PATH)
            except Exception as e:
                print(f"❌ 無法讀取 FAISS 索引: {e}")
                self.index = None

    def vectorize_texts(self, texts):
        """將文本轉換為向量"""
        if not texts:
            return np.array([])  # 避免錯誤返回空陣列
        embeddings = self.embedder.encode(texts, show_progress_bar=True)
        return np.array(embeddings).astype("float32")

    def build_index(self, texts):
        """建立 FAISS 向量庫並存儲到磁碟"""
        if not texts:
            print("⚠️ build_index() 收到空文本，將返回空索引")
            self.index = faiss.IndexFlatL2(384)  # 384 是 all-MiniLM-L6-v2 的嵌入維度
            return self.index, np.array([])

        embeddings = self.vectorize_texts(texts)
        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

        # 存儲 FAISS 索引
        faiss.write_index(self.index, FAISS_INDEX_PATH)
        return self.index, embeddings

    def search(self, query, k=3):
        """在 FAISS 向量庫中檢索最相關的文本塊"""
        if self.index is None:
            print("⚠️ FAISS 索引尚未建立，返回空結果")
            return [], []

        query_embedding = self.embedder.encode([query]).astype("float32")
        distances, indices = self.index.search(query_embedding, k)

        # 確保返回的 indices 不是 None
        if indices is None:
            return [], []
        return distances, indices
