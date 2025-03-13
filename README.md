# mistral-RAG: 自動化 AI 檢索與對話系統

![GitHub Repo stars](https://img.shields.io/github/stars/Y-L-work/mistral-RAG-AI?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/Y-L-work/mistral-RAG-AI?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/Y-L-work/mistral-RAG-AI?color=blue&style=flat-square)

## 專案簡介

mistral-RAG 是一個以 Mistral AI 模型及檢索增強生成（RAG）技術開發的聊天機器人，能自動進行網頁資料抓取、問題優化處理及向量檢索，透過本地端運行 Mistral AI 模型提供精確且有來源依據的回答。

![專案架構圖](https://raw.githubusercontent.com/Y-L-work/mistral-RAG-AI/main/assets/project-architecture.png)

## 主要功能

- ![FAISS](https://img.shields.io/badge/vector%20search-FAISS-blue?style=for-the-badge)
- ![Mistral AI](https://img.shields.io/badge/model-Mistral--7B--GPTQ-yellow?style=for-the-badge)
- ![BeautifulSoup](https://img.shields.io/badge/web%20scraping-BeautifulSoup-green?style=for-the-badge)
- ![Flask](https://img.shields.io/badge/API-Flask-orange?style=for-the-badge)
- ![Local Deployment](https://img.shields.io/badge/deployment-local-lightgrey?style=for-the-badge)

## 技術架構

- **大型語言模型 (LLM)**：Mistral-7B-Instruct GPTQ (量化模型)
- **向量索引與檢索**：FAISS + HuggingFace Sentence Transformers
- **網頁爬取**：BeautifulSoup + Requests
- **API 服務**：Flask + Waitress
- **資料儲存**：SQLite / JSON-based Memory

![示範 GIF](https://raw.githubusercontent.com/Y-L-work/mistral-RAG-AI/main/assets/demo.gif)

## 專案結構

```
mistral-RAG/
├── data/                 # 處理後的文本與向量資料
│    └── sources/         # 原始抓取的網頁內容
├── models/               # Hugging Face 量化模型
├── src/                  # 核心功能模組
│    ├── scraper.py       # 網頁爬取
│    ├── retriever.py     # 向量索引與檢索
│    ├── generator.py     # 模型推理生成
│    └── config.py        # 專案設定
├── web/                  # Flask API
│    └── app.py           # API 主要程式
├── docker-compose.yml    # Docker Compose 配置
├── Dockerfile            # Docker 環境設定
├── requirements.txt      # Python 依賴套件
└── .env                  # API 金鑰設定
```

## 安裝與執行

1. 安裝套件

```bash
pip install -r requirements.txt
```

2. 設定 `.env` 檔案

```ini
MISTRAL_API_KEY=你的_API_Key
FLASK_API_KEY=你的安全金鑰
```

3. 啟動服務

```bash
python web/app.py
```

API 運行位置：[http://localhost:8001/](http://localhost:8001)

## Docker 部署

透過 Docker Compose 快速部署 API：

```bash
docker-compose up --build
```

使用 curl 測試 API 是否正常運作：

```bash
curl -X POST "http://localhost:8001/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "RAG 是什麼？"}'
```

## 未來計畫

- n8n 自動化流程串接
- Line Bot 與 Discord Bot 支援
- 混合檢索技術（FAISS + BM25）提升效果

專案現已初步完成，之後有空時會再逐步優化更新。

