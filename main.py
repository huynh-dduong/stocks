import os
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.DataFrame()
data = [None] * 5

# Iterate though each file in stocks folder
for xls in os.scandir('stocks'):
    # Put each Excel sheet into data array
    for i in range(5):
        data[i] = (pd.read_excel(xls, sheet_name=i))
    # Merge all indexes in data array based on Symbol and Company Name into one dataframe
    df = reduce(lambda left, right: pd.merge(left, right, on=['Symbol', 'Company Name'], how='inner'), data)
    
    # Drop and clean up columns I don't need to view
    df = df.drop(columns=['Mkt Cap','Thomson Reuters Consensus', '5 Day Chg_y', '4 Week Chg_y', 'Beta', 'PEG Ratio'])
    # print(df)
    
    # value_counts prints the occurances of each analyst opinion to replace later.
    industy_count = df['Industry'].value_counts()    
    # print(industy_count)
    
    refinitiv_count = df['Refinitiv'].value_counts()
    # print(refinitiv_count)
    
    argus_a_count = df['Argus Analyst'].value_counts()    
    # print(argus_a_count)
    
    argus_a6_count = df['Argus A6 Quantitative'].value_counts()
    # print(argus_a6_count) 
    
    market_edge_count = df['MarketEdge'].value_counts()
    # print(market_edge_count)
    
    morgan_count = df['Morgan Stanley'].value_counts()
    # print(morgan_count)
    
    smart_count = df['SmartConsensus'].value_counts()
    # print(smart_count)
    
    tiprank_analyst_count = df['TipRanks Analyst Consensus'].value_counts()
    # print(tiprank_analyst_count)
    
    tiprank_blogger_count = df['TipRanks Blogger Sentiment'].value_counts()
    # print(tiprank_blogger_count)
    
    # Replacing analyst opinions to a -1 to 1 scale, with -1 suggest negative opinion of stock and 1 suggest positive opinion of stock
    df['Refinitiv'].replace(['Neutral', 'Positive', 'Negative', '--'], [0, 1, -1, 0], inplace=True)
    df['Argus Analyst'].replace(['--', 'Buy', 'Hold', 'Sell'], [0, 1, 0, -1], inplace=True)
    df['Argus A6 Quantitative'].replace(['BUY', 'HOLD', 'SELL'], [1, 0, -1], inplace=True)
    df['MarketEdge'].replace(['Long', 'Neutral From Avoid', 'Avoid', 'NC', 'Neutral From Long'], [1, 0.5, -1, 0, -0.5], inplace=True)
    df['Morgan Stanley'].replace(['Equalweight', 'Underweight', 'Overweight', '--'], [0, -1, 1, 0], inplace=True)
    df['SmartConsensus'].replace(['Hold', 'Buy', 'Sell', 'Drop'], [0, 1, -1, -0.5], inplace=True)
    df['TipRanks Analyst Consensus'].replace(['Moderate Buy', 'Strong Buy', 'Hold', 'Moderate Sell', 'Strong Sell'], [0.5, 1, 0, -0.5, -1], inplace=True)
    df['TipRanks Blogger Sentiment'].replace(['Bullish', 'Neutral', 'Bearish'], [1, 0, -1], inplace=True)
    
    df_col_list = ['Refinitiv', 'Argus Analyst', 'Argus A6 Quantitative', 'MarketEdge', 'Morgan Stanley', 'SmartConsensus', 'TipRanks Analyst Consensus', 'TipRanks Blogger Sentiment']
    
    # Get the sum of analyst opinions to see overall views. -8 would suggest not viewing, and 8 would strongly suggest viewing
    df['Analyst Opinion Sum'] = df[df_col_list].sum(axis=1)
    
    # Creates histogram of number of stocks in each industy -- can indicate stocks better to look at in the market.
    df['Industry'].value_counts().plot(kind='bar')
    plt.xlabel('Industy')
    plt.ylabel('Count')
    plt.title('Count of Stocks by Industy')
    # plt.show()
    
    file_name = "output/" + str(xls)[11:-6] + ".csv"
    df.to_csv(file_name, encoding='utf-8', index=False)
    

    
# Write the dataframe into AllSheets.xlsx. If the sheet exists, replace. Else append with the name of the stock market file name
# with pd.ExcelWriter('AllSheets.xlsx', mode='a', if_sheet_exists='replace') as writer:
#     df.to_excel(writer, sheet_name=str(xls.name))


    


