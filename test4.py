import os
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import json

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

if __name__ == '__main__':
    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    })
    URL = "https://www.amazon.com/s?k=iphone+15+pro+max&ref=nb_sb_noss_1"

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")

    links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
    links_list = ["https://www.amazon.in" + link.get('href') for link in links if link.get('href') and not link.get('href').startswith("http")]

    products = []

    for link in links_list:
        try:
            new_webpage = requests.get(link, headers=HEADERS)
            new_webpage.raise_for_status()  # Check if the request was successful
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            product = {
                "name": get_title(new_soup),
                "price": get_price(new_soup),
                "rating": get_rating(new_soup),
                "reviews": get_review_count(new_soup),
                "availability": get_availability(new_soup),
                "image_url": get_image_url(new_soup)
            }

            if product["name"]:  # Only add products that have a name
                products.append(product)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {link}\nException: {e}")

    # Save to JSON file
    with open("amazon_data.json", "w") as f:
        json.dump(products, f, indent=4)

    print("Data saved to amazon_data.json")



# here instead of giving the url manually generate code that take url from user 