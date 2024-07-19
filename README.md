Certainly! Here’s a README file for the script:

---

# Document Downloader with CAPTCHA Handling

## Overview

This script downloads PDF documents from a list of URLs. If the request is blocked by a CAPTCHA, the script will open a browser for manual CAPTCHA solving and then proceed to download the document. The downloaded files are named according to their `prfNumber` parameter in the URL.

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

## Usage

1. **Configure URLs**:
   - Edit the `urls` list in the script to include the URLs of the documents you want to download.

2. **Run the Script**:
   ```bash
   python download.py
   ```

3. **Handling CAPTCHA**:
   - If a CAPTCHA is encountered, the script will automatically open a Chrome browser window.
   - Solve the CAPTCHA manually.
   - The script will then proceed to save cookies and attempt to download the document again.

4. **Script Behavior**:
   - If the file is successfully downloaded, it will be saved in the script's directory with the name format `lv<prfNumber>.pdf`.
   - If the CAPTCHA is not solved or the document cannot be downloaded, appropriate messages will be logged to the console.

## Script Details

- **Initialization**: 
  - The script initializes a session with `requests` and attempts to use saved cookies to download the document.
  
- **Manual CAPTCHA Handling**:
  - If cookies are not valid or CAPTCHA is detected, the script opens a Chrome browser to manually solve the CAPTCHA.
  - After solving CAPTCHA, cookies and headers are saved for future use.

- **File Naming**:
  - Each downloaded file is named using the format `lv<prfNumber>.pdf`, where `<prfNumber>` is extracted from the URL.

- **Error Handling**:
  - The script includes error handling and logging to help diagnose issues during execution.

## Example

To download documents for URLs with PRF numbers `5541` and `5542`, you would configure the `urls` list as follows:

```python
urls = [
    "https://kataster.skgeodesy.sk/Portal45/api/Bo/GeneratePrfPublic/?cadastralUnitCode=877891&prfNumber=5541&outputType=pdf",
    "https://kataster.skgeodesy.sk/Portal45/api/Bo/GeneratePrfPublic/?cadastralUnitCode=877891&prfNumber=5542&outputType=pdf",
]
```

After running the script, the documents will be saved as `lv5541.pdf` and `lv5542.pdf` in the same directory as the script.

## Troubleshooting

- **Browser Not Opening**: Ensure Chrome and ChromeDriver are correctly installed and their versions are compatible.
- **CAPTCHA Not Solved**: Make sure you solve the CAPTCHA within the allotted time. Adjust `time.sleep` if needed.
- **File Not Downloaded**: Verify that the URL is correct and the server response is as expected.

## License

This script is provided as-is. Feel free to modify and use it according to your needs. No warranty is provided regarding its functionality or suitability for any purpose.

---

Feel free to adjust the README according to your needs or additional details specific to your project.