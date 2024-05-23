import os
import re
import requests
import uuid
import zipfile
import hashlib
import shutil
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Function to validate URLs
def validator(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# Function to find files on a webpage
def finder(url, soup, media_type):
    files = []

    # Find image files
    if media_type == "image":
        tags = ['jpg', 'jpeg', 'png', 'svg', 'gif', 'webp', 'tiff', 'psd', 'eps', 'ai', 'indd', 'raw']
        for tag in soup.find_all('img'):
            file = tag.get('src')
            if file and any(ext in file for ext in tags):
                file_url = file
                if not validator(file_url):
                    file_url = urljoin(url, file_url)
                files.append(file_url)

    # Find text
    elif media_type == "text":
        text_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'strong']
        for tag in text_tags:
            for element in soup.find_all(tag):
                files.append(element.get_text(strip=True))

    # Find links
    else:
        for link in soup.find_all('a'):
            file = link.get('href')
            if media_type in file:
                file_url = file
                if not validator(file_url):
                    file_url = urljoin(url, file_url)
                files.append(file_url)

    return files

# Function to download the files
def downloader(urls, folder_name):
    os.makedirs(folder_name, exist_ok=True)
    for i, url in enumerate(urls):
        response = requests.get(url, stream=True)
        file_extension = url.split(".")[-1].split("&")[0]
        url_hash = hashlib.md5(url.encode()).hexdigest()
        unique_id = str(uuid.uuid4())[:8]
        file_name = f'{url_hash}-{unique_id}.{file_extension}'
        file_name = file_name[:255]
        file_name = re.sub(r'[\\/:"*?<>|]+', '_', file_name)
        with open(f'{folder_name}/{file_name}', 'wb') as out_file:
            out_file.write(response.content)
        print(f"Downloaded file: {file_name}")

# Function to create zip file
def zipper(folder_name):
    if os.listdir(folder_name):
        with zipfile.ZipFile(f'{folder_name}.zip', 'w') as zipf:
            for file in os.listdir(folder_name):
                zipf.write(f'{folder_name}/{file}')
        return f'{folder_name}.zip'
    else:
        return ""

# Function to access website
def scrapper(url, images=False, text=False):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except (requests.exceptions.RequestException, ValueError):
        print(f"Unable to access URL: {url}")
        return None, None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Clear previous data
    if images:
        shutil.rmtree('images', ignore_errors=True)
    if text:
        shutil.rmtree('text', ignore_errors=True)

    # Add images to the image folder
    if images:
        image_urls = finder(url, soup, 'image')
        os.makedirs('images', exist_ok=True)
        if image_urls:
            downloader(image_urls, 'images')
        else:
            print("Found no images.")

    # Add text files to the text folder
    if text:
        text_content = finder(url, soup, 'text')
        os.makedirs('text', exist_ok=True)
        if text_content:
            with open('text/content.txt', 'w') as text_file:
                for line in text_content:
                    text_file.write(line + '\n')

    # Output folder(s) as zip files
    images_zip_file, text_zip_file = None, None
    if images and os.path.exists('images') and os.listdir('images'):
        images_zip_file = zipper('images')
    if text and os.path.exists('text') and os.listdir('text'):
        text_zip_file = zipper('text')
    return images_zip_file, text_zip_file

# Function to find requests errors
def checker(url, media_types):
    if not url:
        raise ValueError("URL cannot be empty.")
    if not url.startswith("https://"):
        raise ValueError("The URL must begin with https://")
    if not media_types:
        raise ValueError("At least one media type must be selected.")
    try:
        image_file, text_file = scrapper(url, "Images" in media_types, "Text" in media_types)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            raise ValueError("HTTP Error: Forbidden. Access to the URL is forbidden.")
        else:
            raise ValueError(f"HTTP Error: {e.response.status_code}")
    except TypeError as e:
        raise ValueError(f"TypeError: {str(e)}")
    except (requests.exceptions.RequestException, ValueError):
        raise ValueError(f"Unable to access URL: {url}")

    files = []
    if "Text" in media_types and not text_file:
        raise ValueError("Found no text.")
    if "Images" in media_types and not image_file:
        raise ValueError("Found no images.")
    if image_file:
        files.append(image_file)
    if text_file:
        files.append(text_file)

    print(f"Returning downloaded files from {url} in {files} ...")

    return files

# Example usage
if __name__ == "__main__":
    url = "https://www.amazon.com/Samsung-SM-155M-DSN-Unlocked-International/dp/B0CSB1GX4H/ref=sr_1_1?sr=8-1"
    media_types = ["Images", "Text"]
    downloaded_files = checker(url, media_types)
    print(downloaded_files)
