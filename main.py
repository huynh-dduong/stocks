import os
import pandas as pd

# Create dataframe to store all Excel files
df = pd.DataFrame()
df['Symbol'] = ''

# Iterate through each file and 
for xls in os.scandir('stocks'):
    data = pd.read_excel(xls, sheet_name=None)
    concat_data = pd.concat(data.values())
    df = pd.merge(df, concat_data, how='inner', left_on=['Symbol', 'Company Name'], right_on=['Symbol', 'Company Name'])
    
        
df.to_excel(excel_writer='AllSheets.xlsx', sheet_name='Sheet1')
    
