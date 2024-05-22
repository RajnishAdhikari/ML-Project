
import os
import json
import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from groq import Groq  # Ensure you have access to this module or the equivalent Groq client library

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client with LLaMA 3 model
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def ask_question(question, model="llama3-8b-8192"):
    """ Queries the LLaMA model via Groq API to process the question. """
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": question}],
        model=model,
    )
    return chat_completion.choices[0].message.content

def extract_product_info(html):
    """ Use the LLaMA model to extract product info from HTML. """
    question = f"Extract product name, price, description, and image URL from this HTML: {html}"
    answer = ask_question(question)
    return json.loads(answer)  # Assuming the model returns JSON structured data

@app.route('/extract_product_info', methods=['GET', 'POST'])
def extract_product_info_route():
    if request.method == 'POST':
        data = request.get_json()
        url = data.get('url')
    else:
        url = request.args.get('url')

    if url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            html = response.text
            product_info = extract_product_info(html)
            
            # Save the product_info to a JSON file
            with open('product_info.json', 'w') as json_file:
                json.dump(product_info, json_file, indent=4)

            return jsonify(product_info)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "No URL provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)