import os
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import json
from flask import Flask, request, jsonify
from groq import Groq

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Function to extract Product Title
def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip()
    except AttributeError:
        try:
            price = soup.find("span", attrs={'id': 'priceblock_dealprice'}).string.strip()
        except:
            price = ""
    return price

# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""
    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review_count = ""
    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()
    except AttributeError:
        available = "Not Available"
    return available

# Function to extract Product Image URL
def get_image_url(soup):
    try:
        image_container = soup.find("div", attrs={'class': 'imgTagWrapper'})
        img_tag = image_container.find('img')
        if img_tag and 'src' in img_tag.attrs:
            image_url = img_tag['src']
        else:
            image_url = ""
    except AttributeError:
        image_url = ""
    return image_url

# Function to generate product description using Groq
def generate_description(title):
    if not title:
        return "Description not available"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Generate a description for the product with the title: {title}",
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract_data():
    """
    API endpoint to process HTML and extract information
    """

    # Check if request contains HTML data
    if not request.is_json or "html" not in request.json:
        return jsonify({"error": "Missing or invalid HTML data in request"}), 400

    # Get HTML data from request
    html_data = request.get_json()["html"]

    # Parse the HTML data
    soup = BeautifulSoup(html_data, "html.parser")

    # Extract product information
    product_info = {
        "title": get_title(soup),
        "price": get_price(soup),
        "rating": get_rating(soup),
        "reviews": get_review_count(soup),
        "availability": get_availability(soup),
        "image_url": get_image_url(soup),
        "description": generate_description(get_title(soup))
    }

    return jsonify(product_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
