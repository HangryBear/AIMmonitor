# AIMmonitor

# maincode.py
Uses a provided set of symbols (use ScrapeSymbols.py to generate/update symbols.csv (in ./dataset)), and downloads the last 1 year's worth of OHLC data for each symbol (pickling each one to its own file in ./dataset). 

To minimise the number of calls to Yahoo Finance, once the data's been completely downloaded once, the script will only download and update any data for new dates. 

This script is a work in progress, and at this time it only concatenates all the OHLC data for all symbols into one Excel file (./datasets/output.xlsx).

Future plans are to:
1. perform stock screening operations 
2. display company names, tables and graphs in Streamlit
3. email a daily update
4. check my portfolio performance

# ScrapeSymbols.py
Scrapes AIM 100 symbol / stock ticker list from LSE website to ./datasets/symbols.csv file. You should only need to run this script once to begin with, then periodically if any symbols have changed on the index. 

This script can easily be modified to scrape any other symbols lists. If you use this script, please be curteous by only running it very infrequently. This repo contains a relatively up to date symbols.csv in ./dataset, so if you are happy with that, there is no need to run this script at all.

# SingleStockDownloader.py
Saves one symbol to ./datasets/singleSymbol.csv, this shows you exactly what's in the Yahoo Finance Dataframe, which you may find handy for development purposes. 
