# from flask import Flask, request, jsonify
# from transformers import LlamaForCausalLM, AutoTokenizer
# import requests
# from bs4 import BeautifulSoup
# import os
# from dotenv import load_dotenv

# app = Flask(__name__)

# # Load environment variables from .env file
# load_dotenv()

# # Set environment variable to disable symlinks warning
# os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# # Access the Hugging Face API token
# hf_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')

# # Model ID
# model_id = "meta-llama/Meta-Llama-3-8B"

# # Load the LLaMA-3 model and tokenizer with the token
# model = LlamaForCausalLM.from_pretrained(model_id, token=hf_token)
# tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_token)

# # Function to extract product information from HTML
# def extract_product_info(html):
#     soup = BeautifulSoup(html, 'html.parser')

#     # Use the LLaMA-3 model to identify relevant HTML elements
#     input_text = f"Extract the product name, price, description, and image URL from the following HTML:\n\n{html}"
#     input_ids = tokenizer.encode(input_text, return_tensors="pt")
#     output = model.generate(input_ids, max_length=1024, num_beams=5, early_stopping=True)
#     output_text = tokenizer.decode(output[0], skip_special_tokens=True)

#     # Parse the output text to extract the required information
#     product_info = {}
#     lines = output_text.strip().split("\n")
#     for line in lines:
#         if "Product name:" in line:
#             product_info["name"] = line.split("Product name:")[1].strip()
#         elif "Price:" in line:
#             product_info["price"] = line.split("Price:")[1].strip()
#         elif "Description:" in line:
#             product_info["description"] = line.split("Description:")[1].strip()
#         elif "Image URL:" in line:
#             product_info["image_url"] = line.split("Image URL:")[1].strip()

#     return product_info

# @app.route('/extract_product_info', methods=['POST'])
# def extract_product_info_route():
#     url = request.json.get('url')
#     if url:
#         try:
#             response = requests.get(url)
#             html = response.text
#             product_info = extract_product_info(html)
#             return jsonify(product_info)
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500
#     else:
#         return jsonify({"error": "No URL provided"}), 400

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Access the Hugging Face API token
hf_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')

# Hugging Face Inference API endpoint
api_url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B"

# Headers for authorization
headers = {"Authorization": f"Bearer {hf_token}"}

# Function to extract product information from HTML
def extract_product_info(html):
    input_text = f"Extract the product name, price, description, and image URL from the following HTML:\n\n{html}"
    
    # Sending request to Hugging Face Inference API
    response = requests.post(api_url, headers=headers, json={"inputs": input_text})
    
    if response.status_code == 200:
        output_text = response.json()[0]['generated_text']
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
    else:
        return {"error": f"Failed to extract product information, status code: {response.status_code}, response: {response.text}"}

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
