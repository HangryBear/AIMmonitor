# importing the libraries
from bs4 import BeautifulSoup
import requests
import csv

headings = []

for page in range(1, 7):

    url="https://www.londonstockexchange.com/indices/ftse-aim-100-index/constituents/table?page="+str(page)
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    symbolTable = soup.find("table", attrs={"class": "full-width ftse-index-table-table"})
    symbolTableData = symbolTable.tbody.find_all("tr")  # contains 2 rows

    rowData = ""

    for row in symbolTableData:
        first = True
        for element in row.find_all("td"):
            if first:
                rowData = (element.text).replace(',', '') # strip commas from numbers
                first = False
            else:
                rowData = rowData + "," + (element.text).replace(',', '') # strip commas from numbers
                break # uncomment if you don't just want the first 2 columns
        headings.append(rowData)
        rowData = ""

#print(headings)
 
with open('datasets/symbols.csv','w',newline='\n') as file:

    
    # Upload as open project on Github

    for heading in sorted(headings):
        file.write(heading+"\n")