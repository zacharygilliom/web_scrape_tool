from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

def strip_val(val):
	val[1] = val[1].replace('\xa0', '')
	return val

# Website that we want to pull data from.
website_url = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita').text

# Decided to go with lxml for parser.
soup = BeautifulSoup(website_url, 'lxml')

# Only 3 tables on the page.
my_table = soup.findAll('table', {'class':'wikitable sortable'})
data = []
# Want to loop through every table and pull out the data..
for table in my_table:
	tbl = table.tbody
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

# Creating all three of the dataframe 
International_Monetary_Fund_2019 = pd.DataFrame(columns=['Rank', 'Country', 'IMF GDP 2019'], data=International_Monetary_Fund_2019_data)

World_Bank_2018 = pd.DataFrame(columns=['Rank', 'Country', 'World Bank GDP 2018'], data=World_Bank_2018_data)

United_Nations_2017 = pd.DataFrame(columns=['Rank', 'Country', 'UN GDP 2017'], data=United_Nations_2017_data)

# Biggest issue is that some of the "Countries" are not actual countries so the rank value is a hypen. Dropping Duplicates, dropping hyphens specifically,
# and dropping the value with .loc did not actually drop all hyphens.  Was able to find that two of the indices had the values that were duplicated.
United_Nations_2017.replace((United_Nations_2017.at[3, 'Rank']), '0', inplace=True)
United_Nations_2017.replace((United_Nations_2017.at[96, 'Rank']), '0', inplace=True)
United_Nations_2017.replace(',', '', inplace=True, regex=True)
United_Nations_2017 = United_Nations_2017[United_Nations_2017['Rank'] != '0']
United_Nations_2017 = United_Nations_2017.astype({'Rank': 'str', 'UN GDP 2017': 'str'}).astype({'Rank': 'int', 'UN GDP 2017': 'int'})

# all three datasets had different locations of the hyphens that were difficult to eliminate.  So we have to go through each dataframe individually.
World_Bank_2018.replace((World_Bank_2018.at[1, 'Rank']), '0', inplace=True)
World_Bank_2018.replace(',', '', inplace=True, regex=True)
World_Bank_2018 = World_Bank_2018[World_Bank_2018['Rank'] != '0']
World_Bank_2018 = World_Bank_2018.astype({'Rank': 'str', 'World Bank GDP 2018': 'str'}).astype({'Rank': 'int', 'World Bank GDP 2018': 'int'})


International_Monetary_Fund_2019.replace((International_Monetary_Fund_2019.at[2, 'Rank']), '0', inplace=True)
International_Monetary_Fund_2019.replace(',', '', inplace=True, regex=True)
International_Monetary_Fund_2019 = International_Monetary_Fund_2019[International_Monetary_Fund_2019['Rank'] != '0']
International_Monetary_Fund_2019 = International_Monetary_Fund_2019.astype({'Rank': 'str', 'IMF GDP 2019': 'str'}).astype({'Rank': 'int', 'IMF GDP 2019': 'int'})

# In order to better visualize our data, we want to combine all three dataframes.  So we go one at a time.  df.Merge creates columns
# from the other dataframes so we also want to drop the extra columns at the end.
combined_data = International_Monetary_Fund_2019.merge(World_Bank_2018, on='Country')
combined_data = combined_data.merge(United_Nations_2017, on='Country')
combined_data.drop(['Rank_y', 'Rank'], axis=1, inplace=True)

# now we want to take the combined data and use melt function so that we can get our 3 values into one columns for better visuals.
combined_long_data = pd.melt(combined_data, id_vars = ['Country'], value_vars = ['IMF GDP 2019', 'World Bank GDP 2018', 'UN GDP 2017'])
combined_long_data = combined_long_data[combined_long_data['value'] > 50000]


# Finally we want to use a barplot as it will help explain the data better.
sns.barplot(x='Country', y='value', hue='variable', data=combined_long_data)
plt.show()

