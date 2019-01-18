from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import time
import os
import redis

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

trumpHeaders = []
previousTrumpHeaders = []
r = redis.from_url(os.environ.get("REDISTOGO_URL"))

page = requests.get("http://vg.no")
soup = BeautifulSoup(page.content, 'html.parser')
headers = soup.find_all(class_="article-content")

previousTrumpHeaders = r.get('trump')

#print("previous:" + previousTrumpHeaders)
if previousTrumpHeaders is not None:
    previousTrumpHeaders = previousTrumpHeaders.decode('unicode-escape').encode('latin1').decode('utf-8').replace('"','')
print ("tidligere header: "+previousTrumpHeaders)

for header in headers:
    if "Trump" in str(header):
        trumpHeaders.append(header.getText().strip())
        url = header.findAll('a')[0]
        if url is not None:
            print(url.getText())
print("nåværende trumpHeaders:")
trumpString = '-'.join(trumpHeaders)
print(trumpString)
if trumpString != previousTrumpHeaders:
    print("Ny(e) overskrift(er) funnet")
    data = {'text': ",".join(trumpHeaders)}
    postToUrl(os.environ.get("KUNNSKAPSDELING_URL"), data)
    postToUrl(os.environ.get("EKS_CIBER_URL"), data)
    #serialize
r.set('trump', json.dumps(trumpString, ensure_ascii=False).encode('utf8'))