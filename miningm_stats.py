import csv
from datetime import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Scrape the website page using Selenium
url = 'https://www.f2pool.com/mining-user-ltc/0522834fec2c2ec908e2da44bc259f5e?user_name=randytx'

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
        with open('/tmp/randytx.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            
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
                    data.insert(0, datetime.now(pytz.timezone('US/Central')).strftime('%Y-%m-%d %H:%M:%S'))
                    csvwriter.writerow(data)
finally:
    driver.quit()
