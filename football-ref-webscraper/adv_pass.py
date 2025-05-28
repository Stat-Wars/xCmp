import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sys

def fetch_adv_passing_rows(year: int):
    """
    Return all <tr> elements #passing_advanced table
    for a given season on Pro-Football-Reference. Advanced passing only available 2018 and on. 
    """
    url = f"https://www.pro-football-reference.com/years/{year}/passing_advanced.htm"
    response = requests.get(url)
    response.raise_for_status()  # throws error for bad status

    # get table body
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': "passing_advanced"})
    if not table:
        raise ValueError(f"Advanced passing table could not be found for year {year}")
    tbody = table.find('tbody')
    if not tbody:
        raise ValueError(f"No tbody found in 'passing_advanced' table for year {year}")
    
    rows = tbody.find_all("tr")

    # filter data rows
    data_rows = [
        row for row in rows 
        if not row.get('class') or not any(cls in ['thead', 'norank', 'over_header'] for cls in row.get('class'))
    ]
    
    return data_rows

def parse_rows_to_df(rows):
    """
    Parse all <tr> elements and compile the data into a dataframe
    """
    parsed_data = []
    cols = [] #keeping track of each column name for the df

    for row in rows:
        row_data = {}
        tds = row.find_all("td")

        for td in tds:
            col_name = td.get("data-stat")
            if not col_name or col_name == "awards":
                continue
            
            value = td.get_text(strip=True)
            row_data[col_name] = value if value != "" else np.nan

            if col_name not in cols:
                cols.append(col_name)

        parsed_data.append(row_data)
    
    df = pd.DataFrame(parsed_data)
    df = df.reindex(columns=cols) # apply preserved column order from the parsed table
    return df
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", "-y", type=int, default=2024)

    args = parser.parse_args()

    try:    
        trows = fetch_adv_passing_rows(args.year)
        df = parse_rows_to_df(trows)
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)
    
    print(f"Extracted DataFrame with shape: {df.shape}")

    fname = f"./tables/adv_passing/passing_adv_{args.year}.csv"
    df.to_csv(fname, index=False)

    print(df.head())
    print(f"Saved CSV to: {fname}")