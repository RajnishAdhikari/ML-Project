from flask import Flask, request, jsonify
from transformers import LlamaForCausalLM, LlamaTokenizer
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Load the LLaMA-3 model and tokenizer
model = LlamaForCausalLM.from_pretrained("decaplusplus/llama-3b-hf")
tokenizer = LlamaTokenizer.from_pretrained("decaplusplus/llama-3b-hf")

# Function to extract product information from HTML
def extract_product_info(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Use the LLaMA-3 model to identify relevant HTML elements
    input_text = f"Extract the product name, price, description, and image URL from the following HTML:\n\n{html}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    output = model.generate(input_ids, max_length=1024, num_beams=5, early_stopping=True)
    output_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # Parse the output text to extract the required information
    product_info = {}
    lines = output_text.strip().split("\n")
    for line in lines:
        if "Product name:" in line:
            product_info["name"] = line.split("Product name:")[1].strip()
        elif "Price:" in line:
            product_info["price"] = line.split("Price:")[1].strip()
        elif "Description:" in line:
            product_info["description"] = line.split("Description:")[1].strip()
        elif "Image URL:" in line:
            product_info["image_url"] = line.split("Image URL:")[1].strip()

    return product_info

@app.route('/extract_product_info', methods=['POST'])
def extract_product_info_route():
    url = request.json.get('url')
    if url:
        try:
            response = requests.get(url)
            html = response.text
            product_info = extract_product_info(html)
            return jsonify(product_info)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "No URL provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)