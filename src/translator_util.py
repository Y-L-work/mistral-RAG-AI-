import asyncio
from googletrans import Translator
import threading

translator = Translator()

def run_async(fn, *args, **kwargs):
    """
    接受一個函式 fn 與參數，每次執行時都重新建立 coroutine，
    先嘗試直接使用 asyncio.run()，若當前已有事件循環則在新執行緒中執行。
    """
    def run():
        return asyncio.run(fn(*args, **kwargs))
    try:
        return run()
    except RuntimeError:
        result_container = []
        def worker():
            result = asyncio.run(fn(*args, **kwargs))
            result_container.append(result)
        t = threading.Thread(target=worker)
        t.start()
        t.join()
        return result_container[0]

def translate_to_english(text):
    """將文本翻譯成英文"""
    try:
        result = run_async(translator.translate, text, src='zh-cn', dest='en')
        return result.text
    except Exception as e:
        print("翻譯到英文錯誤:", e)
        return text

def translate_to_traditional(text):
    """將英文文本翻譯成繁體中文"""
    try:
        result = run_async(translator.translate, text, src='en', dest='zh-tw')
        return result.text
    except Exception as e:
        print("翻譯到繁體中文錯誤:", e)
        return text

def is_chinese(text):
    """判斷文本中是否包含中文字符"""
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False
