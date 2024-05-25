import os
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def content_receiver(content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{content} your task is to find out the product price, product name, product image url, product reviews and product rating with its css selector. Give me the value of each with its selector so that it is easier to read. Give me only data but not explanation.",
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content

def combined_content_processor(content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{content} your task is to find out the product price, product name, product image url and product rating with its css selector. Give me the value of each with its selector in json format, take values if present.",
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content
