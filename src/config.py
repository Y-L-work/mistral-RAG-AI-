from dotenv import load_dotenv
import os

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("請先在環境變數或 .env 中設定 MISTRAL_API_KEY")

MISTRAL_MODEL = "mistral-large-latest"

# 若需要多語言效果，可考慮使用：
# EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

FAISS_INDEX_DIR = "/faiss_index"
NEWS_DATA_DIR = "/news_data"

SOURCES_DIR = os.path.join(os.getcwd(), "data", "sources")
CACHE_DIR = os.path.join(os.getcwd(), "data", "cache")
