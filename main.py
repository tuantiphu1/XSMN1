import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": "Trả lời đúng một câu: GitHub Action hoạt động!"
        }
    ]
)

print(response.choices[0].message.content)
