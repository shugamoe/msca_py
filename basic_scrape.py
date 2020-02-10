import urllib.request
from bs4 import BeautifulSoup

theurl = "http://www.bloomberg.com/quote/SPX:IND"
thepage = urllib.request.urlopen(theurl)
soup = BeautifulSoup(thepage, 'html.parser')
name_box = soup.find('h1', attrs={'class': 'name'})
name = name_box.text.strip()

print(name)

price_box = soup.find('div', attrs={'class':'price'})
price = price_box.text

print (price)

