from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.scraper import scrape_url
from src.retriever import Retriever
from src.generator import Generator

class Chatbot:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()
        self.default_search_url = "https://example.com/sample-news-article"

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        self.conversation_history = []

    def process_query(self, query):
        """
        完整 RAG 流程：
        1. 查詢重寫：使用 Generator.rephrase_query
        2. 網頁爬取：抓取預設網址的最新資訊
        3. 文本拆分：將爬取文本拆分成塊
        4. 向量檢索：利用 Retriever 進行檢索
        5. 組合提示：整合檢索到的內容及對話歷史
        6. 調用 Mistral AI 生成回答
        """
        # 1. 查詢重寫
        rewritten_query = self.generator.rephrase_query(query)
        self.conversation_history.append({"query": query, "rewritten": rewritten_query})

        # 2. 網頁爬取
        try:
            scraped_text = scrape_url(self.default_search_url)
        except Exception as e:
            scraped_text = "無法取得最新資訊，請稍後再試。"

        # 3. 文本拆分
        chunks = self.text_splitter.split_text(scraped_text)
        if not chunks:
            raise Exception("文本拆分後無任何內容。")

        # 4. 向量檢索
        index, embeddings = self.retriever.build_index(chunks)

        # ✅ 確保索引不為 None
        if index is None or embeddings is None or len(embeddings) == 0:
            return "❌ 向量庫未成功建立，請稍後再試"

        distances, indices = self.retriever.search(rewritten_query, k=3)
        if len(indices) == 0:
            return "⚠️ 找不到相關內容，請提供更多上下文"

        retrieved_chunks = [chunks[i] for i in indices[0] if i < len(chunks)]

        # 5. 組合提示
        history_context = "\n".join([
            f"使用者：{item['query']}\n機器人：{item.get('answer', 'N/A')}"
            for item in self.conversation_history[-3:]
        ]) if self.conversation_history else ""

        context = "\n---\n".join(retrieved_chunks)
        prompt = f"以下是對話歷史與背景資訊，請根據這些資訊回答問題，並請在回答中附上來源資訊：\n\n對話歷史：\n{history_context}\n\n背景資訊:\n{context}\n\n問題：{query}\n\n回答："

        # 6. 調用 Mistral AI 生成回答
        answer = self.generator.generate_answer(prompt)
        self.conversation_history[-1]["answer"] = answer

        return answer
