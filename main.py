from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

def strip_val(val):
	val[1] = val[1].replace('\xa0', '')
	return val

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
		val = val.split('\n')
		val = val[1:-1]
		val = strip_val(val)
		rows.append(val)
	data.append(rows)	

International_Monetary_Fund_2019_data = data[0]
World_Bank_2018_data = data[1]
United_Nations_2017_data = data[2]


International_Monetary_Fund_2019 = pd.DataFrame(columns=['Rank', 'Country', 'IMF GDP'], data=International_Monetary_Fund_2019_data)

World_Bank_2018 = pd.DataFrame(columns=['Rank', 'Country', 'World Bank GDP'], data=World_Bank_2018_data)

United_Nations_2017 = pd.DataFrame(columns=['Rank', 'Country', 'UN GDP'], data=United_Nations_2017_data)

# United_Nations_2017['Rank'] = United_Nations_2017['Rank'].replace('-', 0)

United_Nations_2017.drop_duplicates('Rank', inplace=True)

United_Nations_2017.drop(3, inplace=True)
United_Nations_2017.drop(96, inplace=True)


United_Nations_2017 = United_Nations_2017.astype({'Rank': 'str', 'UN GDP': 'str'}).astype({'Rank':'int'})

print(United_Nations_2017.dtypes)

for index, row in United_Nations_2017.iterrows():
	United_Nations_2017.loc[index, 'UN GDP'] = row['UN GDP'].replace(',', '')
	# print(row['UN GDP'])

United_Nations_2017 = United_Nations_2017.astype({'UN GDP': 'int'})
# print(United_Nations_2017)
# print(United_Nations_2017.dtypes)


# print(International_Monetary_Fund_2019_data)
# print(International_Monetary_Fund_2019)
# print(World_Bank_2018)
# print(United_Nations_2017)

plt.subplot(311)
sns.lineplot(x=United_Nations_2017[United_Nations_2017['Rank'] < 11]['Country'], y=United_Nations_2017[United_Nations_2017['Rank'] < 11]['UN GDP'])

plt.show()
