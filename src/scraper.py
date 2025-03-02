import requests
from bs4 import BeautifulSoup
from src.utils import clean_text


def scrape_url(url):
    """
    使用 Requests 與 BeautifulSoup 爬取網頁內容，
    並回傳清理後的純文字。
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"無法取得 {url}，狀態碼: {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return clean_text(text)
