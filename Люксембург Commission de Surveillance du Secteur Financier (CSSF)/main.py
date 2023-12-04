import SaveHdd
import WorkWebSite
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup


# Connect the driver
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome()
url = "https://www.cssf.lu/en/warnings/"
driver.get(url)

# Get the initial page content using requests and BeautifulSoup
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Call the test function from WorkWebsite.py
result = WorkWebSite.test(url, soup, "black_list")
save = SaveHdd.save_json(result)



