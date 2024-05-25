from flask import Flask, request, render_template, jsonify
import os
import json
from helper import split_content_and_process
from scraper import get_product_details
from groq_client import combined_content_processor

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    try:
        html_content = get_product_details(url)
        if "Failed to" in html_content:
            return jsonify({"error": html_content}), 500
        
        combined_html = split_content_and_process(html_content)
        final_json = combined_content_processor(combined_html)
        
        # Save to JSON file
        with open("flipkart_data.json", "w", encoding='utf-8') as f:
            f.write(final_json)
        
        return jsonify({"message": "Data extracted successfully and saved into respective JSON file."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
