import csv
from datetime import datetime, time, timedelta
import pytz
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

def crawl_mining_stats(url):
    print(f"Crawling workers status at {datetime.now()}")
    # Set up Selenium WebDriver
    service = webdriver.FirefoxService(executable_path='/usr/local/bin/geckodriver')
    driver = webdriver.Firefox(service=service)

    try:
        driver.get(url)
        # Example: Extract and print the title of the page
        title = driver.title
        print(f"Page Title: {title}")
        try:
            element = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.ID, "HOPE"))
            )
        except:
            pass  # Do nothing if the element is not found

        # Extract and print specific data from the table with id="worker-table"
        table = driver.find_element(By.ID, 'worker-table')
        if table:
            tbody = table.find_element(By.TAG_NAME, 'tbody')
            rows = tbody.find_elements(By.TAG_NAME, 'tr')
            
            # Open the CSV file for appending
            file_exists = os.path.isfile('randytx.csv')
            with open('/home/pi/data/randytx.csv', 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                
                # Write the header if the file is new
                """
                if not file_exists:
                    header = ['Timestamp', 'Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6']
                    csvwriter.writerow(header)
                """
                # Write the data rows
                for row in rows:
                    columns = row.find_elements(By.TAG_NAME, 'td')
                    if columns:
                        # Skip column[1] and column[6]
                        data = [columns[i].text for i in range(len(columns)) if i not in [1, 6]]
                        # if data[0] is empty, change it to be 'Unknown'
                        if data[0] == '':
                            data[0] = 'Unknown'
                        data[5] = '-' 
                        # if data[4] contains '\n', split it into two columns
                        if '\n' in data[4]:
                            data[4], data[5] = data[4].split('\n')
                        # Ensure data[4] has the correct format
                        if len(data[4]) == 16:  # Format is '%Y-%m-%d %H:%M'
                            data[4] += ':00'  # Append ':00' to match '%Y-%m-%d %H:%M:%S'
                        # insert the current date and time into the data
                        data.insert(0, datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S'))
                        csvwriter.writerow(data)
    finally:
        driver.quit()

def crawl_mining_miners(url):
    # Placeholder function for crawling miners
    print(f"Crawling miners at {datetime.now()}")
    # Set up Selenium WebDriver
    service = webdriver.FirefoxService(executable_path='/usr/local/bin/geckodriver')
    driver = webdriver.Firefox(service=service)
    try:
        driver.get(url)
        # Example: Extract and print the title of the page
        title = driver.title
        print(f"Page Title: {title}")

        # Wait for the element with class name " group" to be present, with a timeout of 120 seconds
        locator = (By.TAG_NAME, "hope")
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((locator))
            )
        except:
            pass  # Do nothing if the element is not found

        # Extract and print specific data from the table with id="worker-table"
        table = driver.find_element(By.ID, 'sort-by-miner-table')
        if table:
            tbody = table.find_element(By.TAG_NAME, 'tbody')
            rows = tbody.find_elements(By.TAG_NAME, 'tr')
            
            # Open the CSV file for appending
            with open('/home/pi/data/miners.csv', 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                
                # Write the data rows
                for row in rows:
                    columns = row.find_elements(By.TAG_NAME, 'td')
                    if columns:
                        data = [columns[i].text for i in range(len(columns))]
                        # deal with data[0] that contains '\n'
                        if '\n' in data[0]:
                            # replace the '\n' with ''
                            data[0] = data[0].replace('\n','')

                        # deal with the data[5] that contains '\n'
                        if '\n' in data[5]:
                            data[5] = data[5].split('\n')[0]
                        # insert the current date and time into the data
                        data.insert(0, datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S'))
                        csvwriter.writerow(data)
    finally:
        driver.quit()


if __name__ == '__main__':
    url_randytx = 'https://www.f2pool.com/mining-user-ltc/0522834fec2c2ec908e2da44bc259f5e?user_name=randytx'
    url_miners = 'https://www.f2pool.com/miners'
    last_miner_crawl = datetime.now() - timedelta(hours=12)  # Initialize to ensure the first run

    while True:
        # Crawl the mining stats
        crawl_mining_stats(url_randytx)
        
        # Check if 12 hours have passed since the last miner crawl
        if datetime.now() - last_miner_crawl >= timedelta(hours=12):
            crawl_mining_miners(url_miners)
            last_miner_crawl = datetime.now()  # Update the last crawl time

        # Sleep for 10 minutes before the next crawl
        sleep(600)  # 600 seconds = 10 minutes