import asyncio
from googletrans import Translator

translator = Translator()

async def async_translate(text, src, dest):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, translator.translate, text, src, dest)
    return result

def translate_to_english(text):
    """將文本翻譯成英文"""
    try:
        result = asyncio.run(async_translate(text, src='zh-cn', dest='en'))
        return result.text
    except Exception as e:
        print("翻譯到英文錯誤:", e)
        return text

def translate_to_traditional(text):
    """將英文文本翻譯成繁體中文"""
    try:
        result = asyncio.run(async_translate(text, src='en', dest='zh-tw'))
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
