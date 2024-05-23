import os
import json
import requests
import pandas as pd
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
    """Queries the LLaMA model via Groq API to process the question."""
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": question}],
        model=model,
    )
    return chat_completion.choices[0].message.content

def extract_product_info(html):
    """Use the LLaMA model to extract product info from HTML."""
    soup = BeautifulSoup(html, 'html.parser')

    # Extract product details using BeautifulSoup with updated selectors
    product_name = soup.find('span', {'class': 'pdp-mod-product-badge-title'}).get_text(strip=True) if soup.find('span', {'class': 'pdp-mod-product-badge-title'}) else "Not found"
    price = soup.find('span', {'class': 'pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl'}).get_text(strip=True) if soup.find('span', {'class': 'pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl'}) else "Not found"
    if price == "Not found":
        price = soup.find('span', {'class': 'pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs'}).get_text(strip=True) if soup.find('span', {'class': 'pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs'}) else "Not found"
    description_elements = soup.find_all('li', {'class': ''})
    description = ' '.join([element.get_text(strip=True) for element in description_elements]) if description_elements else "Not found"
    image_url = soup.find('img', {'class': 'gallery-preview-panel__image'}).get('src') if soup.find('img', {'class': 'gallery-preview-panel__image'}) else "Not found"

    # Validate/Refine with LLaMA 3
    question = f"Extract product name, price, description, and image URL from this HTML: {html}"
    answer = ask_question(question)

    try:
        refined_data = json.loads(answer)  # Assuming the model returns JSON structured data
    except json.JSONDecodeError:
        refined_data = {}

    # Merge the results, prioritize LLaMA 3 output
    product_info = {
        "name": refined_data.get("name", product_name),
        "price": refined_data.get("price", price),
        "description": refined_data.get("description", description),
        "image_url": refined_data.get("image_url", image_url)
    }

    return product_info

def process_urls_from_excel(file_path):
    """Read URLs from an Excel file and process each one."""
    df = pd.read_excel(file_path)
    results = []

    for url in df['url']:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        product_info = extract_product_info(html)
        results.append(product_info)

    with open('product_info.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)

    return results

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
    file_path = "D:\\Data Science\\LLama3 Project\\url_sheet.xlsx"
    process_urls_from_excel(file_path)
    app.run(debug=True)
