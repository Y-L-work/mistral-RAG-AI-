from langchain.text_splitter import RecursiveCharacterTextSplitter
from .scraper import scrape_url
from .retriever import Retriever
from .generator import Generator


class Chatbot:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()
        # 預設網頁搜尋 URL，建議改為穩定可用的新聞來源
        self.default_search_url = "https://example.com/sample-news-article"
        # 建立文本拆分器 (利用 LangChain)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        # 多輪對話記憶：儲存最近幾輪對話（如需持久存儲，可考慮 SQLite）
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

        # 記錄原查詢與改寫結果到對話記憶
        self.conversation_history.append({"query": query, "rewritten": rewritten_query})

        # 2. 網頁爬取：若爬取失敗則使用預設訊息
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
        distances, indices = self.retriever.search(index, embeddings, rewritten_query, k=3)
        retrieved_chunks = [chunks[i] for i in indices[0] if i < len(chunks)]

        # 5. 組合提示：加入最近幾輪對話歷史作為上下文（取最後 3 輪）
        history_context = ""
        if self.conversation_history:
            history_context = "\n".join(
                [f"使用者：{item['query']}\n機器人：{item.get('answer', 'N/A')}" for item in
                 self.conversation_history[-3:]]
            )

        context = "\n---\n".join(retrieved_chunks)
        prompt = f"以下是對話歷史與背景資訊，請根據這些資訊回答問題，並請在回答中附上來源資訊：\n對話歷史：\n{history_context}\n\n背景資訊:\n{context}\n\n問題：{query}\n\n回答："

        # 6. 調用 Mistral AI 生成回答
        answer = self.generator.generate_answer(prompt)

        # 將當前回應存入對話記憶
        self.conversation_history[-1]["answer"] = answer

        return answer
