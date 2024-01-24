import time
import re
from math import ceil
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scrape_data_viva_real(pages_number, price_range, property_types, num_bedrooms, num_bathrooms, min_area, max_area, num_parking_slots, neighborhoods):
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
    driver = webdriver.Chrome(options=chrome_options)
    
    neighborhood_filter = ""
    for neighborhood in neighborhoods:
        neighborhood_filter += f',Paran%C3%A1,Londrina,Bairros,{neighborhood},,,neighborhood,BR%3EParana%3ENULL%3ELondrina%3EBarrios%3E{neighborhood},,,;'
    neighborhood_filter = neighborhood_filter[:-1]

    link = f'https://www.vivareal.com.br/venda/parana/londrina/#area-ate={max_area}&area-desde={min_area}&banheiros={num_bathrooms}&onde=Brasil,Paran%C3%A1,Londrina,,,,,,BR%3EParana%3ENULL%3ELondrina,,,;{neighborhood_filter}&preco-ate={price_range}&quartos={num_bedrooms}&tipos={property_types}&vagas={num_parking_slots}'
    print(link)
    driver.get(link)

    try:
        cookie_popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'cookie-notifier'))
        )
        accept_button = cookie_popup.find_element(By.ID, 'cookie-notifier-cta')
        accept_button.click()

    except TimeoutException:
        print("Nenhum pop-up de consentimento de cookies encontrado ou não foi necessário.")
    
    if(pages_number <= 0):
        time.sleep(5)
        total_records_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-total-records'))
        )
        total_records = int(float(total_records_element.text.replace('.', '').replace(',', '.')))
        pages_number = ceil(total_records / 36)

    page = 1
    while page <= pages_number:
        print(f'Pagina {page}')
        time.sleep(15)
        data = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        soup_complete_source = BeautifulSoup(data, "html.parser")

        soup = soup_complete_source.select('.results-list.js-results-list [data-type="property"]')
        for line in soup:
            try:
                full_address = line.select_one(".property-card__address").text.strip()
                address.append(full_address.replace('\n', ''))

                if any(prefix in full_address for prefix in ['Rua', 'Avenida', 'Travessa', 'Alameda']):
                    neighbor_text = re.search(r'-(.*?),', full_address)
                    neighbor.append(neighbor_text.group(1) if neighbor_text else '-')
                else:
                    neighbor_text = full_address.split(',')[0] if ',' in full_address else full_address.split('-')[0]
                    neighbor.append(neighbor_text)

                full_link = line.select_one('.property-card__content-link')['href']
                link_imovel.append(f'https://www.vivareal.com.br{full_link}')

                full_area_element = line.select_one(".property-card__detail-value.js-property-card-value.property-card__detail-area.js-property-card-detail-area")
                area.append(full_area_element.text.strip() if full_area_element else None)

                full_tipo = line.select_one('.property-card__title.js-cardLink.js-card-title').text.split()[0].replace(' ', '').replace('\n', '')
                tipo.append(full_tipo)

                full_room = re.sub(r'\D', '', line.select_one(".property-card__detail-room.js-property-detail-rooms").text.strip())
                room.append(full_room)

                full_bath = re.sub(r'\D', '', line.select_one(".property-card__detail-bathroom.js-property-detail-bathroom").text.strip())
                bath.append(full_bath)

                full_park = re.sub(r'\D', '', line.select_one(".property-card__detail-garage.js-property-detail-garages").text.strip())
                park.append(full_park)

                full_price = re.sub(r'\D', '', line.select_one(".property-card__price.js-property-card-prices.js-property-card__price-small").text.strip())
                price.append(full_price)

            except AttributeError:
                print('Erro')

        if page < pages_number:
            try:
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button.js-change-page[title="Próxima página"]'))
                )
                next_page_button.click()

                WebDriverWait(driver, 10).until(
                    EC.url_changes(driver.current_url)
                )

            except Exception as e:
                print(f"Erro ao processar a página {page}: {e}")
                break
        page += 1

    driver.quit()
    return link_imovel, address, neighbor, area, tipo, room, bath, park, price  