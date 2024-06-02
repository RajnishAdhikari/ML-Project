import requests
from bs4 import BeautifulSoup
import time

HEADERS = ({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
})

def get_product_details(url, max_retries=5, backoff_factor=0.3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS)
            if response.status_code == 200:
                html_content = response.content.decode('utf-8')
                soup = BeautifulSoup(html_content, 'html.parser')
                div_content = soup.find('div', class_='YJG4Cf')
                if div_content:
                    for tag in div_content(['script', 'style', 'header', 'footer']):
                        tag.decompose()
                    for div in div_content.find_all('div', class_='HKcm+1'):
                        div.decompose()
                    for div in div_content.find_all('div', class_='col EPCmJX'):
                        div.decompose()
                    for div in div_content.find_all('div', class_='xuHtQW'):
                        div.decompose()
                    for div in div_content.find_all('div', class_='pPAw9M'):
                        div.decompose()
                    return str(div_content)
                else:
                    return "Failed to find the <div> with class='YJG4Cf'"
            else:
                print(f"Failed to retrieve content. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        time.sleep(backoff_factor * (2 ** attempt))
    return "Failed to retrieve content after multiple attempts."
