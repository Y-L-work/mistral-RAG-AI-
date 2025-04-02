import time
from mistralai import Mistral
from src.config import MISTRAL_API_KEY, MISTRAL_MODEL
import re


class Generator:
    def __init__(self):
        # 建立 Mistral 客戶端
        self.client = Mistral(api_key=MISTRAL_API_KEY)
        self.model = MISTRAL_MODEL

    def generate_answer(self, prompt, max_tokens=4096, temperature=0.7, retry=3, delay=2):
        """
        傳入組合好的 prompt，調用 Mistral AI 生成回答。
        生成回答的 token 數量上限設定為 4096，
        遇到速率限制或其他 API 錯誤時，會重試指定次數。
        """
        for attempt in range(retry):
            try:
                response = self.client.chat.complete(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                answer = response.choices[0].message.content
                formatted_answer = self.format_answer(answer)
                return formatted_answer
            except Exception as e:
                if "429" in str(e):
                    print(f"速率限制，等待 {delay} 秒後重試 (嘗試 {attempt + 1}/{retry})")
                    time.sleep(delay)
                else:
                    raise e
        raise Exception("生成回答失敗，多次重試仍然無法解決速率限制問題。")

    def rephrase_query(self, query, max_tokens=64, temperature=0.5, retry=3, delay=2):
        """
        使用 Mistral AI 對查詢進行改寫，使其更精準，並具備重試機制。
        """
        prompt = f"請改寫以下查詢，使其更精準：\n查詢：{query}\n改寫後的查詢："
        for attempt in range(retry):
            try:
                response = self.client.chat.complete(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content
            except Exception as e:
                if "429" in str(e):
                    print(f"速率限制，等待 {delay} 秒後重試 (嘗試 {attempt + 1}/{retry})")
                    time.sleep(delay)
                else:
                    raise e
        raise Exception("查詢改寫失敗，多次重試仍然無法解決速率限制問題。")

    def format_answer(self, answer):
        """
        自動排版與換行處理：
        1. 保護 Markdown 連結（例如 [arXiv:2503.22655](https://arxiv.org/abs/2503.22655)），
           避免其中的標點符號導致換行斷裂。
        2. 先將 URL（非 Markdown 連結）以 placeholder 取代。
        3. 在常見標點（句號、問號、驚嘆號）後加入換行。
        4. 對列表項（例如 "-" 或數字開頭）加入縮排換行。
        5. 如果回答中出現「論文」、「作者」、「參考文獻」等關鍵字，
           則額外對「日期」、「摘要」、「作者」及「參考文獻」進行換行與縮排處理。
        6. 最後恢復之前保護的 Markdown 連結與 URL。
        """
        # Step 0: 保護 Markdown 連結
        md_link_pattern = r'\[[^\]]+\]\([^)]+\)'
        md_links = re.findall(md_link_pattern, answer)
        for i, link in enumerate(md_links):
            answer = answer.replace(link, f"__MD_LINK_PLACEHOLDER_{i}__")

        # Step 1: 保護純 URL（非 Markdown 連結）
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, answer)
        for i, url in enumerate(urls):
            answer = answer.replace(url, f"__URL_PLACEHOLDER_{i}__")

        # Step 2: 在標點符號後插入換行
        formatted = re.sub(r'([。\.！？!?])', r'\1\n', answer)

        # Step 3: 對列表項自動換行與縮排
        formatted = re.sub(r'\s*-\s+', r'\n   - ', formatted)  # 處理橫線列表
        formatted = re.sub(r'(\d+\.)\s*', r'\n\1 ', formatted)  # 處理數字項目

        # Step 4: 針對論文資訊額外排版（關鍵字：論文、作者、參考文獻、日期、摘要）
        if any(keyword in formatted for keyword in ["論文", "作者", "參考文獻", "日期：", "摘要："]):
            formatted = re.sub(r'(作者：)', r'\1\n   ', formatted)
            formatted = re.sub(r'(參考文獻：)', r'\1\n   ', formatted)
            formatted = re.sub(r'(日期：)', r'\n   \1', formatted)
            formatted = re.sub(r'(摘要：)', r'\n   \1', formatted)

        # Step 5: 將連續換行壓縮為單一換行
        formatted = re.sub(r'\n+', '\n', formatted)

        # Step 6: 恢復 URL placeholders
        for i, url in enumerate(urls):
            formatted = formatted.replace(f"__URL_PLACEHOLDER_{i}__", url)

        # Step 7: 恢復 Markdown 連結 placeholders
        for i, link in enumerate(md_links):
            formatted = formatted.replace(f"__MD_LINK_PLACEHOLDER_{i}__", link)

        return formatted.strip()
