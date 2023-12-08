import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import SaveHdd

def get_dynamic_page_content(url):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)  # Give the page some time to load the dynamic content
    content = driver.page_source
    driver.quit()
    return content

def test(url, type_list):
    json_dictionary = {}
    all_dictionary = []
    page_number = 1

    while page_number < 80:
        url_with_page = f"{url}?page={page_number}"
        content = get_dynamic_page_content(url_with_page)
        soup = BeautifulSoup(content, 'html.parser')

        list_data = soup.select(".mas-search-card")
        print()
        for item in list_data:
            print(item)
            key = []
            value = []

            data = item.select_one(".mas-ancillaries")
            name = item.select_one(".ola-field-button")

            if data:
                key.append('date_publish')
                value.append(data.get_text(strip=True).split(":")[1])

            items = name.get_text(strip=True)
            pattern = r"(?:https?:\/\/|ftps?:\/\/|www\.)(?:(?![.,?!;:()]*(?:\s|$))[^\s]){2,}"
            url2 = re.findall(pattern, items)

            if url2:
                key.append("links")
                value.append([url2[0], ])
            else:
                key.append('name')
                value.append(name.get_text(strip=True))

            # # Interaction with buttons
            # button = item.select_one("button")
            # if button:
            #     button_text = button.find("div", class_="mas-btn__text")
            #     if button_text and "Show details" in button_text.get_text():
            #         button.click()
            #         time.sleep(5)  # Adjust this wait time based on the loading time of the dynamic content
                    # Extract data from the dynamically loaded content
            dynamic_data = item.select_one('.masx-toggle-content')
            if dynamic_data:
                for content_item in dynamic_data.select('.masx-toggle-content__item'):
                    show_title = content_item.select_one('h4')
                    show_p = content_item.select_one('p')
                    if show_title and show_p:
                        key.append(show_title.get_text(strip=True))
                        value.append(show_p.get_text(strip=True))

            # After extracting data, add the common information
            key.extend(["phone", "email", "legal_entity_address"])
            value.extend(["", "", ""])

            json_dictionary = dict(zip(key, value))
            json_dictionary['type'] = type_list
            json_dictionary['source'] = url
            json_dictionary['Country'] = 'Singapore'
            print(json_dictionary)
            all_dictionary.append(json_dictionary)

        page_number += 1
        print("Page number", page_number)

    return all_dictionary


if __name__ == "__main__":
    url = "https://www.mas.gov.sg/investor-alert-list"
    type_list = "black_list"

    # Create a driver object before calling test function
    driver = webdriver.Chrome()
    test_data = test(url, type_list)
    SaveHdd.save_json(test_data)
    driver.quit()
