# Dockerfile (flask_api)
FROM python:3.9-slim

WORKDIR /app

# 複製 requirements.txt 與 Linux-compatible 的輪子檔案（來源改為 packages_linux）
COPY requirements.txt /app/
COPY packages_linux /app/packages/

# 使用本地下載的 Linux .whl 安裝套件
RUN pip install --default-timeout=12000 --no-cache-dir --find-links=/app/packages -r requirements.txt

# 複製專案程式碼
COPY web/ /app/
COPY src/ /app/src/

# 建立 FAISS 向量庫目錄
RUN mkdir -p /faiss_index

EXPOSE 8000

CMD ["python", "web/serve.py"]

