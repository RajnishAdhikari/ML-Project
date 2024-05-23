import os
from autoscraper import AutoScraper

amazon_url = "https://www.amazon.com/s?k=headphone"

wanted_list = [
    "$165.11", 
    "Beats Studio Pro - Wireless Bluetooth Noise Cancelling Headphones - Personalized Spatial Audio, USB-C Lossless Audio, Apple & Android Compatibility, Up to 40 Hours Battery Life - Sandstone", 
    "7,483"
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

for rule, values in rules.items():
    if any("$" in value for value in values):
        price_rule = rule
    elif any(value.replace(",", "").isdigit() for value in values):
        rating_rule = rule
    else:
        title_rule = rule

print(f"Identified rules - Title: {title_rule}, Price: {price_rule}, Rating: {rating_rule}")

if title_rule and price_rule and rating_rule:
    scraper.set_rule_aliases({
        title_rule: 'Title', 
        price_rule: 'Price', 
        rating_rule: 'Rating'
    })
    scraper.keep_rules([title_rule, price_rule, rating_rule])
    scraper.save('amazon-search')
    print("Scraper rules set and saved successfully.")
else:
    print("Failed to identify all required rules.")

results = scraper.get_result_similar('https://www.amazon.com/s?k=mobile', group_by_alias=True)

# Correct way to print the results for Title and Price
if 'Title' in results and 'Price' in results:
    titles = results['Title']
    prices = results['Price']
    for title, price in zip(titles, prices):
        print(f"Title: {title}, Price: {price}")
else:
    print("Title and/or Price not found in the results.")
