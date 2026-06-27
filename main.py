import os
import requests
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": "Viết một câu chào ngắn gửi Telegram."
        }
    ]
)

message = response.choices[0].message.content

bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": chat_id,
        "text": message
    }
)

print("Đã gửi Telegram.")
