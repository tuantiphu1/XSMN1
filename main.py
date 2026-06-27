import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# ===== CONFIG =====
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# ===== 1. CRAWL XSMN =====
def get_xsmn():
    url = "https://www.minhngoc.net.vn/ket-qua-xo-so/mien-nam.html"
    r = requests.get(url, timeout=20)
    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text, "html.parser")

    # lấy toàn bộ nội dung bảng kết quả
    data = soup.get_text("\n", strip=True)

    return data[:4000]  # tránh quá dài

# ===== 2. CHATGPT FORMAT =====
def format_with_gpt(raw):
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": f"""
Hãy chuyển dữ liệu xổ số sau thành bản tin dễ đọc, gọn, có tiêu đề và chia tỉnh rõ ràng:

{raw}
"""
            }
        ]
    )
    return res.choices[0].message.content

# ===== 3. SEND TELEGRAM =====
def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

# ===== RUN =====
raw = get_xsmn()
final_text = format_with_gpt(raw)
send_telegram(final_text)

print("DONE")
