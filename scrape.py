import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests

def scrape(url):
    """Extracts S&P 500 information from a table and returns multiple lists"""
    page = requests.get(url)
    statusCode = page.status_code
    
    if statusCode == 200: 
        soup = BeautifulSoup(page.content, 'html.parser')
        wiki_table = soup.find("table", class_=["wikitable", "sortable", "sticky-header", "jquery-tablesorter"])
        if not wiki_table:
            raise ValueError("Could not find the expected S&P 500 table on the page")
        
        tbody = wiki_table.find("tbody") # Extract the <tbody> from the main table
        if not tbody:
            raise ValueError("No <tbody> found in the table")

        symbol_list = [] 
        name_list = []
        sector_list = []
        subsector_list = []
        headquarter_list = []
        added_list = []
        
        for row in tbody.findAll('tr'): # returns a list
            cells = row.findAll('td') # iterate through each item in the row

            if len(cells) == 8: # check if there are 8 columns in the table
                if cells[0].text.strip() not in symbol_list:
                    symbol_list.append(cells[0].text.strip()) # need to remove leading and trailing whitespace
                    name_list.append(cells[1].text.strip())
                    sector_list.append(cells[2].text.strip())
                    subsector_list.append(cells[3].text.strip())
                    headquarter_list.append(cells[4].text.strip())
                    added_list.append(cells[5].text.strip())
        
        return symbol_list, name_list, sector_list, subsector_list, headquarter_list, added_list

def create_df(symbols, names, sectors, subsectors, hqs, dates):
    """Creates a DataFrame from lists of company data"""

    df = pd.DataFrame({
    "Symbol": symbols,
    "Name": names,
    "Sector": sectors,
    "Subsector": subsectors,
    "Headquarters": hqs,
    "Date Added": dates
    })
    return df

def main():
    link = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    symbols, names, sectors, subsectors, hqs, dates = scrap(link)
    df = create_df(symbols, names, sectors, subsectors, hqs, dates)
    print(df)
    df.to_csv("sp500_companies.csv", index=False)

if __name__ == "__main__":
    main()

