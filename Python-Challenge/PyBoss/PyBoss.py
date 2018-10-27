# list of all US states and two-letter abbrevation as dictionary key
us_state_abbrev = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
}

import pandas as pd
import datetime

df=pd.read_csv('employee_data.csv')
#print(df.head())

#Add new columns for First Name and Last Name
df['First Name'],df['Last Name']=df['Name'].str.split(' ',1).str
#print(df.head())

#Format DOB to %m/%d/%y
# NOT WORKING
#print(type(pd.Timestamp(df['DOB'])))
df['DOB'] = df['DOB'].map('{:.%m/%d/%y}'.format)
#print(df['DOB'].head())

#Replace first 5 number of SSN to *
df['SSN']= '***-**' + df['SSN'].str[6:]
#print(df.head()) 

#Replace State Name with two-letter code
#Define a generic function using Pandas replace function
def coding(col, codeDict):
  colCoded = pd.Series(col, copy=True)
  for key, value in codeDict.items():
    colCoded.replace(value, key, inplace=True)
  return colCoded

df['State']=coding(df['State'],us_state_abbrev)
#print(df.head())

#Reorder the Data Frame
#Emp ID,First Name,Last Name,DOB,SSN,State
df=df[['Emp ID','First Name','Last Name','DOB','SSN','State']]
print(df.head())

#write to csv
df.to_csv('output.csv',header=True, index=True)