from src.chatbot import Chatbot

def main():
    chatbot = Chatbot()
    print("歡迎使用客製化聊天機器人，輸入您的查詢（輸入 'exit' 結束）：")
    while True:
        user_input = input(">> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        try:
            answer = chatbot.process_query(user_input)
            print("回答：")
            print(answer)
        except Exception as e:
            print(f"發生錯誤：{e}")
        print("-" * 50)

if __name__ == "__main__":
    main()
