from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import SaveHdd
import WorkWebSite
import time

# region parameter Browser
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome()
url = "https://www.sec.gov/enforce/public-alerts"
driver.get(url)

# Wait for a few seconds to let the JavaScript load the content
time.sleep(5)

# Get the page source after JavaScript execution
page_source = driver.page_source

# Close the browser
driver.quit()
# endregion

# Use BeautifulSoup for parsing the page source
soup = BeautifulSoup(page_source, 'html.parser')

# Call the parsing function with the URL, type_list, and soup
test = WorkWebSite.parsing(url, "black_list", soup)

# Save the result to a JSON file
# save = SaveHdd.save_json(test)
