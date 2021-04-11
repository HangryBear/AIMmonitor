import pandas as pd # for Excel file
from datetime import date
from pandas_datareader import data
import numpy as np
from pathlib import Path
from time import sleep


# TODO
# seems to get overloaded if you apply calls too quickly

def getData(sym):
    today = date.today()
    file = "datasets/"+sym

    if Path(file).is_file(): # do we have a saved file of existing price data
        stockData = pd.read_pickle(file)
        if 'Date' not in stockData.columns:
            stockData = stockData.reset_index() # this is necessary to convert 'Date' from the row index to a standard column
        try:
            finalDateInFile = stockData.iloc[-1]["Date"]
        except Exception as e:
            print("**** Date error in file for " + sym)
        

        if finalDateInFile < today: 
            # top up the file with the missing data only, to reduce data downloads
            print("Saved data found for " + sym + ", updating to today's date")
            missingData = data.DataReader(sym, start=finalDateInFile, end=today, data_source='yahoo')
            missingData = missingData.reset_index() # this is necessary to convert 'Date' from the row index to a standard column
        
            try:
                stockData = stockData.append(missingData)
                stockData.to_pickle(file)
            except:
                print("**** Error retrieving data for " + sym)
        else:
            print("Up to date saved data found for " + sym)
            
 
    else: # no saved file of data, so download the whole lot
        print("No saved data found for " + sym + ", downloading and saving")
            
        firstDate = date.fromordinal(today.toordinal()-365)
        try:
            stockData = data.DataReader(sym, start=firstDate, end=today, data_source='yahoo')
            stockData = stockData.reset_index() # this is necessary to convert 'Date' from the row index to a standard column
            stockData.to_pickle(file)
            sleep(5) # to prevent yfinance server overload by too many calls
        except Exception as e:
            print("**** Error retrieving data for " + sym)
            #print(e)
        
    # for debugging, print latest 5 days worth of data
    # print(stockData.tail())

    #p = np.array(data['Date''Close']) # 52-weeks of closing prices
    #closePrice = p[1]
    #slicep = p[1::5].copy() # take every 5th day
    #relativep = (slicep/closePrice)*100 # set as a % of first close
    return stockData

if __name__ == "__main__":
    
    symbols = pd.read_csv('datasets/symbols.csv', usecols=[0,1], header=None)

    for index, row in symbols.iterrows(): 
        ticker = row[0].strip()
        
        # add all to same dataframe, then save in 1 go.
        if index==0:
            stockData = getData(ticker) # Get the current price information of this stock
        else:
            stockData = stockData.append(getData(ticker))
                
        # For debugging only
        #if index ==2: 
        #    stockData.to_clipboard()
        #    break # only do the first few for debugging

    print("Writing all data to datasets/output.xlsx")
    stockData.to_excel('datasets/output.xlsx')