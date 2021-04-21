import pandas as pd # for Excel file
from datetime import date
from pandas_datareader import data
import numpy as np
from pathlib import Path
from time import sleep
import streamlit as st
from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.momentum import RSIIndicator

# To run the Streamlit dashboard in your browser,
# execute this in the terminal: 
# streamlit run d:\Dropbox\GIT\AIMmonitor\maincode.py

def displaystreamlit(stockDatacollection):
    # Generate web page

    # hack to adjust sidebar width
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 400px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 400px;
            margin-left: -400px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    option = st.sidebar.selectbox('Select one symbol', ( list(stockDataCollection)))


    df = stockDataCollection[option]

    indicator_bb = BollingerBands(df['Close'])

    bb = df
    bb['bb_h'] = indicator_bb.bollinger_hband()
    bb['bb_l'] = indicator_bb.bollinger_lband()
    bb = bb[['Close','bb_h','bb_l']]

    macd = MACD(df['Close']).macd()

    rsi = RSIIndicator(df['Close']).rsi()
    
    st.title(option)

    st.write('Bollinger Bands')

    st.line_chart(bb)

    progress_bar = st.progress(0)

    # https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py

    st.write('MACD')
    st.area_chart(macd)

    st.write('RSI ')
    st.line_chart(rsi)

    st.write('Recent data ')
    # sets the dates in the right format
    df.index = df.index.strftime('%d-%m-%Y')
    st.dataframe(df.tail(10))

def getData(sym): # this function gets ticker data, and saves/updates pickle
    today = date.today()
    file = "datasets/"+sym

    if Path(file).is_file(): # do we have a saved file of existing price data
        stockData = pd.read_pickle(file)
        try:
            finalDateInFile = stockData.index[-1] # y-axis index is the dates
            #print(stockData.head()) #debug
        except Exception as e:
            print("**** Date error in file for " + sym)
        
        if finalDateInFile < today: 
            # top up the file with the missing data only, to reduce data downloads
            print("Saved data found for " + sym + ", updating to today's date")
            
            try:
                missingData = data.DataReader(sym, start=finalDateInFile, end=today, data_source='yahoo')
            
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
            stockData.to_pickle(file)
            sleep(5) # to prevent yfinance server overload with too many calls
        except Exception as e:
            print("**** Error retrieving data for " + sym)
            #print(e)

    return stockData

if __name__ == "__main__":
    
    symbols = pd.read_csv('datasets/symbols.csv', usecols=[0,1], header=None)
    stockDataCollection = {} # make a dictionary of all the ticker data

    for index, row in symbols.iterrows(): 
        ticker = row[0].strip()
        tickerAndCompany = row.to_string(header=False, index=False)
        tickerAndCompany = tickerAndCompany.split("ORD",1)[0]
        tickerAndCompany = tickerAndCompany.replace("\n",",  ")
        stockDataCollection[tickerAndCompany] = getData(ticker)
                        
        #if index == 2: break # only do the first few for debugging

    print("Update of stock data complete")

    #generate our Streamlit based results site
    displaystreamlit(stockDataCollection)
    
    #p = np.array(data['Date''Close']) # 52-weeks of closing prices
    #closePrice = p[1]
    #slicep = p[1::5].copy() # take every 5th day
    #relativep = (slicep/closePrice)*100 # set as a % of first close