import time
from mistralai import Mistral
from src.config import MISTRAL_API_KEY, MISTRAL_MODEL


class Generator:
    def __init__(self):
        # 建立 Mistral 客戶端
        self.client = Mistral(api_key=MISTRAL_API_KEY)
        self.model = MISTRAL_MODEL

    def generate_answer(self, prompt, max_tokens=256, temperature=0.7, retry=3, delay=2):
        """
        傳入組合好的 prompt，調用 Mistral AI 生成回答。
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
                return response.choices[0].message.content
            except Exception as e:
                if "429" in str(e):
                    print(f"速率限制，等待 {delay} 秒後重試 (嘗試 {attempt+1}/{retry})")
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
                    print(f"速率限制，等待 {delay} 秒後重試 (嘗試 {attempt+1}/{retry})")
                    time.sleep(delay)
                else:
                    raise e
        raise Exception("查詢改寫失敗，多次重試仍然無法解決速率限制問題。")
