import time
import re
from math import ceil
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json

def is_not_svg(element):
    return element.name != 'svg'

def scrape_data_olx(pages_number, price_range, property_types, num_bedrooms, num_bathrooms, min_area, max_area, num_parking_slots, neighborhoods):
    link_imovel = []
    address = []
    neighbor = []
    area = []
    tipo = []
    room = []
    bath = []
    park = []
    price = []

    chrome_options = Options()
    chromedriver = "./chromedriver"
    chrome_options.add_argument(f"webdriver.chrome.driver={chromedriver}")
    driver = Chrome(options=chrome_options)
    
    neighborhoods = 'sd=nb36487&sd=nb36326&sd=nb36233&sd=nb36443&sd=nb36310&sd=nb36371&sd=nb36396&sd=nb36415&sd=nb36170&sd=nb36268&sd=nb36345&sd=nb36106&sd=nb36430&sd=nb36223&sd=nb36410&sd=nb36412&sd=nb36409&sd=nb36141&sd=nb36509&sd=nb36314&sd=nb36048&sd=nb36347&sd=nb36421&sd=nb36351&sd=nb36483&sd=nb36504&sd=nb36309&sd=nb36152&sd=nb36198&sd=nb36497&sd=nb36111&sd=nb36067&sd=nb36117&sd=nb36088'
    link = f'https://www.olx.com.br/imoveis/venda/estado-pr/regiao-de-londrina/londrina'
    link += f'?pe={price_range}&ros={num_bedrooms}&bas={num_bathrooms}&gsp={num_parking_slots}&{neighborhoods}'
    print(link)
    driver.get(link)

    try:
        cookie_popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'cookie-notice-box'))
        )
        accept_button = cookie_popup.find_element(By.ID, 'cookie-notice-ok-button')
        accept_button.click()

    except TimeoutException:
        print("Nenhum pop-up de consentimento de cookies encontrado ou não foi necessário.")
    
    if(pages_number <= 0):
        time.sleep(5)
        total_records_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'olx-text.olx-text--body-small.olx-text--block.olx-text--regular.olx-color-neutral-110'))
        )
        total_results_text = total_records_element.text.strip()
        total_value = int(total_results_text.split()[-2].replace('.', ''))
        pages_number = ceil(total_value / 50)

    print(pages_number)
    page = 1
    while page <= pages_number:
        print(f'Pagina {page}')
        time.sleep(15)
        data = driver.page_source
        data_without_svg = re.sub(r'<svg.*?</svg>', '', data, flags=re.DOTALL)
        soup_complete_source = BeautifulSoup(data_without_svg, "html.parser")

        script_tag = soup_complete_source.find('script', {'id': '__NEXT_DATA__'})
        json_data = json.loads(script_tag.contents[0])
        ads = json_data.get('props', {}).get('pageProps', {}).get('ads', [])
        for line in ads:
            if 'location' in line:
                full_address = line['location']
                address.append(full_address.replace('\n', ''))
            
            if 'locationDetails' in line:
                full_neighbor = line['locationDetails'].get('neighbourhood', '')
                neighbor.append(full_neighbor.replace('\n', ''))
            
            if 'url' in line:
                full_link = line['url']
                link_imovel.append(full_link)
            
            if 'price' in line:
                full_price = line['price']
                numeric_price = int(re.sub(r'[^\d]', '', full_price))
                price.append(numeric_price)

            if 'properties' in line:
                properties_dict = {prop['name']: prop['value'] for prop in line['properties']}
                
                area.append(properties_dict.get('size', ''))
                room.append(properties_dict.get('rooms', ''))
                bath.append(properties_dict.get('bathrooms', ''))
                park.append(properties_dict.get('garage_spaces', ''))
                tipo.append(properties_dict.get('category', ''))

        if page < pages_number:
            current_url = driver.current_url
            next_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Próxima página'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", next_page_button)
            time.sleep(2)
            next_page_button.click()
            WebDriverWait(driver, 10).until(
            lambda driver: driver.current_url != current_url
        )
        page += 1

    driver.quit()
    return link_imovel, address, neighbor, area, tipo, room, bath, park, price  