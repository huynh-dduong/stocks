# E-Trade Stocks Analysis

## Introduction
I use the E-Trade app to buy and trade stocks. And when I'm on the hunt for a new stock, I go through the Stock Screener and start searching there. But one of the major problems with this is how overwelming it can be, there are a variety of filters that can be applied such as specific stock exchanges, different market caps for a company, its percentage performance on given weeks, and many more. Even after filtering my selections, I have to scrub through pages of garbled numbers with no easy viewing of what's a good stock which makes me want to bang my head on the wall.

So I want to create something that will be able to extract all the raw data from various stock markets, transform the data into a aggregated spreadsheet, and visualize the data in Tableau to provide better insights and determine a stock I am willing to invest in.

## Laying Down the Foundation
As stated I'm going to use E-Trade's database to extract the raw data for later uses. The stock markets I'm interested in are the NASDAQ, NYSE, S&P 400, S&P 500, and S&P 600. Extracting all the data from each file, I go to the E-Trade website and log-in. Then I go to the Market & Ideas Tab > Stocks > Stock Screener.

![Image instructions of how to access stock screener](images\stockscreener.png)

Next, I select one stock market as selecting multiple exchanges filters stocks available in selected filters and click "view results".

![Image instructions of how to filter stocks using stock screener](images\stockscreenerfilter.png)

Finally, I clicked on "Export to Excel".

![Image instructions of how to filter stocks using stock screener](images\stockscreenerexport.PNG)