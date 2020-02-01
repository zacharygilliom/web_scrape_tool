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


United_Nations_2017.replace((United_Nations_2017.at[3, 'Rank']), '0', inplace=True)

United_Nations_2017.replace((United_Nations_2017.at[96, 'Rank']), '0', inplace=True)

United_Nations_2017.replace(',', '', inplace=True, regex=True)

United_Nations_2017 = United_Nations_2017[United_Nations_2017['Rank'] != '0']

United_Nations_2017 = United_Nations_2017.astype({'Rank': 'str', 'UN GDP': 'str'}).astype({'Rank': 'int', 'UN GDP': 'int'})


World_Bank_2018.replace((World_Bank_2018.at[1, 'Rank']), '0', inplace=True)

World_Bank_2018.replace(',', '', inplace=True, regex=True)

World_Bank_2018 = World_Bank_2018[World_Bank_2018['Rank'] != '0']

World_Bank_2018 = World_Bank_2018.astype({'Rank': 'str', 'World Bank GDP': 'str'}).astype({'Rank': 'int', 'World Bank GDP': 'int'})


International_Monetary_Fund_2019.replace((International_Monetary_Fund_2019.at[2, 'Rank']), '0', inplace=True)

International_Monetary_Fund_2019.replace(',', '', inplace=True, regex=True)

International_Monetary_Fund_2019 = International_Monetary_Fund_2019[International_Monetary_Fund_2019['Rank'] != '0']

International_Monetary_Fund_2019 = International_Monetary_Fund_2019.astype({'Rank': 'str', 'IMF GDP': 'str'}).astype({'Rank': 'int', 'IMF GDP': 'int'})


plt.subplot(311)
sns.barplot(x=United_Nations_2017[United_Nations_2017['Rank'] < 11]['Country'], y=United_Nations_2017[United_Nations_2017['Rank'] < 11]['UN GDP'])
plt.title('Top Countries by GDP in 2017, 2018, and 2019')


plt.subplot(312)
sns.barplot(x=World_Bank_2018[World_Bank_2018['Rank'] < 11]['Country'], y=World_Bank_2018[World_Bank_2018['Rank'] < 11]['World Bank GDP'])

plt.subplot(313)
sns.barplot(x=International_Monetary_Fund_2019[International_Monetary_Fund_2019['Rank'] < 11]['Country'], 
			y=International_Monetary_Fund_2019[International_Monetary_Fund_2019['Rank'] < 11]['IMF GDP'])

plt.show()
