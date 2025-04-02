import requests
from bs4 import BeautifulSoup
import time
import random
import os
import json
from datetime import datetime
from src.config import NEWS_DATA_DIR
from src.translator_util import translate_to_traditional

# 定義 HTTP 請求標頭，模擬一般瀏覽器
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_page(url):
    """發送 GET 請求取得網頁內容，並加入隨機延遲"""
    time.sleep(random.uniform(2, 4))
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_title(html_content):
    """從 HTML 中提取 <title> 作為文章標題"""
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        if soup.title and soup.title.string:
            return soup.title.string.strip()
    except Exception as e:
        print(f"Error extracting title: {e}")
    return None

def parse_text(html_content):
    """使用 BeautifulSoup 解析 HTML 並抽取純文字內容"""
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        return text
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return ""

def clean_text(text):
    """對抽取的文字進行清理：移除多餘空白"""
    return " ".join(text.split())

def load_existing_titles(directory):
    """
    讀取目錄中所有新聞 JSON 檔，提取已爬取文章的標題（轉小寫）
    """
    titles = set()
    if not os.path.exists(directory):
        return titles
    try:
        for filename in os.listdir(directory):
            if filename.startswith("news_") and filename.endswith(".json"):
                file_path = os.path.join(directory, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # 每筆資料格式為 { url: {"title": ..., "content": ...} }
                    for article in data.values():
                        if isinstance(article, dict) and "title" in article:
                            titles.add(article["title"].strip().lower())
    except Exception as e:
        print(f"Error loading existing titles: {e}")
    return titles

def crawl_news(urls):
    """
    針對 URL 清單進行爬蟲，返回每個 URL 的文章資訊（包含 title 與 content）
    並檢查是否重複（依據標題）－若重複則忽略該篇文章。
    """
    news_data = {}
    existing_titles = load_existing_titles(NEWS_DATA_DIR)
    for url in urls:
        print(f"Scraping URL: {url}")
        html = fetch_page(url)
        if html:
            title = get_title(html)
            if title:
                if title.strip().lower() in existing_titles:
                    print(f"Duplicate article detected (title: {title}), skipping URL: {url}")
                    continue
            raw_text = parse_text(html)
            cleaned = clean_text(raw_text)
            news_data[url] = {"title": title if title else "", "content": cleaned}
        else:
            news_data[url] = {"title": "", "content": None}
    return news_data

def save_news_data(news_data):
    """
    將爬取的新聞資料存成 JSON 檔案（含原文及繁體中文翻譯版本），並自動清除舊檔案
    """
    if not os.path.exists(NEWS_DATA_DIR):
        os.makedirs(NEWS_DATA_DIR)
    date_str = datetime.now().strftime("%Y-%m-%d")
    original_file_path = os.path.join(NEWS_DATA_DIR, f"news_{date_str}.json")
    try:
        with open(original_file_path, "w", encoding="utf-8") as f:
            json.dump(news_data, f, ensure_ascii=False, indent=4)
        print(f"News data saved to {original_file_path}")
    except Exception as e:
        print(f"Error saving news data: {e}")

    # 儲存翻譯版本（繁體中文）
    translated_data = {}
    for url, article in news_data.items():
        if article.get("content"):
            translated_content = translate_to_traditional(article["content"])
            translated_data[url] = {"title": article.get("title", ""), "content": translated_content}
        else:
            translated_data[url] = {"title": article.get("title", ""), "content": None}
    translated_file_path = os.path.join(NEWS_DATA_DIR, f"news_{date_str}_zh.json")
    try:
        with open(translated_file_path, "w", encoding="utf-8") as f:
            json.dump(translated_data, f, ensure_ascii=False, indent=4)
        print(f"Translated news data saved to {translated_file_path}")
    except Exception as e:
        print(f"Error saving translated news data: {e}")

    # 自動刪除舊檔案，若檔案數量超過 30
    clean_old_news(NEWS_DATA_DIR, max_files=30)

def clean_old_news(directory, max_files=30):
    """
    檢查目錄中檔案數量，若超過 max_files 則刪除最舊的檔案。
    """
    try:
        files = [os.path.join(directory, f) for f in os.listdir(directory) if
                 f.startswith("news_") and f.endswith(".json")]
        if len(files) > max_files:
            files.sort(key=lambda x: os.path.getmtime(x))
            files_to_delete = files[:len(files) - max_files]
            for f in files_to_delete:
                os.remove(f)
                print(f"Deleted old news file: {f}")
    except Exception as e:
        print(f"Error cleaning old news files: {e}")

if __name__ == "__main__":
    # 新增的網站清單：包含 AI 論文類與 AI 新聞類網站
    NEWS_URLS = [
        # AI 論文類網站
        "https://arxiv.org/list/cs.AI/recent",
        "https://paperswithcode.com",
        "https://openreview.net",
        "https://www.semanticscholar.org",
        # AI 新聞類網站
        "https://syncedreview.com",
        "https://venturebeat.com/category/ai/",
        "https://techcrunch.com/tag/artificial-intelligence/",
        "https://www.technologyreview.com/ai/",
        "https://www.aitrends.com",
        "https://deepai.org"
    ]
    collected_news = crawl_news(NEWS_URLS)
    for url, article in collected_news.items():
        title = article.get("title", "")
        content = article.get("content", "")
        if content:
            print(f"\nContent from {url} (Title: {title}) (first 500 chars):\n{content[:500]}...\n")
        else:
            print(f"\nNo content fetched from {url}.\n")
    save_news_data(collected_news)
