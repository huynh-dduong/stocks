# E-Trade Stocks Analysis

Link to the [Excel Sheet](https://1drv.ms/x/c/e8bcccfd5234146a/Eb-o4kryEP5OtBb0URLPp4AB1EWPfmx-RLEpvMM6aii5TA?e=SnPXXd)

## Table of Contents

[Introduction](#introduction)

[Exploratory Data Analysis](#exploratory-data-analysis)

[Visualizations and Key Findings](#visualizations-and-key-findings)

[Conclusion](#conclusion)

## Introduction
I use the E-Trade app to buy and trade stocks. When I search for a new stock, I begin by using E-Trade's stock searcher. But I am immediately overwhelmed seeing all the search filters, ranging from different stock exchanges to levels of market cap. Even after filtering my selections, I have to scrub through pages drowning in various numbers with no way of knowing what is a good stock.

### Problem
As stated, I want to solve the issue of finding a reliable and profitable stock utilizing Python Pandas and Excel's Analyzing Tools. What's valuable about solving the problem is reducing the amount of time needed to choose an impressive stock. Another value for solving the problem is making the searching process more intuitive by visualizing the data to give better insights to people.

### Outlined Methods
I will be using Python Pandas to aggregate all the data from E-Trade within the NASDAQ, NYSE, S&P 400, S&P 500, and S&P 600. Then I will use Pandas to clean up and transform the data to make visualization easier.

I'm using Excel Pivot Tables and Pivot Charts to filter and visualize specific parts of my data to provide better insights. 

### Data-Related Issues
Some issues I can see now are the lack of timeframes E-Trade provides, which limits the amount of pivot charts I can use to convey any ideas. Otherwise, choosing the best features to provide insights might pose a challenge, as there are 3000+ stocks I am analyzing, which will cause a lot of noise and skew my choices.

## Exploratory Data Analysis
These are the libraries I will be importing:  
- The os library is used to scan the folders and grab the files of each stock exchange.
- The pandas library will allow analysis and aggregation of the data.
- The reduce library will aid in aggregation.

```
import os
import pandas as pd
from functools import reduce
```

First, initialize the variables. From top to bottom:
- df is an empty dataframe that will house all of the data together.
- Data is a tmp variable holding data from each E-Trade page, as the site separates information such as analyst opinions, balance sheets, and overall summaries.
- excel_file_name is a quality of life variable that will differentiate if the code is run on different days.
- df.to_excel will create an empty Excel file for the data to export.
```
df = pd.DataFrame()

data = [None] * 5

excel_file_name = str(pd.Timestamp.now().date()) + "_AllSheets.xlsx"

df.to_excel(excel_file_name, sheet_name="master")
```
This will scan through a folder; I named mine 'stocks' for this project. Then iterate through each file and assign it to the data array for later extraction.

```
for xls in os.scandir('stocks'):
    for i in range(5):
        data[i] = (pd.read_excel(xls, sheet_name=i))
```
To aggregate all the separate pages into a master spreadsheet, calling reduce on the data array will take two files and combine them based on their Symbol and Company Name to prevent any misalignments.
```
    df = reduce(lambda left, right: pd.merge(left, right, on=['Symbol', 'Company Name'], how='inner'), data)
```
This drops the uncessessary columns from the database for cleaning
```
    df = df.drop(columns=['Mkt Cap','Thomson Reuters Consensus', '5 Day Chg_y', '4 Week Chg_y', 'Beta', 'PEG Ratio'])
```
Since the analyst opinions are keywords, I decided to convert them as values for easier data visualization. I started by identifying all the keywords and categorizing them from negative to positive. Then assign a variable for all the columns that need to be updated. Finally, I iterated through every column and updated each value appropriately.

**_NOTE:_** On the analyst scale, -1 suggest a negative opinion of a stock and 1 suggest a positive opinion. 0 indicate either a neutral stance or opnion was not found for a stock.

```
    netrual_keywords = ['Neutral', '--', 'Hold', 'HOLD', 'NC', 'Hold', 'Neutral', 'Equalweight', '']
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
```

Some cells in the table contain percentages or ratios, which will hurt the data visualization process. So I identified and categorized columns that have a '%' or 'x' character in the string to remove. And finally, rename each column to include an indicator of whether it was a ratio or percentage.

```
    percent_col = ['5 Day Chg_x', '4 Week Chg_x', '52 Week Chg', 'Vs. S&P 500 4 Weeks', 'Vs. S&P 500 13 Weeks', 'Vs. S&P 500 52 Weeks',
                   'Return on Equity',	'Return on Assets',	'EPS Growth CFY*',	'EPS Growth NFY*',	'Revenue Growth CFY*',
                   'Revenue Growth NFY*',	'Dividend Yield',	'Dividend Growth 5 Year']
    ratio_col = ['P/E Ratio (TTM)*',	'Price/Sales Ratio',	'Price/Book Ratio',	'Price/Cash Flow',	'Debt to Capital']
        
    for col in percent_col:
        df[col] = df[col].replace({'%': ''}, regex=True)
        df = df.rename(columns={str(col): str(col) + " by %"})

    for col in ratio_col:
        df[col] = df[col].replace({'x': ''}, regex=True)
        df = df.rename(columns={str(col): str(col) + " by x"})
```
These lines of code will export to Excel and CSV if the data is intended to be imported to SQL or Tableau. The ExcelWriter gets the name of the empty Excel file initially created and appends all the data if the tab doesn't exist. If the tab exists, replace the existing data if the code ran multiple times in a day.

```
    with pd.ExcelWriter(excel_file_name, mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=str(xls.name))
        
    file_name = "output/" + str(xls)[11:-6] + ".csv"
    df.to_csv(file_name, encoding='utf-8', index=False)
```

## Visualizations and Key Findings
This chart shows the industry's performance against the S&P 500. I also filtered it by the top 10 most populated industries, as the lesser populated could produce outliers that would catapult it as one of the best.

We can see that fintech, aerospace, electrical utilities, healthcare, banking, and tech have the best 52-week averages of performance against the S&P 500. Given the current events, many of their 13-week averages aren't performing as well. But fintech is the top among the two. So I'll choose to explore that sector more.

![Industry Performance against the S&P500](/images/industry_performance_vsp500.png)

This chart analyzes the industry's average price performance. Again, I filtered the chart by top populated industries to limit outliers. And we can see healthcare, telecommunications, communications, and pharma are the top for best price performance, but recently most of them are down. This might suggest a good time to look into these sectors to find stocks at a low to hold when higher. But I'm more inclined to look at the positive 4-week averages, as they can suggest stability among a sector for safer bets. Again, I'll pick the fintech industry, as it has positive averages from the past month and year.

![Industry Price Performance](/images/industry_price_performance.png)

Now looking at the fintech industry, I filtered by the top 10 best analyst sums, as analyst insights can suggest more stable and profitable stocks. I also added a dividends and close prices label to have a price range so it's not always Google or Apple that beats the rest out. Looking at it, I find FIS has a positive analyst opinion, affordable pricing, and a solid dividend.

![Average Analyst Opinion of a Stock](/images/analyst_opinion_stock.png)

After searching through the sector and a favorably rated stock within my price range, I want to look at the cash flow and debt of the stock. These two are indicators of how healthy the company is. Typically, higher cash flow to debt ratios indicates less profit, as more is covered by debts. Understanding this point, FIS's calculated debt-to-cash flow is 23.8%, indicating a healthy remainder after debts, reinforcing the quality of the stock.

![Cash Flow and Debt by a Stock](/images/cashflow_debt_stock.png)

Along with seeing the company's debts, understanding the company's earnings is important too. The chart shows price-per-earning and earnings-per-share, which show company profitability. The chart shows the top ten earnings per share within the fintech industry. Seeing how INTU, RKT, and FIS are the best rated. Looking closer, though, we can see RKT, with a massive P/E, is a smaller company, which massively inflates the result. And again, INTU is simply out of my price range. So based on all of these charts, FIS is the best choice for me given all the charts.


![Price per Earning and Earning Per Share this Year](/images/PE_EPS_Stock.png)

## Conclusion

### Key Findings
Some key findings are that, given the data, I was able to produce competent pivot charts that provided insight on the best stock based on the performance, price, earnings, and debt. The result will personally help me find a sound stock when searching again. But others can utilize this process to target specific industries and stocks that would save time and energy researching extensively.

### Deployment
It is important to regulate and provide more data over time for the ability to produce trend lines and provide even better insights that would reduce outliers. With this in mind, being able to automate the process from web scraping to running scripts for analysis would improve the quality of life. However, remember that over-reliance on the process is dangerous, so continuous human review to make sure the data is correct is appropriate.

### Improvements
As stated previously, one noticeable improvement is automating the process more. Creating schedules to web scrape and utilizing Excel VBA to analyze the data would add a lot more quality of life. Another is data; having the ability to see the data over time would provide better insights, as it can target the outliers and yield better results.

## What Have I Learned
Removing myself from the project as a data analyst, I have learned a lot about Python web scraping and cleaning. I also learned more about Excel's pivot charts and formulas such as IFERROR and XLOOKUP. 

More importantly, I gained more experience on what I needed to look out for as a data analyst. I've done this type of analysis looking at stocks based on the criteria I set out. But making it intuitive for others was the difficult part. Being able to explain it so anyone with no prior knowledge can make a confident decision is challenging. Now, as I continue to work on these projects and gain experience, I will question more as a data analyst how the data itself affects the business and the problem I'm trying to solve.
