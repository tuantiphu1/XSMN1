import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# ======================
# CONFIG
# ======================
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL = "https://www.minhngoc.net.vn/ket-qua-xo-so/mien-nam.html"


# ======================
# 1. CRAWL XSMN (RAW DATA)
# ======================
def get_xsmn():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers, timeout=20)
    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text, "html.parser")

    # lấy toàn bộ bảng kết quả (ổn định hơn get_text)
    tables = soup.find_all("table")

    data = []

    for t in tables:
        text = t.get_text("\n", strip=True)
        if len(text) > 200:
            data.append(text)

    return "\n\n".join(data)


# ======================
# 2. CHATGPT FORMAT (KHÔNG BỊ BỊA)
# ======================
def format_with_gpt(raw):
    prompt = f"""
Bạn là hệ thống định dạng dữ liệu xổ số miền Nam.

QUY TẮC QUAN TRỌNG:
- CHỈ dùng dữ liệu được cung cấp bên dưới
- KHÔNG được tự thêm số, không đoán, không bịa
- Nếu thiếu dữ liệu thì ghi "không có dữ liệu"
- Trình bày gọn, dễ đọc theo từng tỉnh

DỮ LIỆU:
{raw}
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return res.choices[0].message.content


# ======================
# 3. TELEGRAM SEND
# ======================
def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    })


# ======================
# MAIN FLOW
# ======================
def main():
    print("Fetching XSMN...")

    raw = get_xsmn()

    if not raw or len(raw) < 500:
        send_telegram("❌ Không lấy được dữ liệu xổ số")
        return

    print("Formatting with GPT...")

    final_text = format_with_gpt(raw)

    print("Sending Telegram...")

    send_telegram(final_text)

    print("DONE")


if __name__ == "__main__":
    main()
