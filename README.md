<h1 align="center"> mistral-RAG: 自動化 AI 檢索與對話系統</h1>

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

**mistral-RAG** 是一個免費、開源且可本地部署的 AI 對話系統，結合了最新的 **RAG 技術** 與 **Mistral-7B-Instruct GPTQ** 模型，提供高品質且精準的自動化回答系統。

---

##  功能特色

- 🔹 **檢索增強生成 (RAG)** — 提升答案準確性
- 🔹 **查詢重寫 (Query Rewriting)** — 自動調整、優化問題
- 🔹 **多輪對話記憶 (Conversational Memory)** — 記住並理解對話歷史
- 🔹 **網頁爬取 (Web Scraping)** — 即時獲取最新資訊
- 🔹 **免費 & 本地部署** — 無須付費 API，方便執行

---

## 🛠️ 技術架構

**主要技術與工具**

|  類別 | 🛠️ 工具 & 技術 |
|--------|----------------------|
| 🌐 **網頁爬取** | ![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4B8BBE?style=for-the-badge&logo=python&logoColor=white) ![Requests](https://img.shields.io/badge/Requests-CC0000?style=for-the-badge&logo=python&logoColor=white) |
| 🧠 **LLM** | ![Mistral-7B](https://img.shields.io/badge/Mistral_7B-Instruct-6A5ACD?style=for-the-badge&logo=ai) ![GPTQ](https://img.shields.io/badge/GPTQ-Quantized-FFA500?style=for-the-badge&logo=pytorch) |
| 📚 **向量檢索** | ![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD700?style=for-the-badge&logo=huggingface&logoColor=black) ![FAISS](https://img.shields.io/badge/FAISS-0078D7?style=for-the-badge&logo=vector&logoColor=white) |
| 💾 **儲存與記憶** | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white) ![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white) ![LangChain](https://img.shields.io/badge/LangChain-Memory-228B22?style=for-the-badge) |
| 🚢 **容器化部署** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![Docker Compose](https://img.shields.io/badge/Docker%20Compose-1488C6?style=for-the-badge&logo=docker) |
| ⚙️ **流程自動化** | ![n8n](https://img.shields.io/badge/n8n-A259FF?style=for-the-badge&logo=n8n&logoColor=white) *(團專已經做過了，有空補上)* |

---

## 📂 專案目錄

```plaintext
mistral-RAG/
├── data/                # 儲存處理過的文本與嵌入
│    ├── sources/        # 原始爬取文本
├── src/
│    ├── generator.py   # AI 回應生成 (Mistral AI)
│    ├── retriever.py   # 向量檢索 (FAISS)
│    ├── scraper.py     # 網頁爬取
│    ├── config.py      # 設定檔
├── web/
│    ├── app.py         # Flask API 入口點
│    ├── serve.py       # WSGI 伺服器
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```
---

##  快速開始

### 1️⃣ 安裝環境

```bash
pip install -r requirements.txt
```

### 2️⃣ 運行系統

```bash
python src/scraper.py          # 爬取資料
python src/retriever.py        # 建立 FAISS 索引
python web/app.py              # 啟動 Flask API
```

👉 API 運行於：[http://localhost:8001](http://localhost:8001)

---

## 🐳 Docker 部署

快速透過 Docker Compose 部署系統：

```bash
docker-compose up --build
```

---

##  API 使用範例 在PowerShell下執行

```bash
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/query" -ContentType "application/json" -Body '{"query": "什麼是 RAG 技術？"}'
```

**🔖 成功回應範例：**

```json
{
  "answer": "RAG (Retrieval-Augmented Generation) 是一種結合資訊檢索與生成模型的技術，用來提高回答的準確性和即時性。"
}
```

---

## 📊 GitHub 活動

![GitHub Activity](https://github-readme-activity-graph.vercel.app/graph?username=Y-L-work&theme=react-dark)

---

##  未來規劃

- 🔹 **查詢優化與路由**
- 🔹 **Line / Discord / Telegram 整合**
- 🔹 **強化檢索技術（Hybrid Search: FAISS + BM25）**
- ⏸️ **n8n 完整流程自動化（暫停中）**


<p align="center">
 喜歡本專案的話，記得給個 ⭐ 支持一下喔！
</p>

