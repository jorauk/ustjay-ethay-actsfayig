import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    """ Returns fact from unkno.com """
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


def pig_latinize(input):
    """
    Takes text from user (input), posts to Pig Latinizer,
    and returns Pig Latin text
    """
    request_url = 'https://hidden-journey-62459.herokuapp.com/piglatinize/'
    post_latin = requests.post(request_url, data={'input_text': input},
        allow_redirects=False)
        
    return post_latin.headers['Location']
    

@app.route('/')
def home():
    fact = get_fact().lstrip()
    latinize = requests.get(pig_latinize(fact))
    
    soup = BeautifulSoup(latinize.content, "html.parser")
    latin_quote = soup.find_all("h2")
    
    return latin_quote[0].nextSibling


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

