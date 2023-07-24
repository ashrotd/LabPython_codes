import requests
from bs4 import BeautifulSoup

page = requests.get('https://aviationweather.gov/metar/data?ids=KUNI&format=raw&hours=24&taf=off&layout=on')
soup = BeautifulSoup(page.content,'html.parser')
links = soup.select("code")
first10 = links[:]
for anchor in first10:
    print(anchor.text)