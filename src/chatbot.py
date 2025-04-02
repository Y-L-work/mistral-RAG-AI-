from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.scraper import scrape_url
from src.retriever import Retriever
from src.generator import Generator
from src.memory_manager import MemoryManager
from src.translator_util import is_chinese, translate_to_english
import os
import json
from src.config import NEWS_DATA_DIR
from datetime import datetime
import re

class Chatbot:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()
        self.default_search_url = "https://example.com/sample-news-article"
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.memory_manager = MemoryManager()

    def load_latest_news_data(self):
        """
        嘗試讀取最新的新聞資料 JSON 檔案，並返回其內容
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(NEWS_DATA_DIR, f"news_{date_str}.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    news_data = json.load(f)
                return news_data
            except Exception as e:
                print(f"Error loading latest news data: {e}")
                return {}
        else:
            return {}

    def extract_article_info(self, query):
        """
        根據查詢，嘗試從中提取文章標題（假設以 ** 包起來）
        """
        pattern = r"\*\*(.*?)\*\*"
        matches = re.findall(pattern, query)
        if matches:
            title = matches[0].strip()
            return title
        return None

    def process_query(self, query):
        # 若查詢中含中文，則翻譯為英文進行檢索
        if is_chinese(query):
            query_for_retrieval = translate_to_english(query)
            print("DEBUG - Translated query for retrieval:", query_for_retrieval)
        else:
            query_for_retrieval = query

        # 檢查是否為新聞詳情請求（查詢中含有文章標題和「內容」或「詳細」關鍵字）
        detail_request = False
        article_title = self.extract_article_info(query)
        if article_title and ("內容" in query or "詳細" in query):
            detail_request = True

        rewritten_query = self.generator.rephrase_query(query_for_retrieval)
        self.memory_manager.save_context({"input": query}, {"output": ""})

        # 若已有向量索引則使用現有 corpus，否則以預設 URL 爬取並建立索引
        if self.retriever.index is not None and hasattr(self.retriever, "corpus") and self.retriever.corpus:
            corpus = self.retriever.corpus
        else:
            try:
                scraped_text = scrape_url(self.default_search_url)
            except Exception as e:
                scraped_text = "無法取得最新資訊，請稍後再試。"
            corpus = self.text_splitter.split_text(scraped_text)
            self.retriever.build_index(corpus)

        if not corpus:
            raise Exception("文本拆分後無任何內容。")

        # 執行檢索，取得相關背景資訊
        distances, indices = self.retriever.search(rewritten_query, k=5)
        if len(indices) == 0:
            return "⚠️ 找不到相關內容，請提供更多上下文"
        retrieved_chunks = [corpus[i] for i in indices[0] if i < len(corpus)]
        memory_data = self.memory_manager.load_memory()
        history_context = memory_data.get("chat_history", "")

        # 如果是新聞詳情請求，嘗試從最新新聞資料中找出該文章內容
        additional_details = ""
        if detail_request:
            news_data = self.load_latest_news_data()
            # 逐一檢查每筆新聞資料，若 URL 或內容中含有文章標題則視為匹配
            for url, content in news_data.items():
                if article_title.lower() in url.lower() or article_title.lower() in content.lower():
                    additional_details = content
                    break
            if not additional_details:
                additional_details = "（注意：未能取得完整文章內容，以下回答僅根據現有背景資訊進行推測。）"

        # 根據是否為新聞詳情請求，產生不同的 prompt
        if detail_request:
            prompt = (
                "請根據以下新聞資料，詳細說明文章內容，包括文章主題、主要論點及結論：\n\n"
                f"新聞資料：\n{additional_details}\n\n"
                f"請提供詳細說明："
            )
        else:
            context = "\n---\n".join(retrieved_chunks)
            prompt = (
                "以下是對話歷史與背景資訊，請根據這些資訊回答問題，"
                "並請在回答中附上來源資料（請提供新聞來源網址或論文參考文獻）：\n\n"
                f"對話歷史：\n{history_context}\n\n"
                f"背景資訊:\n{context}\n\n"
                f"問題：{query}\n\n"
                f"回答："
            )
        print("DEBUG - prompt:", prompt)
        answer = self.generator.generate_answer(prompt)
        self.memory_manager.save_context({"input": query}, {"output": answer})
        return answer
