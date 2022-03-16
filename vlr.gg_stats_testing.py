# --- DEV. NOTES ---
# the stats are saved toa csv file that is best opened in excel
# some of the stats in the CL% column are empty. this means that their CL% is 0%
# need to figure out the different tables for the SQL server

# --- CODE ---

# imports
import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL for vlr.gg page displaying stats table
URL = "https://www.vlr.gg/stats/?event_group_id=all&event_id=799&series_id=1559&subseries_id=all&region=all&country=all&min_rounds=10&min_rating=10&agent=all&map_id=all&timespan=60d"

# creating page object
page = requests.get(URL)

# using lxml to parser through html code to a format python can use
soup = BeautifulSoup(page.text, 'lxml')

# initiating table1 variable to the table of stats from web page
table1 = soup.find("table", class_ = "wf-table mod-stats")

# obtain every title of columns with tag <th>
headers = []
for i in table1.find_all('th'):
    title = i.text
    headers.append(title)

# create a dataframe using pandas
mydata = pd.DataFrame(columns = headers)

# create a for loop to fill dataframe
# finds 'tr' tag for the table
for j in table1.find_all('tr')[1:]:
    # finds 'td' tag which holds data within the table, and sets it to the newly initiated variable row_data
    row_data = j.find_all('td')
    row = [i.text for i in row_data]
    length = len(mydata)
    mydata.loc[length] = row

# drop unneccesary column "Agents"
mydata.drop('Agents', inplace=True, axis=1)

# delete "\n"'s from column "Player"
mydata = mydata.replace(r'\n',' ', regex=True)
mydata = mydata.replace(r'\t',' ', regex=True)
mydata.columns = mydata.columns.str.replace(' ', '')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(mydata)
print('-'*80)

mydata.to_csv('stats_vlr.csv')
