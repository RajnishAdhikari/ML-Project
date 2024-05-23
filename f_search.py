# from autoscraper import AutoScraper
# amazon_url="https://www.amazon.in/s?k=iphones"

# wanted_list=["₹58,400","New Apple iPhone 11 (128GB) - Black"]

# scraper=AutoScraper()
# result=scraper.build(amazon_url,wanted_list)

# print(scraper.get_result_similar(amazon_url,grouped=True))


# scraper.set_rule_aliases({'rule_hii5':'Title', 'rule_ibzk':'Price'})
# scraper.keep_rules(['rule_hii5', 'rule_ibzk'])
# scraper.save('amazon_search')



from autoscraper import AutoScraper

amazon_url="https://www.amazon.com/s?k=headphone"

wanted_list = ["$165.11", "Beats Studio Pro - Wireless Bluetooth Noise Cancelling Headphones - Personalized Spatial Audio, USB-C Lossless Audio, Apple & Android Compatibility, Up to 40 Hours Battery Life - Sandstone", " 7,483"]

scraper = AutoScraper()
result = scraper.build(amazon_url, wanted_list)
# print(result)

print (scraper.get_result_similar(amazon_url,grouped=True))