from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

def download_selenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("accept-language=en-US,en;q=0.9")
    chrome_options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://google.com")
        title = driver.title

        try:
            # Debugging: Save page source to check if the element exists
            page_source = driver.page_source
            with open("debug_source.html", "w", encoding="utf-8") as f:
                f.write(page_source)

            # Wait for the element
            language = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'SIvCob')]"))
            ).text
        except Exception as e:
            language = f"Language element not found: {e}"
        
        data = {"page_title": title, "language": language}
    finally:
        driver.quit()
    
    return data

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return download_selenium()
    elif request.method == 'POST':
        return ""

if __name__ == "__main__":
    app.run(debug=True, port=3000)
