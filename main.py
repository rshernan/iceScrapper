from flask import Flask, jsonify, request, abort
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pandas

app = Flask(__name__)


options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("disable-gpu")
options.add_argument("no-sandbox") 
driver = webdriver.Chrome("C:\\chromedriver.exe",chrome_options=options)

def transformUrl(url):
    content=""
    driver.get("https://translate.google.es/translate?hl=es&sl=es&tl=en&u="+url)
    content = driver.page_source
    soup = BeautifulSoup(content)
    iframes=soup.find_all('iframe',{"src":True})
    content=iframes[0]['src']
    return content

@app.route('/TEST', methods=['GET'])
def get_tasks():
    driver.get(transformUrl("www.google.com"))
    content = driver.page_source
    soup = BeautifulSoup(content)
    return jsonify(str(soup))

@app.route('/source', methods=['POST'])
def create_task():
    if not request.json or not 'url' in request.json:
        abort(400)
    driver.get(transformUrl(request['url']))
    content = driver.page_source
    soup = BeautifulSoup(content)
    return jsonify(str(soup))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False, port=5000)

