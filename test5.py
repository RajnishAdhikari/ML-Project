from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

app = Flask(__name__)

# Load a pre-trained transformer model from Hugging Face for text generation
model_name = "gpt2"  # You can choose any other model that suits your needs
generator = pipeline('text-generation', model=model_name)

def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

def get_price(soup):
    try:
        price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip()
    except AttributeError:
        try:
            price = soup.find("span", attrs={'id': 'priceblock_dealprice'}).string.strip()
        except:
            price = ""
    return price

def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""
    return rating

def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review_count = ""
    return review_count

def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()
    except AttributeError:
        available = "Not Available"
    return available

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

def generate_description(title):
    if not title:
        return "Description not available"
    generated_text = generator(title, max_length=50, num_return_sequences=1)
    return generated_text[0]['generated_text']

@app.route("/extract", methods=["POST"])
def extract_info():
    if not request.json or 'html' not in request.json:
        return jsonify({"error": "Invalid input"}), 400

    html_content = request.json['html']
    soup = BeautifulSoup(html_content, "html.parser")
    
    title = get_title(soup)
    price = get_price(soup)
    rating = get_rating(soup)
    review_count = get_review_count(soup)
    availability = get_availability(soup)
    image_url = get_image_url(soup)
    description = generate_description(title)
    
    product_info = {
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": review_count,
        "availability": availability,
        "image_url": image_url,
        "description": description
    }
    
    return jsonify(product_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
