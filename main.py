from bs4 import BeautifulSoup
import requests
import pandas as pd

website_url = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita').text

soup = BeautifulSoup(website_url, 'lxml')
# print(soup.prettify())

my_table = soup.findAll('table', {'class':'wikitable sortable'})
data = []
for table in my_table:
	tbl = table.tbody
	# print(table)
	links = tbl.findAll('tr')
	rows = []
	for i in range(1, len(links)):
		val = links[i].text
		val = val.replace('\n', ',')
		val = val.replace('\xa0', '')
		val = [val[1:-1]]
		rows.append(val)
	data.append(rows)	

International_Monetary_Fund_2019_data = data[0]
World_Bank_2018_data = data[1]
United_Nations_2017_data = data[2]

International_Monetary_Fund_2019 = pd.DataFrame(columns=['Rank', 'Country', 'GDP'])

print(International_Monetary_Fund_2019)


