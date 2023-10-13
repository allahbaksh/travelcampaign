import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from itertools import product

# Set the absolute path for the CSV file
CSV_PATH = "flight_datasets/flight_data_set1.csv"

# Number of flights to scrape
COUNT = 1000

# List of cities for "From" and "To" options
from_cities = ["HKG", "SIN", "BKK", "LHR", "MFM", "KUL", "SZX", "JFK", "AYT", "CDG", "IST", "FCO", "DXB", "CAN", "HKT", "JED", "UTP", "TPE", "PRG", "PVG", "LAS", "MIA", "BCN", "SVO", "PEK", "LAX", "BUD", "VIE", "AMS", "SOF", "MAD", "MCO", "SGN", "LIM", "TXL", "HND", "WAW", "MAA", "CAI", "NBO", "HGH", "MXP", "SFO", "EZE", "VCE", "MEX", "DUB", "ICN", "DLM", "BOM", "DPS", "DEL", "YYZ", "ZUH", "LED", "BOJ", "SYD", "DJE", "MUC", "JNB", "CUN", "EDI", "SZV", "OTP", "PUJ", "AGR", "JAI", "BRU", "NCE", "CNX", "SSH", "LIS", "DMM", "RAK", "CGK", "BAH", "HAN", "HNL", "MNL", "KWL", "AKL", "REP", "TTM", "AMM", "YVR", "AUH", "KBP", "DOH", "FLR", "GIG", "MEL", "IAD", "RUH", "CHC", "FRA", "BAK", "GRU", "HRE", "CCU", "NKG"]
to_cities = ["NKG", "CCU", "HRE", "GRU", "BAK", "FRA", "CHC", "RUH", "IAD", "MEL", "GIG", "FLR", "DOH", "KBP", "AUH", "YVR", "AMM", "TTM", "REP", "AKL", "KWL", "MNL", "HNL", "HAN", "CGK", "RAK", "DMM", "LIS", "SSH", "CNX", "NCE", "BRU", "JAI", "AGR", "PUJ", "OTP", "SZV", "EDI", "CUN", "JNB", "MUC", "DJE", "SYD", "BOJ", "LED", "ZUH", "YYZ", "DEL", "DPS", "BOM", "DLM", "ICN", "DUB", "MEX", "VCE", "EZE", "SFO", "MXP", "HGH", "NBO", "CAI", "MAA", "WAW", "HND", "TXL", "LIM", "SGN", "MCO", "MAD", "SOF", "AMS", "VIE", "BUD", "LAX", "PEK", "SVO", "BCN", "MIA", "LAS", "PVG", "PRG", "TPE", "UTP", "JED", "HKT", "CAN", "DXB", "FCO", "IST", "CDG", "AYT", "JFK", "SZX", "KUL", "MFM", "LHR", "BKK", "SIN", "HKG"]

# List of dates to scrape (add more dates as needed)
dates_to_scrape = ["15/10/2023", "16/10/2023", "17/10/2023", "18/10/2023", "19/10/2023", "20/10/2023", "21/10/2023"]

chrome_options = Options()

options = [
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-blink-features",
    "--disable-blink-features=AutomationControlled",
    "--disable-3d-apis"
]

for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(options=chrome_options)

# Initialize a variable to keep track of the current date
current_date = None

try:
    # Ensure the directory exists
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

    for from_city, to_city, date in product(from_cities, to_cities, dates_to_scrape):
        # Construct the URL with "From" and "To" cities and the date
        url = f"https://www.makemytrip.com/flight/search?tripType=O&itinerary={from_city}-{to_city}-{date}&paxType=A-1_C-0_I-0&cabinClass=E&sTime=1695980223513&forwardFlowRequired=true&mpo=&semType=&intl=true"
        driver.get(url)
        time.sleep(5)  # Adjust the sleep time based on your network speed and page loading time

        # Check if the date has changed, and if so, update the date and click on the element
        if date != current_date:
            current_date = date
            try:
                # Click on the element to update the date
                update_date_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/div/span')
                update_date_element.click()
                time.sleep(2)  # Wait for the page to update with the new date
            except Exception as e:
                print(f"Error occurred while updating date: {e}")

        for i in range(1, COUNT + 1):
            try:
                block = driver.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']')
                # Check if the block has already been processed
                if 'data-scraped' in block.get_attribute('class'):
                    continue

                # Mark the block as processed
                block.get_attribute('class').split(' ')
                block_class = block.get_attribute('class') + ' data-scraped'
                driver.execute_script("arguments[0].setAttribute('class', arguments[1]);", block, block_class)

                # Scrape flight details
                fname = block.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[1]/div/p[1]').text
                print("Flight Name: " + fname)
                fcode = block.find_element(By.CLASS_NAME, 'fliCode').text
                print("Flight Code: " + fcode)

                # DEPARTURE
                deptime = block.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[1]/p[1]').text
                print("Departure Time: " + deptime)
                depcity = block.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[1]/p[2]').text
                print("Departure City: " + depcity)

                # ARRIVAL
                arrtime = block.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[3]/p[1]').text
                print("Arrival Time: " + arrtime)
                arrcity = block.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[3]/p[2]').text
                print("Arrival City: " + arrcity)
                duration = block.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[2]/p').text
                print("Duration: " + duration)

                price = driver.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[2]/div/div/div').text
                price = price.split('\n')
                price = price[0][2:]
                print("Price: " + price)

                data = [[fname, fcode, depcity, deptime, arrcity, arrtime, duration, price, date]]
                with open(CSV_PATH, 'a', newline='', encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerows(data)

                time.sleep(5)

                # Click somewhere outside the block to remove it using ActionChains
                action = ActionChains(driver)
                action.move_by_offset(0, 0).click().perform()
            except Exception as e:
                print(f"An error occurred: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.close()