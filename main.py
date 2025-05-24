import os
import pandas as pd
from functools import reduce

df = pd.DataFrame()
data = [None] * 5

# Iterate though each file in stocks folder
for xls in os.scandir('stocks'):
    # Put each Excel sheet into data array
    for i in range(5):
        data[i] = (pd.read_excel(xls, sheet_name=i))
    # Merge all indexes in data array based on Symbol and Company Name into one dataframe
    df = reduce(lambda left, right: pd.merge(left, right, on=['Symbol', 'Company Name'], how='inner'), data)

    # Write the dataframe into AllSheets.xlsx. If the sheet exists, replace. Else append with the name of the stock market file name
    with pd.ExcelWriter('AllSheets.xlsx', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=str(xls.name))
        


