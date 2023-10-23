import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

# Set the absolute path for the CSV file
CSV_PATH = "flight_datasets/flight_data_DEL_HYD.csv"

# Number of flights to scrape
COUNT = 50

# List of dates to scrape (add more dates as needed)
dates_to_scrape = ["29/09/2023", "30/09/2023", "01/10/2023"]

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

for date in dates_to_scrape:
    driver.get(f"https://www.makemytrip.com/flight/search?itinerary=BLR-DEL-{date}&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&ccde=IN&lang=eng")
    time.sleep(25)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

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

            # Scrape code (similar to your existing code)
            driver.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[3]/span').click()
            time.sleep(1)                         
        
            fname = block.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[1]/div/p[1]').text
            print(fname)
            fcode = block.find_element(By.CLASS_NAME, 'fliCode').text
            print("flightcode: " + fcode)

            # DEPARTURE
            deptime = block.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[1]/p[1]').text
            print("deptime: " + deptime)
            depcity = block.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[1]/p[2]').text
            print("depcity: " + depcity)

            # ARRIVAL
            arrtime = block.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[3]/p[1]').text
            print("arrtime: " + arrtime)
            arrcity = block.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[3]/p[2]').text
            print("arrcity:" + arrcity)
            duration = block.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[2]/p').text
            print("duration: " + duration)

            price = driver.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[2]/div/div/div').text
            price = price.split('\n')
            price = price[0][2:]
            print("price: " + price)

            data = [[fname, fcode, depcity, deptime, arrcity, arrtime, duration, price]]
            with open(CSV_PATH, 'a', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(data)

            time.sleep(2)

            # Click somewhere outside the block to remove it using ActionChains
            action = ActionChains(driver)
            action.move_by_offset(0, 0).click().perform()

        except Exception as e:
            print(f"An error occurred: {e}")

driver.close()