"""
memory_manager.py

這個模組封裝了 LangChain 的 ConversationBufferMemory，
用於管理對話歷史記憶。你可以透過 load、save 與 clear
等方法來操作對話上下文，方便整合至聊天機器人的流程中。
"""

from langchain.memory import ConversationBufferMemory


class MemoryManager:
    def __init__(self, memory_key="chat_history", return_messages=True):
        """
        初始化 MemoryManager。

        :param memory_key: 用於存放對話歷史的 key（預設為 "chat_history"）。
        :param return_messages: 是否在讀取記憶時返回訊息物件（預設 True）。
        """
        self.memory = ConversationBufferMemory(
            memory_key=memory_key,
            return_messages=return_messages
        )

    def load_memory(self):
        """
        載入目前對話記憶內容。

        :return: 一個字典，包含對話記憶（例如 {"chat_history": "使用者與機器人的對話內容"}）。
        """
        return self.memory.load_memory_variables({})

    def save_context(self, input_data, output_data):
        """
        保存一段新的對話上下文至記憶中。

        :param input_data: 輸入訊息的字典，例如 {"input": "使用者的訊息"}。
        :param output_data: 輸出訊息的字典，例如 {"output": "機器人的回應"}。
        """
        self.memory.save_context(input_data, output_data)

    def clear_memory(self):
        """
        清空目前的對話記憶。
        """
        self.memory.clear()
