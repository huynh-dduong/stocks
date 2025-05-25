import os
import pandas as pd
from functools import reduce

df = pd.DataFrame()
data = [None] * 5
excel_file_name = str(pd.Timestamp.now().date()) + "_AllSheets.xlsx"
df.to_excel(excel_file_name, sheet_name="master")

# Iterate though each file in stocks folder
for xls in os.scandir('stocks'):
    # Put each Excel sheet into data array to later merge into one dataframe
    for i in range(5):
        data[i] = (pd.read_excel(xls, sheet_name=i))
        
    # Merge all sheets in data array based on Symbol and Company Name into one dataframe
    df = reduce(lambda left, right: pd.merge(left, right, on=['Symbol', 'Company Name'], how='inner'), data)
    
    # Drop and clean up columns I don't need to view
    df = df.drop(columns=['Mkt Cap','Thomson Reuters Consensus', '5 Day Chg_y', '4 Week Chg_y', 'Beta', 'PEG Ratio'])
    
    # Replacing analyst opinions to a -1 to 1 scale, with -1 suggest negative opinion of stock and 1 suggest positive opinion of stock
    # for EDA process later
    netrual_keywords = ['Neutral', '--', 'Hold', 'HOLD', 'NC', 'Hold', 'Neutral', 'Equalweight', None]
    semi_postive_keywords = ['Moderate Buy', 'Neutral From Avoid']
    semi_negative_keywords = ['Moderate Sell', 'Neutral From Long']
    positive_keywords = ['Positive', 'Buy', 'BUY', 'Long', 'Strong Buy', 'Bullish', 'Overweight']
    negative_keywords = ['Negative', 'Sell', 'SELL', 'Avoid', 'Drop', 'Strong Sell', 'Bearish', 'Underweight']
        
    columns = ['Refinitiv', 'Argus Analyst', 'Argus A6 Quantitative', 'MarketEdge', 'Morgan Stanley', 'SmartConsensus', 'TipRanks Analyst Consensus', 'TipRanks Blogger Sentiment']
    
    for col in columns:
        df.loc[df[col].isin(negative_keywords), [col]] = -1
        df.loc[df[col].isin(semi_negative_keywords), [col]] = -0.5
        df.loc[df[col].isin(netrual_keywords), [col]] = 0
        df.loc[df[col].isin(semi_postive_keywords), [col]] = 0.5
        df.loc[df[col].isin(positive_keywords), [col]] = 1
        
    # Lines will write a excel file with all stock exchanges in one area for Excel EDA, and a CSV file
    # For exporting to a SQL database and Tableau visualization dashboard
    with pd.ExcelWriter(excel_file_name, mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=str(xls.name))
        
    file_name = "output/" + str(xls)[11:-6] + ".csv"
    df.to_csv(file_name, encoding='utf-8', index=False)