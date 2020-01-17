from flask import Flask, request, jsonify
from instragram import main
from youtube import main as youtubeMain
from flask_cors import CORS
from selenium import webdriver

app = Flask(__name__)
CORS(app)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--lang=en-us')
options.add_argument('--log-level=3')

driver = webdriver.Chrome("./chromedriver", chrome_options=options)


@app.route('/')
def basic():
    return 'Server is running ....'


@app.route('/instragram', methods=['GET'])
def instragram():
    url = request.args.get('url')
    result = main(url, driver)
    return result


@app.route('/youtube', methods=['GET'])
def youtube():
    url = request.args.get('url')
    result = youtubeMain(url, driver)
    return result


if __name__ == '__main__':
    app.run()
