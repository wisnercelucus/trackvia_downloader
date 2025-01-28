from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


app = Flask(__name__)


def download_selenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager.install()), options=chrome_options)
    driver.get("https://google.com")
    title = driver.title
    language = driver.find_element(By.XPATH, "//div[id='SIvCob']").text
    data = {"page_title": title, "language": language}
    return data


@app.route('/', methods=['GER', 'POST'])
def home():
    if (request.method == 'GET'):
        return download_selenium()
    elif (request.method == 'POST'):
        return ""
    
    
if (__name__ == "__main__"):
    app.run(debug=True, port=3000)


