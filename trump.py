from bs4 import BeautifulSoup
import requests
page = requests.get("http://vg.no")
soup = BeautifulSoup(page.content, 'html.parser')
headers = soup.find_all("h3")

for header in headers:
   if "Trump" in str(header):
        print(header)