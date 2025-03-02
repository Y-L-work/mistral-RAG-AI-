# mistral-RAG: 自動化 AI 檢索與對話系統

side project

## 📌 專案簡介

mistral-RAG 是一款結合 **大型語言模型 Mistral-7B-Instruct GPTQ**、**Retrieval-Augmented Generation (RAG)** 技術的 AI 聊天機器人，
具備 **多輪對話記憶**、**查詢重寫 (Query Rewriting)**、**網頁爬取 (Web Scraping)**、
**向量檢索 (Vector Retrieval)**，透過 **Mistral AI** 生成高品質回應。

🚀 **主要特色：**

- **檢索增強生成 (RAG)**：結合 FAISS 向量檢索與 Mistral AI 提供準確回應。
- **查詢重寫 (Query Rewriting)**：優化用戶輸入，使檢索結果更精準。
- **多輪對話記憶 (Conversational Memory)**：能夠記住對話歷史。
- **網頁爬取 (Web Scraping)**：透過 **BeautifulSoup + Requests** 自動擷取最新資訊。
- **免費 & 本地部署**：使用 **Mistral-7B-Instruct GPTQ** 免費模型，適合本地運行，無需額外 API 費用。

📌 **目前進度：**
✅ Flask API 已成功運行
✅ FAISS 向量檢索已部署
✅ Mistral AI 生成回應正常運行
✅ Docker 環境準備中
⏸ n8n 整合暫時停止，未來再優化

---

## **🛠️ 技術架構**

🔹 **核心技術棧：**

- **LLM**：Mistral-7B-Instruct GPTQ (本地端部署)
- **向量檢索**：FAISS + Sentence Transformers (all-MiniLM-L6-v2)
- **API 框架**：Flask
- **網頁爬取**：BeautifulSoup + Requests
- **儲存**：SQLite / JSON-based Memory Buffer

---

## **📂 專案結構**

```plaintext
mistral-RAG/
├── data/                # 儲存處理過的文本與嵌入
│    ├── sources/        # 原始爬取的文本
├── models/              # Hugging Face 量化模型
├── src/                 # 核心程式碼
│    ├── retriever.py    # 向量檢索 (FAISS)
│    ├── generator.py    # 生成 AI 回應 (Mistral AI)
│    ├── scraper.py      # 網頁爬取 (BeautifulSoup)
│    ├── config.py       # 設定檔 (API Keys、儲存路徑)
├── web/                 # API 伺服器 (Flask)
│    ├── app.py          # Web API 入口點
├── docker/              # Docker 設定
│    ├── Dockerfile      # 容器化設定
│    ├── docker-compose.yml # 一鍵啟動所有服務
├── requirements.txt      # 依賴套件
└── .env                 # API Key 設定 (Mistral, Flask Security)
```

---

## **🚀 安裝與執行**

### **1️⃣ 安裝環境**
```bash
pip install -r requirements.txt
```

### **2️⃣ 設定環境變數**
建立 `.env` 文件，填入 API Key：
```ini
MISTRAL_API_KEY=你的_API_Key
FLASK_API_KEY=你的安全金鑰
```

### **3️⃣ 啟動 Flask API**
```bash
python web/app.py
```
預設監聽 **[http://localhost:8001/](http://localhost:8001)**

---

## **📌 Docker 部署**

### **1️⃣ 建立 Docker 環境**
```bash
docker-compose up --build
```

### **2️⃣ 透過 Docker 運行 Flask API**
```bash
docker run -p 8001:8001 mistral-rag-api
```

📌 **面試官只需執行 `docker-compose up` 即可快速測試專案！**

---

## **📌 API 使用方式**

### **🔹 查詢 AI 回應**
```bash
curl -X POST "http://localhost:8001/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "請介紹 n8n 是什麼？"}'
```

#### **💡 成功回應：**
```json
{
  "answer": "n8n 是一款開源自動化工具，可視化構建數據流。"
}
```

---

## **📌 未來發展**
✨ **與 n8n 整合**（目前暫停，未來再優化）
✨ **支援 Line Bot / Discord Bot**
✨ **強化檢索技術（Hybrid Search: FAISS + BM25）**

📌 **目前專案暫時停止，未來有空時再進行優化！**

