'''Title: Web Scraping and Data Management Mini Project Documentation

Description:
This Python script performs web scraping to extract information about countries' GDP from a website.
The extracted data is stored in a Pandas DataFrame, and users can interactively perform CRUD operations
(Create, Read, Update, Delete) on the data.

Requirements:
- Python 3.x
- requests
- BeautifulSoup
- pandas

Usage:
1. Ensure that the required libraries are installed: `pip install requests beautifulsoup4 pandas`
2. Run the script: `python your_script_name.py`
3. Follow the on-screen prompts to perform CRUD operations on the country GDP data.'''


import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.populationu.com/gen/countries-by-gdp'

# Make a request to the website
response=requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    soup=BeautifulSoup(response.text, 'html.parser')

    # Find all tables with the class 'ptable2'
    country_tables = soup.find_all('table', class_='ptable2')
    data = []

    # Iterate through each table
    for table in country_tables:
        # Find all rows in the table
        rows = table.find_all('tr')

        # Iterate through each row
        for row in rows:
            # Find all cells in the row
            cells = row.find_all(['td', 'th'])

            # Extract the text content of each cell
            row_data = [cell.text.strip() for cell in cells]

            # Append the row data to the list
            data.append(row_data)

            # Add a separator line between rows
            print(' | '.join(row_data))
        print("---")

    # Create a pandas DataFrame from the extracted data
    df = pd.DataFrame(data[1:], columns=data[0])

    while True:
        print("\nOperations:")
        print("1. Create (Add a new row)")
        print("2. Read (Display specific information)")
        print("3. Update (Update a cell value)")
        print("4. Delete (Remove a row)")
        print("5. Exit")

        choice = input("Enter the operation number (1-5): ")

        if choice == '1':
            # CREATE: Add a new row
            new_row_data = []
            for column in df.columns:
                value = input(f"Enter value for {column}: ")
                new_row_data.append(value)
            df = df.append(pd.Series(new_row_data, index=df.columns), ignore_index=True)
            df.to_csv('countries_data.csv', index=False)  # Save the DataFrame to the CSV file
        elif choice == '2':
            # READ: Display specific information
            country_name = input("Enter the country name: ")
            print(df[df['Country'] == country_name])
        elif choice == '3':
            # UPDATE: Update the cell value
            country_name = input("Enter the country name for the update: ")
            column_name = input("Enter the column name to update: ")
            new_value = input("Enter the new value: ")
            df.loc[df['Country'] == country_name, column_name] = new_value
            df.to_csv('countries_data.csv', index=False)  # Save the DataFrame to the CSV file
        elif choice == '4':
            # DELETE: Remove a row
            country_name = input("Enter the country name to delete: ")
            df = df[df['Country'] != country_name]
            df.to_csv('countries_data.csv', index=False)  # Save the DataFrame to the CSV file
        elif choice == '5':
            # Exit the loop
            print("Exiting. DataFrame after operations saved to 'countries_data.csv'")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
else:
    print("Failed to retrieve the page. Status code:", response.status_code)
