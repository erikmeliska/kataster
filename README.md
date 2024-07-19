# Document Downloader with CAPTCHA Handling

## Overview

This script downloads PDF documents from a list of URLs provided in a `links.txt` file. If the request is blocked by a CAPTCHA, the script will open a browser for manual CAPTCHA solving and then proceed to download the document. The downloaded files are saved in a `documents` directory and named according to their `prfNumber` parameter in the URL.

## Requirements

- Python 3.x
- Selenium
- Requests
- Chrome WebDriver
- Chrome Browser

## Installation

1. **Install Python 3.x**: Ensure Python 3.x is installed on your system.

2. **Install Required Python Packages**:
    ```bash
    pip install selenium requests
    ```

3. **Download Chrome WebDriver**:
    - Download the appropriate version of [ChromeDriver](https://sites.google.com/chromium.org/driver/) that matches your Chrome browser version.
    - Place the `chromedriver` executable in a directory that is in your system's PATH or specify its location directly in the script.

## Configuration

1. **Prepare `links.txt`**:
    - Create a file named `links.txt` in the same directory as the script.
    - Add the URLs of the documents you want to download, one URL per line.

2. **Run the Script**:
    ```bash
    python download.py
    ```

3. **Handling CAPTCHA**:
    - If a CAPTCHA is encountered, the script will automatically open a Chrome browser window.
    - Solve the CAPTCHA manually.
    - The script will then proceed to save cookies and attempt to download the document again.

4. **Document Storage**:
    - Documents are saved in the `documents` directory within the script's directory.
    - Each document is named using 
