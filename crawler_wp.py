import re
import requests
import os
from os.path import join, dirname
from bs4 import BeautifulSoup
from flask import Flask, request
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'production.env')
load_dotenv(dotenv_path)
SECRET_KEY = os.environ.get("SECRET_KEY")
TOKEN_API_WPSCAN = os.environ.get("TOKEN_API_WPSCAN")

API_WPSCAN = "https://wpscan.com/api/v3/wordpresses/"


def request_url_wp(url):
    try:

        validation_url = re.findall(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", url)
        if validation_url:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                print("Error making request")
                return {'error': 'Error making request'}
        else:
            return 400

    except Exception as error:
        print("Error making request")
        print(error)
        return {'error': 'Error making request'}


def parsing(response_xml):
    try:
        soup = BeautifulSoup(response_xml, 'lxml')
        return soup
    except Exception as error:
        print("Error when doing parsing XML")
        print(error)
        return {'error': 'Error when doing parsing XML'}


def get_version(content):
    try:
        result = content.find("generator").get_text().strip()
        if result:
            regex = re.findall(r"\bv?[0-9]+\.[0-9]+\.[0-9]+(?:\.[0-9]+)?\b", result)
        if regex:
            version = regex[0].replace(".", '')
            return version
    except Exception as error:
        print("Not Regex version: ", error)
        return {'error': 'Not Regex version'}


def request_api_wpscan(version):
    try:
        request_wp_scan = requests.get("{}{}".format(API_WPSCAN, version),
                                       headers={
                                           'Authorization': TOKEN_API_WPSCAN})
        if request_wp_scan.status_code == 200:
            return request_wp_scan.json()
    except Exception as error:
        print("Error when doing request api: ", error)
        return {'error': 'Error when doing request api'}


app = Flask(__name__)


@app.route('/', methods=['POST'])
def get_testing():
    try:
        token = request.headers['Authorization_Secret_Token']
        if token == SECRET_KEY:

            content = request.json

            url_request = content['url'] + '/feed/'

            request_api = request_url_wp(url_request)

            if request_api == 400:
                return 'Invalid Url', 400

            response_parse = parsing(request_api)
            version_found = get_version(response_parse)
            response_data = request_api_wpscan(version_found)

            return response_data

        else:
            return 'No permission to request, IP: {}'.format(request.remote_addr), 403

    except Exception as error:
        print('Error:',  error)
        return 'Internal Server Error, IP: {}'.format(request.remote_addr), 500


if __name__ == "__main__":
    request_api = request_url_wp('https://blog.consistem.com.br/feed')
    if request_api == 400:
        print('Invalid Url')
        exit()
    if request_api:
        response_parse = parsing(request_api)
        if response_parse:
            version_found = get_version(response_parse)
            if version_found:
                response_data = request_api_wpscan(version_found)
                print(response_data)