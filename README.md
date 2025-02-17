
# mistral-RAG: 自動化 AI 檢索與對話系統
side project
&#x20; &#x20;

## 📌 專案簡介

mistral-RAG 是一款結合 Retrieval-Augmented Generation (RAG) 技術的 AI 聊天機器人，
具備 **多輪對話記憶**、**查詢重寫 (Query Rewriting)**、**網頁爬取 (Web Scraping)**、
**向量檢索 (Vector Retrieval)**，透過 **Mistral AI** 生成高品質回應。

本專案整合 **n8n AI agent**，查詢與知識庫維護能夠自動化，適合用於 **AI 助理、FAQ 系統、自動客服** 情境。

🚀 **主要特色：**

-  **檢索增強生成 (RAG)**：結合 FAISS 向量檢索與 Mistral AI 提供準確回應。
-  **查詢重寫 (Query Rewriting)**：優化用戶輸入，使檢索結果更精準。
-  **多輪對話記憶 (Conversational Memory)**：能夠記住對話歷史。
-  **網頁爬取 (Web Scraping)**：透過 **BeautifulSoup + Requests** 自動擷取最新資訊。
-  **n8n 自動化整合**：透過 **Webhook** 讓查詢和知識庫更新全自動。
-  **免費 & 本地部署**：使用 Hugging Face 免費模型，適合本地運行，無需額外 API 費用。

---

## **🛠️ 技術架構**

```mermaid
graph TD;
    A[User Query] -->|Rewrite| B[Query Rewriting];
    B -->|Web Scraping| C[Scraper];
    C -->|Chunking| D[Text Splitter];
    D -->|Embedding| E[Vector Store (FAISS)];
    A -->|Embedding| E;
    E -->|Retrieve Top-K| F[Retriever];
    F -->|Format Prompt| G[Prompt Builder];
    G -->|Generate Answer| H[Mistral AI];
    H -->|Return Response| I[Chatbot];
    I -->|Send to User| J[User];
```

🔹 **核心技術棧：**

- **LLM**：Mistral-7B-Instruct GPTQ (本地端部署)
- **向量檢索**：FAISS + Sentence Transformers (all-MiniLM-L6-v2)
- **自動化整合**：n8n Webhook
- **網頁爬取**：BeautifulSoup + Requests
- **API 框架**：Flask
- **儲存**：SQLite / JSON-based Memory Buffer

---

## **📂 專案結構**

```plaintext
chatbot_project/
├── data/                # 儲存處理過的文本與嵌入
│    ├── cache/          # 快取文件處理
│    ├── sources/        # 原始爬取的文本
├── models/              # Hugging Face 量化模型 
├── src/                 # 核心程式碼
│    ├── chatbot.py      # Chatbot 主程式 (整合檢索 + 生成)
│    ├── retriever.py    # 向量檢索 (FAISS)
│    ├── generator.py    # 生成 AI 回應 (Mistral AI)
│    ├── scraper.py      # 網頁爬取 (BeautifulSoup)
│    ├── utils.py        # 通用工具函式
│    ├── config.py       # 設定檔 (API Keys、儲存路徑)
│    ├── main.py         # CLI 介面
├── web/                 # API 伺服器 (Flask)
│    ├── app.py          # Web API 入口點
├── n8n/                 # n8n 自動化設定
├── requirements.txt      # 依賴套件
└── .env                 # API Key 設定 (Mistral, Flask Security)
```

---

## **🚀 安裝與執行**

### **1️⃣ 環境準備**

```bash
# 安裝 Python 依賴
pip install -r requirements.txt
```

### **2️⃣ 設定環境變數**

建立 `.env` 文件，填入 Mistral API Key：

```ini
MISTRAL_API_KEY=你的_API_Key
FLASK_API_KEY=你的安全金鑰
```

### **3️⃣ 啟動 Flask API**

```bash
python web/app.py
```

預設監聽 **[http://localhost:8000/](http://localhost:8000)**

### **4️⃣ 使用 n8n 觸發查詢**

1. **開啟 n8n**，新增 **Webhook 節點**
2. 設定 Webhook URL 為 `http://localhost:5678/webhook/chatbot-query`
3. 觸發 Webhook，ChatFlow-RAG 將自動查詢與回應

---

## **📌 API 使用方式**

### **🔹 查詢 ChatFlow-RAG**

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer 你的安全金鑰" \
     -d '{"query": "請介紹 n8n 是什麼？"}'
```

#### **💡 成功回應：**

```json
{
  "answer": "n8n 是一款開源自動化工具，可視化構建數據流。"
}
```

### **🔹 清除記憶**

```bash
curl -X POST "http://localhost:8000/clear_memory" \
     -H "Authorization: Bearer 你的安全金鑰"
```

---

## **📌 未來發展**

✨ **強化檢索技術**：Hybrid Search (FAISS + BM25)
✨ **支援多語言查詢**
✨ **與 Line Bot / Discord Bot 整合**

---

