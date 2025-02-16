from dotenv import load_dotenv
import os

# 載入 .env 文件中的環境變數
load_dotenv()

# 從環境變數中讀取 Mistral API 金鑰
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("請先在環境變數或 .env 中設定 MISTRAL_API_KEY")

# Mistral AI 模型名稱
MISTRAL_MODEL = "mistral-large-latest"

# 向量化相關設定：使用免費的 HuggingFace 嵌入模型（例如 all‑MiniLM‑L6‑v2）
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# 文本拆分設定
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# 向量索引存放目錄 (建議存放在 D 槽)
FAISS_INDEX_DIR = "D:/faiss_index"

# 資料來源與快取存放目錄
SOURCES_DIR = os.path.join(os.getcwd(), "data", "sources")
CACHE_DIR = os.path.join(os.getcwd(), "data", "cache")
