from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


app = Flask(__name__)

def download_selenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # Recommended for Docker
    chrome_options.binary_location = "/usr/bin/chromium"  # Ensure correct binary

    service = Service("/usr/bin/chromedriver")  # Explicitly use the correct ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://google.com")
        title = driver.title
        try:
            language = driver.find_element(By.XPATH, "//div[@id='SIvCob']").text
        except Exception:
            language = "Language element not found"
        return {"page_title": title, "language": language}
    finally:
        driver.quit()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return download_selenium()
    elif request.method == 'POST':
        return ""


if __name__ == "__main__":
    app.run(debug=True, port=3000)