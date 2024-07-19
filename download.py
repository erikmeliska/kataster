from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import pickle
import time
import re

# Set the download directory to the script's directory and ensure the documents directory exists
script_dir = os.path.dirname(os.path.abspath(__file__))
documents_dir = os.path.join(script_dir, "documents")

if not os.path.exists(documents_dir):
    os.makedirs(documents_dir)
    print(f"Created 'documents' directory at {documents_dir}")

cookies_file = os.path.join(script_dir, "cookies.pkl")
headers_file = os.path.join(script_dir, "headers.pkl")
links_file = os.path.join(script_dir, "links.txt")

def save_cookies_and_headers(driver, cookies_file, headers_file):
    print("Saving cookies and headers...")
    cookies = driver.get_cookies()
    headers = driver.execute_script("return {...window.headers || {}}")
    with open(cookies_file, 'wb') as f:
        pickle.dump(cookies, f)
        print("Cookies saved.")
    with open(headers_file, 'wb') as f:
        pickle.dump(headers, f)
        print("Headers saved.")

def load_cookies_and_headers(session, cookies_file, headers_file):
    print("Loading cookies and headers...")
    headers = {}
    if os.path.exists(cookies_file):
        with open(cookies_file, 'rb') as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])
        print("Cookies loaded.")
    else:
        print("Cookies file not found.")
    if os.path.exists(headers_file):
        with open(headers_file, 'rb') as f:
            headers = pickle.load(f)
        print("Headers loaded.")
    else:
        print("Headers file not found.")
    return headers

def download_pdf_with_cookies(url, documents_dir, session, headers, prf_number):
    print(f"Attempting to download PDF with cookies for PRF number {prf_number}...")
    response = session.get(url, headers=headers)
    print(f"Response status code: {response.status_code}")
    if response.headers.get('Content-Type') == 'application/pdf':
        pdf_path = os.path.join(documents_dir, f'lv{prf_number}.pdf')
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        print(f"File downloaded successfully: {pdf_path}")
        return True
    print(f"Response for PRF number {prf_number} is not a PDF, likely a CAPTCHA page.")
    return False

def extract_prf_number(url):
    match = re.search(r'prfNumber=(\d+)', url)
    if match:
        return match.group(1)
    return None

def read_urls_from_file(file_path):
    print(f"Reading URLs from file: {file_path}")
    urls = []
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    print(f"Found {len(urls)} URL(s) to process.")
    return urls

# Initialize session
print("Initializing session...")
session = requests.Session()
headers = load_cookies_and_headers(session, cookies_file, headers_file)

# Read URLs from links.txt file
urls = read_urls_from_file(links_file)

# Loop through the list of URLs and attempt to download each document
for url in urls:
    prf_number = extract_prf_number(url)
    if prf_number is None:
        print(f"Could not extract PRF number from URL: {url}")
        continue

    if not download_pdf_with_cookies(url, documents_dir, session, headers, prf_number):
        # Initialize WebDriver with options to set the download directory
        print("Setting up WebDriver...")
        options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": documents_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        }
        options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=options)

        try:
            print(f"Opening browser to handle CAPTCHA for PRF number {prf_number}...")
            driver.get(url)
            print("Browser opened, waiting for CAPTCHA solving...")
            
            # Wait for user to solve the CAPTCHA and the document to start downloading
            time.sleep(60)  # Adjust the sleep time as needed to manually solve the CAPTCHA

            print("CAPTCHA should be solved now, proceeding...")
            save_cookies_and_headers(driver, cookies_file, headers_file)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            driver.quit()

        # Check if the file was downloaded
        print("Checking if the file was downloaded...")
        file_downloaded = False
        for file_name in os.listdir(documents_dir):
            if file_name.endswith('.pdf'):
                file_downloaded = True
                print(f"File downloaded successfully: {file_name}")
                break

        if not file_downloaded:
            print(f"Failed to download the file for PRF number {prf_number}.")
