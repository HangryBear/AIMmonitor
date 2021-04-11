from datetime import date
from pandas_datareader import data

today = date.today()
lastYear = date.fromordinal(today.toordinal()-365)

price = data.DataReader("ITM.L", start=lastYear, end=today, data_source='yahoo')

with open('datasets/singleSymbol.csv', 'a') as out_file:
            out_file.write(str(price))