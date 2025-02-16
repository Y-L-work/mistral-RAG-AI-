import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from .config import EMBEDDING_MODEL

class Retriever:
    def __init__(self):
        # 載入免費的嵌入模型 (例如 all‑MiniLM‑L6‑v2)
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)

    def vectorize_texts(self, texts):
        embeddings = self.embedder.encode(texts, show_progress_bar=True)
        return np.array(embeddings).astype("float32")

    def build_index(self, texts):
        embeddings = self.vectorize_texts(texts)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        return index, embeddings

    def search(self, index, embeddings, query, k=3):
        query_embedding = self.embedder.encode([query]).astype("float32")
        distances, indices = index.search(query_embedding, k)
        return distances, indices
