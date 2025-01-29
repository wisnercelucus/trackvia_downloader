import tempfile
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

def download_selenium():
    # Create a unique temporary directory for this session
    temp_user_data_dir = tempfile.TemporaryDirectory()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-data-dir={temp_user_data_dir.name}")  # Unique user data dir
    chrome_options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://google.com")
        title = driver.title
        try:
            # Wait for the language element
            language = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "SIvCob"))
            ).text
        except Exception as e:
            language = f"Language element not found: {e}"
        
        data = {"page_title": title, "language": language}
    finally:
        driver.quit()
        temp_user_data_dir.cleanup()  # Clean up the temporary directory
    
    return data

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return download_selenium()
    elif request.method == 'POST':
        return ""

if __name__ == "__main__":
    app.run(debug=True, port=3000)
