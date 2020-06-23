from bs4 import BeautifulSoup
from requests import get
import pandas as pd 

pages, prices, stars, titles, urlss, pages_to_scrape = [], [], [], [], [], 1



for p in range(1, pages_to_scrape + 1):
	url = "http://books.toscrape.com/catalogue/page-{}.html".format(p)
	pages.append(url)

for url in pages:
	html = get(url)
	bs = BeautifulSoup(html.text, "html.parser")

	for h in bs.findAll("h3"):
		title = h.getText()
		titles.append(title)
	
	for p in bs.findAll("p", class_="price_color"):
		price = p.getText()
		prices.append(price)
	
	for p in bs.findAll("p", class_="star-rating"):
		for k,v in p.attrs.items():
			star = v[1]
			stars.append(star)
	img_container = bs.findAll("div", class_="image_container")
	
	for thumbs in img_container:
		img = thumbs.find("img", class_="thumbnail")
		url = "http://books.toscrape.com/" + str(img["src"])
		nurl = url.replace("../", "")
		urlss.append(nurl)

data = {'Title': titles, 'Prices': prices, 'Stars':stars, "URLs":urlss}
df = pd.DataFrame(data=data)
df.index += 1
df.to_excel("./output.xlsx")
