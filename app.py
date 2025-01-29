import tempfile
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

def download_selenium():
    temp_user_data_dir = tempfile.TemporaryDirectory()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-data-dir={temp_user_data_dir.name}")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.104 Safari/537.36")
    chrome_options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.google.com/?hl=en")  # Force English Google

        title = driver.title

        try:
            # Debug: Save page source and screenshot
            with open("debug_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            driver.save_screenshot("debug_screenshot.png")

            # Wait for the element to be visible
            language = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@id='SIvCob']"))
            ).text
        except Exception as e:
            language = f"Language element not found: {e}"
        
        data = {"page_title": title, "language": language}
    finally:
        driver.quit()
        temp_user_data_dir.cleanup()
    
    return data

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return download_selenium()
    elif request.method == 'POST':
        return ""

if __name__ == "__main__":
    app.run(debug=True, port=3000)
