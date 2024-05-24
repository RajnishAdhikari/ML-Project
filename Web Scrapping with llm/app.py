from flask import Flask, request, render_template, jsonify
import os
import json
from scraper import get_product_details

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    try:
        products = get_product_details(url)
        # Save to JSON file
        with open("amazon_data.json", "w") as f:
            json.dump(products, f, indent=4)
        return "Data extracted successfully and saved into respective JSON file."
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
