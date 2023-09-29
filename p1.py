from bs4 import BeautifulSoup
import requests
import csv

url = "https://brilliantmaps.com/top-100-tourist-destinations"
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')

data = soup.find('tbody', class_='row-hover')

column1 = data.find_all('td', class_='column-1')
column2 = data.find_all('td', class_='column-2')
column3 = data.find_all('td', class_='column-3')
column4 = data.find_all('td', class_='column-4')

# Create a list to store the data
destination_data = []

for col1, col2, col3, col4 in zip(column1, column2, column3, column4):
    destination_data.append([col1.text.strip(), col2.text.strip(), col3.text.strip(), col4.text.strip()])

# Specify the CSV file path
csv_file_path = 'tourist_destinations.csv'

# Write the data to a CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write the header row
    csv_writer.writerow(['Rank', 'Destination', 'Country', 'Visitors (millions)'])
    
    # Write the data rows
    csv_writer.writerows(destination_data)

print(f'Data has been saved to {csv_file_path}')