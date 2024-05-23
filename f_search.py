import os
from autoscraper import AutoScraper

amazon_url = "https://www.amazon.com/s?k=headphone"

wanted_list = [
    "$165.11", 
    "Beats Studio Pro - Wireless Bluetooth Noise Cancelling Headphones - Personalized Spatial Audio, USB-C Lossless Audio, Apple & Android Compatibility, Up to 40 Hours Battery Life - Sandstone", 
    "7,483",
    "https://m.media-amazon.com/images/I/51t0IE0zjaL._AC_SX522_.jpg"
]

scraper = AutoScraper()
result = scraper.build(amazon_url, wanted_list)
print("Initial result:", result)

# Group the results
rules = scraper.get_result_similar(amazon_url, grouped=True)
print("Grouped rules:", rules)

# Identify the correct rules
title_rule = None
price_rule = None
rating_rule = None
image_rule = None

for rule, values in rules.items():
    if any("$" in value for value in values):
        price_rule = rule
    elif any(value.replace(",", "").isdigit() for value in values):
        rating_rule = rule
    elif any(value.startswith("http") and "amazon.com/images" in value for value in values):
        image_rule = rule
    else:
        title_rule = rule

print(f"Identified rules - Title: {title_rule}, Price: {price_rule}, Rating: {rating_rule}, Image: {image_rule}")

if title_rule and price_rule and rating_rule and image_rule:
    scraper.set_rule_aliases({
        title_rule: 'Title', 
        price_rule: 'Price', 
        rating_rule: 'Rating',
        image_rule: 'Image'
    })
    scraper.keep_rules([title_rule, price_rule, rating_rule, image_rule])
    scraper.save('amazon-search')
    print("Scraper rules set and saved successfully.")
else:
    print("Failed to identify all required rules.")

# Load the saved scraper
scraper.load('amazon-search')

# Get results for the new URL
results = scraper.get_result_similar('https://www.amazon.com/s?k=iphone', group_by_alias=True)

# Print the raw results for debugging
print("Results from new URL (grouped by alias):", results)

# Correct way to print the results for Title, Price, and Image
if 'Title' in results and 'Price' in results and 'Image' in results:
    titles = results['Title']
    prices = results['Price']
    images = results['Image']
    for title, price, image in zip(titles, prices, images):
        print(f"Title: {title}, Price: {price}, Image: {image}")
else:
    print("Title, Price, and/or Image not found in the results.")
