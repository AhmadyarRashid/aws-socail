
from flask import Flask, request, jsonify
from instragram import main
from youtube import youtubeMain
from flask_cors import CORS
from selenium import webdriver
import os
from pyvirtualdisplay import Display

app = Flask(__name__)
CORS(app)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--lang=en-us')
options.add_argument('--log-level=3')
options.add_argument('--disable-extensions')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')

outputdir = "/home/ubuntu/aws-socail/"
service_log_path = "{}/chromedriver.log".format(outputdir)
service_args = ['--verbose']

display = Display(visible=0, size=(800, 600))
display.start()

driver = webdriver.Chrome(chrome_options=options,service_args=service_args,service_log_path=service_log_path)

@app.route('/youtube', methods=['GET'])
def basic():
    url = request.args.get('url')
    print('--- url -----', url)
    result = youtubeMain(url, driver)
    return result

@app.route('/yt', methods=['GET'])
def youtube():
    return 'youtube api is working'
    url = request.args.get('url')
    print('--- url -----', url)
    result = youtubeMain(url, driver)
    return result

@app.route('/instragram', methods=['GET'])
def instragram():
    url = request.args.get('url')
    result = main(url, driver)
    return result


if __name__ == '__main__':
    print("server is running")
    #app.run()
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)
