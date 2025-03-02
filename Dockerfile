# 使用 Python 3.9 Slim 作為基礎映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 和本地下載的套件到容器
COPY requirements.txt /app/
COPY packages /app/packages/

# 使用本地下載的套件安裝，而不是從網路下載
RUN pip install --default-timeout=12000 --no-cache-dir --find-links=/app/packages -r requirements.txt

# 複製應用程式代碼
COPY web/ /app/
COPY src/ /app/src/

# 設定環境變數
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=src.app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000
ENV PYTHONPATH=/app

# 確保 FAISS 向量庫目錄存在
RUN mkdir -p /faiss_index

# 開放 Flask 服務的 Port
EXPOSE 8000

# 使用 Python Module 執行 Flask，確保絕對導入生效
CMD ["python", "web/serve.py"]
