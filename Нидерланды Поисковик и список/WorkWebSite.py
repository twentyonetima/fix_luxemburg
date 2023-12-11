import time
import requests
from bs4 import BeautifulSoup
from googletrans import Translator


def change_using(html_content, element_name):
    """
    Метод перехода по ссылкам
    :param html_content: HTML content of the page
    :param element_name: имя селектора
    :return: List of elements
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    find_elements = soup.select(element_name)
    return find_elements


def test(url, type_list, start_page=1):
    """
    Функция тестирования парсера и дальнейшего запуска
    :param url: URL of the page
    :param type_list: Type list
    :param start_page: Starting page number
    :return: List of dictionaries
    """
    translator = Translator()
    json_dictionary = {}
    all_dictionary = []
    key = []
    value = []

    session = requests.Session()
    page_number = start_page
    response = session.get(url)
    time.sleep(3)

    # Handle cookie consent if needed
    cookie_consent_button = session.cookies.get('cookie_consent_button')
    if cookie_consent_button:
        session.cookies.set('cookie_consent_button', 'true')
    print()
    while True:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = change_using(response.content, ".register-result__title a")
        print()
        for i, link in enumerate(links):
            link_url = link['href']
            print(link_url)

            link_response = session.get(link_url)
            link_soup = BeautifulSoup(link_response.content, 'html.parser')

            data = link_soup.select(".page-meta__date")
            keys = link_soup.select(".label")
            values = link_soup.select(".value")
            contacts_list = link_soup.select(".contact-details__address li span")
            for contact in range(len(contacts_list)):
                if contact % 2 == 0:
                    if contacts_list[contact].text == "Adress:":
                        key.append('addresses_of_exchange_offices')
                    elif contacts_list[contact].text == "Place of residence:":
                        key.append('legal_entity_address')
                    else:
                        key.append(contacts_list[contact].text)
                else:
                    value.append(contacts_list[contact].text)
            if i < len(data):
                key.append("data_publish")
                value.append(data[0].text)
            for items in range(len(keys)):
                if keys[items].text == "Statutory name:":
                    key.append('name')
                    value.append(values[items].text.replace("\"", ""))
                elif keys[items].text == "Statutory seat:":
                    key.append('addresses_of_exchange_officess')
                    value.append(values[items].text.replace("\"", ""))
                elif keys[items].text == "LEI code:":
                    key.append('сbr_license_id')
                    value.append(values[items].text.replace("\"", ""))
                elif keys[items].text == "URL:":
                    key.append('social_networks')
                    value.append(values[items].text.replace("\"", ""))
                elif keys[items].text == "Disclosure":
                    key.append('remarks')
                    translates = translator.translate(values[items].text, dest="ru")
                    value.append(translates.text.replace("/", ""))
                else:
                    key.append(keys[items].text)
                    value.append(values[items].text.replace("\"", ""))

            count = 0
            # print(len(key))
            # print(len(value))
            # chek = len(key)

            for s in range(len(key)):

                if count != len(key):
                    count += 1
                    json_dictionary[key[s]] = value[s]

                    if count == len(key):
                        json_dictionary['type'] = type_list
                        json_dictionary[
                            'source'] = f"https://www.dnb.nl/en/public-register/?p={str(page_number)}&l=20"
                        json_dictionary['Country'] = 'Netherlands'
                        print(json_dictionary)
                        all_dictionary.append(json_dictionary)
                        json_dictionary = {}

            # Move to the next page
        next_button = soup.select_one('.pagination__item--next-page button')
        if not next_button:
            break
        next_url = next_button['onclick'].split("'")[1]
        response = session.get(next_url)
        time.sleep(3)
        page_number += 1

    return all_dictionary


if __name__ == "__main__":
    url = "https://www.dnb.nl/en/public-register/?p=1&l=20"
    type_list = "black_list"
    result = test(url, type_list)
    print(result)
