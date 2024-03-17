import argparse
import csv
import requests
import warnings
import pandas as pd
from bs4 import BeautifulSoup

# Suppress FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Scrape data from a webpage table and save it to a CSV file.")
    parser.add_argument('-u', '--url', type=str, help="URL of the webpage containing the table data")
    parser.add_argument('-f', '--filename', type=str, help="Filename for the CSV file to be saved")
    return parser.parse_args()

def scrape_table_to_csv(url):
    # Downloading contents of the web page
    data = requests.get(url).text

    soup = BeautifulSoup(data, 'html.parser')

    # Create a list with the Table
    table = soup.find('table')

    # Defining the dataframe
    df = pd.DataFrame()

    # Check if table is not None
    if table is not None:
        # Extracting column headers
        headers = [header.text.strip() for header in table.find_all('th')]
        # Append column headers as the first row in the DataFrame
        df = df.append({'Data': headers}, ignore_index=True)

        # Collecting Data
        for row in table.find_all('tr'):
            # Find all data for each column
            columns = row.find_all('td')

            # Check if there are columns
            if columns:
                # Collect text from each column
                data_row = [col.text.strip() for col in columns]
                # Append data row to dataframe
                df = df.append({'Data': data_row}, ignore_index=True)

    else:
        print("No table found in the web page.")

    return df

def save_to_csv(df, filename):
    # Clean up the DataFrame
    df['Data'] = df['Data'].apply(lambda x: ', '.join("'" + item + "'" if item else "''" for item in x))

    # Remove unwanted elements from the DataFrame
    df['Data'] = df['Data'].apply(lambda x: x.replace("'', ", "").replace(", ''", ""))

    # Remove specific strings from the second row
    if len(df) > 1:
        df.loc[1, 'Data'] = df.loc[1, 'Data'].replace("'', 'Parent Directory', '', '-', ''", "")

    # Save the cleaned DataFrame to CSV
    df.to_csv(filename, index=False, header=False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    print("CSV file saved successfully.")

def main():
    args = parse_arguments()
    url = args.url
    filename = args.filename

    # Ensure URL and filename are provided
    if not (url and filename):
        print("Error: Both URL and filename are required. Use -h or --help for more information.")
        return

    df = scrape_table_to_csv(url)
    if not df.empty:
        save_to_csv(df, filename)

if __name__ == "__main__":
    main()
