<h1 align="center"> mistral-RAG: AI 新知聊天機器人</h1>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=mistral-RAG&fontSize=60&animation=fadeIn" alt="mistral-RAG Banner"/>
</p>

<p align="center">
<a href="https://github.com/Y-L-work/mistral-RAG-AI-/stargazers">
  <img src="https://img.shields.io/github/stars/Y-L-work/mistral-RAG-AI-?style=social" alt="Stars">
</a>
<a href="https://github.com/Y-L-work/mistral-RAG-AI-/network/members">
  <img src="https://img.shields.io/github/forks/Y-L-work/mistral-RAG-AI-?style=social" alt="Forks">
</a>
<a href="https://github.com/Y-L-work/mistral-RAG-AI-/issues">
  <img src="https://img.shields.io/github/issues/Y-L-work/mistral-RAG-AI-" alt="Issues">
</a>
<a href="https://github.com/Y-L-work/mistral-RAG-AI-/blob/main/LICENSE">
  <img src="https://img.shields.io/github/license/Y-L-work/mistral-RAG-AI-" alt="License">
</a>
</p>

---

## 📖 專案簡介

**mistral-RAG** 是一個免費、開源且本地可部署的 **AI 聊天機器人系統**，結合最新的 **RAG 技術** 與 **Mistral-7B-Instruct GPTQ 模型**，即時抓取並整理🔹最新的 AI **相關新聞與論文**🔹，提供高品質 AI 聊天機器人互動。

---

## 功能特色

- 🔹 **檢索增強生成 (RAG)** — 提升答案準確性
- 🔹 **每日自動爬取最新 AI 新聞與論文** — 即時獲取最新資訊（包含翻譯成繁體中文）
- 🔹 **智能向量索引更新（每月重建，每日追加）**
- 🔹 **查詢重寫 (Query Rewriting)** — 自動調整、優化問題
- 🔹 **多輪對話記憶 (Conversational Memory)** — 記住並理解對話歷史
- 🔹 **免費 & 本地部署 & Docker 容器化** — 無須付費 API，方便執行

---

## 🛠️ 技術架構

|  類別 |    工具 & 技術 |
|--------|----------------------|
|  🔹 **網頁爬取** | ![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4B8BBE?style=for-the-badge&logo=python&logoColor=white) ![Requests](https://img.shields.io/badge/Requests-CC0000?style=for-the-badge&logo=python&logoColor=white) |
|  🔹 **LLM** | ![Mistral-7B](https://img.shields.io/badge/Mistral_7B-Instruct-6A5ACD?style=for-the-badge&logo=ai) ![GPTQ](https://img.shields.io/badge/GPTQ-Quantized-FFA500?style=for-the-badge&logo=pytorch) |
|  🔹 **向量檢索** | ![sentence-transformers](https://img.shields.io/badge/sentence_transformers-FFD700?style=for-the-badge) ![FAISS](https://img.shields.io/badge/FAISS-0078D7?style=for-the-badge&logo=vector&logoColor=white) |
|  🔹 **儲存與記憶** | ![LangChain](https://img.shields.io/badge/LangChain-Memory-228B22?style=for-the-badge) |
|  🔹 **容器化部署** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![Docker Compose](https://img.shields.io/badge/Docker%20Compose-1488C6?style=for-the-badge&logo=docker) |
|  🔹 **流程自動化** | ![n8n](https://img.shields.io/badge/n8n-A259FF?style=for-the-badge&logo=n8n&logoColor=white) *(團專已經做過了，有空補上)* |

---

## 📂 專案目錄

```plaintext
mistral-RAG/
├── packages_linux/      # 為了減少 Docker 速度，下載到本地端，以提升速度
├── src/
│    ├── chatbot.py     # 定義 Chatbot 類，整合檢索、生成回答及對話記憶管理
│    ├── generator.py   # 定義 Generator 類，調用 Mistral API 生成回答
│    ├── retriever.py   # 定義 Retriever 類，建立及查詢 FAISS 向量庫
│    ├── scraper.py     # 網頁爬取輔助函式（例如 fetch_page、parse_text、clean_text）
│    ├── config.py      # 系統配置（目錄路徑、模型參數等）
│    ├── memory_manager.py # 封裝 LangChain ConversationBufferMemory，用來管理、記憶對話歷史
│    ├── update_vector_store.py # 用於更新 FAISS 向量庫的腳本，更新最新新聞資料
│    ├── Crawler_AI_news.py # 網路爬蟲腳本，用於爬取 AI 新聞和論文，保存原文與翻譯版本
│    ├── translator_util.py  # 翻譯工具函式，處理中英文之間的翻譯，解決 coroutine 問題
│    └── utils.py            # 通用工具函式（例如 JSON 讀寫、文字清理）
├── web/
│    ├── app.py         # Flask API 入口
│    ├── serve.py       # WSGI 伺服器
│    ├── chat.html      # 前端聊天介面
├── Dockerfile
├── Dockerfile.crawler
├── docker-compose.yaml
├── requirements.txt
└── .env
```

---

## 🚀 快速開始

### 1️⃣ 下載專案程式碼

```bash
gh repo clone Y-L-work/mistral-RAG-AI-
```

### 2️⃣ 安裝環境

```bash
pip install -r requirements.txt
```

### 3️⃣ 啟動系統

```bash
python src/scraper.py          # 爬取資料
python src/retriever.py        # 建立 FAISS 索引
python web/app.py              # 啟動 Flask API
```


---
## 🐳 Docker 部署

快速透過 Docker Compose 部署系統：

```bash
docker-compose up --build
```

## 🌐 網頁使用說明

- **開啟網頁聊天室:** [AI新聞 聊天機器人](https://funny-tidy-raven.ngrok-free.app/)
- **輸入你的問題**（例如：「最新的AI論文或AI新聞？」）
- **點擊送出**，稍待片刻即可獲得AI生成的回覆。

👉 網頁入口：[https://funny-tidy-raven.ngrok-free.app/](https://funny-tidy-raven.ngrok-free.app/)
- (本網頁是用docker上ngrok，是使用電腦本地端開的，電腦關閉時就無法使用網頁。沒有開放24小時，請在白天使用。)
---
## 📊 GitHub 活動

![GitHub Activity](https://github-readme-activity-graph.vercel.app/graph?username=Y-L-work&theme=react-dark)

---

## 🚧 未來規劃

- 🔹 **查詢路由與優化策略增強**
- 🔹 **進一步強化向量檢索技術 (Hybrid Search)**
- ⏸️ **n8n 完整流程自動化（暫停中）**

<p align="center">
 喜歡本專案的話，記得給個 ⭐ 支持一下喔！
</p>

