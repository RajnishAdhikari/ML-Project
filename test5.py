import os
import requests
from bs4 import BeautifulSoup
from groq import Groq

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),  # Ensure you have set your Groq API key in the environment variables
)

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
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Generate a product description for the following title: {title}",
            }
        ],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content

def extract_info(html_content):
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
    
    return product_info

# Example usage
if __name__ == "__main__":
    # Replace this with the actual HTML content you want to process
    html_content = """https://www.amazon.com/s?k=iphone+15+pro+max&ref=nb_sb_noss_1"""
    
    product_info = extract_info(html_content)
    print(product_info)
