import time
import re
import requests
from bs4 import BeautifulSoup
from googletrans import Translator


def change_using(html_content, element_name):
    soup = BeautifulSoup(html_content, 'html.parser')
    find_elements = soup.select(element_name)
    return find_elements


def click_button(soup, name_button, times=None):
    time.sleep(times)
    button = soup.select_one(name_button)
    print('Click')
    button.click()


def test(url, type_list):
    translator = Translator()
    read_files = []
    json_dictionary = {}
    key = []
    value = []
    all_dictonary = []
    data_published_list = []
    page_number = 0

    # Download the HTML content using requests
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    click_button(soup, ".coi-banner__accept", 3)
    time.sleep(3)

    odd = change_using(html_content, ".odd")
    even = change_using(html_content, ".even")
    all_list = odd + even
    all_date = []
    count_data = 0

    while page_number < 21:
        time.sleep(3)
        for i in range(len(all_list)):
            # Re-find the elements inside the loop
            all_list = change_using(html_content, ".odd") + change_using(html_content, ".even")

            for j in range(3):
                all_date.append(all_list[i].select("td")[j].text)
        print(all_date)
        for k in range(len(all_date)):

            if count_data == 0:
                key.append("date_publish")
                value.append(all_date[k])
                count_data += 1

            elif count_data == 1:
                items = all_date[k]
                pattern = r"(?:https?:\/\/|ftps?:\/\/|www\.)(?:(?![.,?!;:()]*(?:\s|$))[^\s]){2,}"
                url = re.findall(pattern, items)
                items2 = all_date[k].split(" ")
                count_data += 1
                if len(items2) == 2:
                    print(items2)
                    key.append("name")
                    value.append(items2[0].replace("\"", " "))
                    key.append("links")
                    if len(url) == 0:
                        value.append([remove_parentheses(items2[1]), ])
                    else:
                        value.append([url[0], ])
                else:
                    if url:
                        print(url)
                        key.append("name")
                        value.append(url[0])
                        key.append("links")
                        value.append([url[0], ])
                    else:
                        key.append("name")
                        text = all_date[k].replace("\"", "")
                        value.append(text)

            elif count_data == 2:
                key.append("remarks")
                translation = translator.translate(all_date[k], dest='ru')
                value.append(translation.text)
                count_data = 0

        count = 0
        print(len(key))
        print(len(value))
        chek = len(key)

        for s in range(len(key)):

            if count != 3:
                count += 1
                json_dictionary[key[s]] = value[s]
                print()

                if count == 3:
                    json_dictionary['type'] = type_list
                    json_dictionary['Country'] = 'Finland'
                    print(json_dictionary)
                    all_dictonary.append(json_dictionary)
                    json_dictionary = {}
                    count = 0
        key.clear()
        value.clear()
        all_date.clear()
        # Clicking the "Next" button
        next_button_selector = ".pagination .next a"
        click_button(soup, next_button_selector, 3)

        # Download the new HTML content for the next page
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Increment the page number
        page_number += 1
        print("Page number", page_number)

    return all_dictonary


def remove_parentheses(input_string):
    # Remove "(" and ")"
    cleaned_string = input_string.replace("(", "").replace(")", "")
    return cleaned_string


if __name__ == "__main__":
    import SaveHdd

    url = "https://www.finanssivalvonta.fi/en/registers/warning-lists/warnings-concerning-unauthorised-service-providers/"
    test_result = test(url, "black_list")
    save = SaveHdd.save_json(test_result)

