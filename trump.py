from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import time
import os
import redis

trumpHeaders = []
previousTrumpHeaders = []
print("REDIS URL: "+os.environ.get("REDISTOGO_URL"))
r = redis.from_url(os.environ.get("REDISTOGO_URL"))

page = requests.get("http://vg.no")
soup = BeautifulSoup(page.content, 'html.parser')
headers = soup.find_all(class_="article-content")

previousTrumpHeaders=r.get('trump')
print (previousTrumpHeaders)

for header in headers:
    if "Trump" in str(header):
        trumpHeaders.append(header.getText().strip())
print("trumpHeaders")
print(*trumpHeaders, sep = ", ")
if trumpHeaders != previousTrumpHeaders:
    data = {'text': ",".join(trumpHeaders)}
    postToUrl(os.environ.get("KUNNSKAPSDELING_URL"), data)
    postToUrl(os.environ.get("EKS_CIBER_URL"), data)
    
r.set('trump', trumpHeaders)
print("Soon going to sleep")
print("Prev trump Headers:")
print(*previousTrumpHeaders, sep = ", ")
print("Current trump headers:")
print(*trumpHeaders, sep = ", ")

def postToUrl(url, data):
    response = requests.post(
        url, data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )