from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import time

webhook_url = 'https://hooks.slack.com/services/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'
trumpHeaders = []
previousTrumpHeaders = []

while True:
    page = requests.get("http://vg.no")
    soup = BeautifulSoup(page.content, 'html.parser')
    headers = soup.find_all(class_="article-content")
    
    for header in headers:
        if "Trump" in str(header):
            trumpHeaders.append(header.getText().strip())
    print("trumpHeaders")
    print(*trumpHeaders, sep = ", ")
    if trumpHeaders != previousTrumpHeaders:
        slack_data = {'text': ",".join(trumpHeaders)}
        response = requests.post(
            webhook_url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
    previousTrumpHeaders = trumpHeaders
    trumpHeaders = []
    print("Soon going to sleep")
    print("Prev trump Headers:")
    print(*previousTrumpHeaders, sep = ", ")
    print("Current trump headers:")
    print(*trumpHeaders, sep = ", ")
    time.sleep(60)