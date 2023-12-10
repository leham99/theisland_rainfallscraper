from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time
import csv

# User credentials for login. Replace with actual username and password.
user = "enter your username"
p = "enter your password"


#you need to download the latest chromedriver from the following link
#(make sure you click on chromedriver for your system under the binary colum)
#https://googlechromelabs.github.io/chrome-for-testing/#stable
# Setup the Chrome WebDriver. Replace the path with the actual path of your ChromeDriver.
service = Service(executable_path=r"yourpath\chromedriver.exe")
driver = webdriver.Chrome(service=service)

def load_url(driver):
    # Base URL of the website to scrape.
    base_url = 'https://islands.smp.uq.edu.au/climate.php?'

    # Loop through the pages (change range to scrape more/less days).
    for i in range(26):
        url = f"{base_url}{i}"
        driver.get(url)
        click_javascript_button(driver)
        data = extract_data(driver)
        rain_mean = average(data)
        save_data_to_csv(rain_mean,"output.csv")

def navigate_and_login(driver, user, password):
    # Navigate to the login page and login with provided credentials.
    url = 'https://islands.smp.uq.edu.au/climate.php?0'
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    username = driver.find_element(By.NAME, 'email')
    pwd = driver.find_element(By.NAME, 'word')

    username.send_keys(user)
    pwd.send_keys(password)

    sign_in = wait.until(EC.element_to_be_clickable((By.NAME, "Sign In")))
    sign_in.click()
    time.sleep(5)

def click_javascript_button(driver):
    # Wait for and click a specific JavaScript button on the page.
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.ID, "t2tab")))
    button.click()
    time.sleep(5)

def extract_data(driver):
    # Parse the HTML of the current page and extract data.
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    content_div = soup.find('div', {'id': 'content'})
    t2_div = content_div.find('div', {'id': 't2', 'class': 'content_tab'})
    table = t2_div.find('table')
    rows = table.find('tbody').find_all('tr')[-28:]  # Change -28 to modify the number of days.
    #the "-" makes -28 start at the end of the list and capture the last 28 days.
    #if you remove the "-" you will start at the top


    # Extract the third cell (rainfall) from each row. You can change the value in cells[2] to 1 to get max temp
    data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 3:
            data.append(cells[2].text.strip())  # Change cells[2] to cells[1] to capture max temp per day instead

    return data

def average(av_data):
    # Calculate the average of the provided data.
    total = 0
    for x in av_data:
        total += float(x)
    mean = round(total / len(av_data), 2)

    return mean

def save_data_to_csv(data, filename):
    # Save the scraped data to a CSV file.
    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data])
    except Exception as e:
        print(f"Error writing to file: {e}")

# Main workflow to log in and start data scraping.
navigate_and_login(driver, user, p)
load_url(driver)