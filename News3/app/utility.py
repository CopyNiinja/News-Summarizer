import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
gro_api_key=os.getenv("GROQ_API_KEY")

def generate_summary(news_body):
    client = Groq(
        api_key=gro_api_key,
    )
    chat_completion = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
            {
                "role": "system",
                "content": "You are expert in news summarization in bengali languages. Please summarize the following news article in top  3-5 bullet points in the bengali language that you get."
            },
            {
                "role": "user",
                "content": news_body
            }
        ],
        temperature=0,
        max_tokens=2000,
        top_p=1,
        stream=False,
        stop=None,
    )
    return chat_completion.choices[0].message.content




