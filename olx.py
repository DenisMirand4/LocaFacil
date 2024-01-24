import time
import re
from math import ceil
from bs4 import BeautifulSoup, SoupStrainer
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
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
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--incognito')
    # chrome_options.add_argument('--headless')
    chromedriver = "./chromedriver"
    chrome_options.add_argument(f"webdriver.chrome.driver={chromedriver}")
    driver = Chrome(options=chrome_options)
    
    # neighborhood_filter = ""
    # for neighborhood in neighborhoods:
    #     neighborhood_filter += f',Paran%C3%A1,Londrina,Bairros,{neighborhood},,,neighborhood,BR%3EParana%3ENULL%3ELondrina%3EBarrios%3E{neighborhood},,,;'
    # neighborhood_filter = neighborhood_filter[:-1]

    # link = f'https://www.vivareal.com.br/venda/parana/londrina/#area-ate={max_area}&area-desde={min_area}&banheiros={num_bathrooms}&onde=Brasil,Paran%C3%A1,Londrina,,,,,,BR%3EParana%3ENULL%3ELondrina,,,;{neighborhood_filter}&preco-ate={price_range}&quartos={num_bedrooms}&tipos={property_types}&vagas={num_parking_slots}'
    link = f'https://www.olx.com.br/estado-sp?q=casa&cg=1000'
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
    
    # if(pages_number <= 0):
    #     time.sleep(5)
    #     total_records_element = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, 'js-total-records'))
    #     )
    #     total_records = int(float(total_records_element.text.replace('.', '').replace(',', '.')))

    #     # Calculate the number of pages based on the total number of records and the page size (36)
    #     pages_number = ceil(total_records / 36)

    print(pages_number)
    page = 1
    while page <= pages_number:
        print(f'Pagina {page}')
        time.sleep(15)
        # data = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        data = driver.page_source
        data_without_svg = re.sub(r'<svg.*?</svg>', '', data, flags=re.DOTALL)
        soup_complete_source = BeautifulSoup(data_without_svg, "html.parser")
        # print(soup_complete_source.prettify())
        # soup_complete_source = BeautifulSoup(data, "html.parser")
        soup = soup_complete_source.select('.gHnzLR')

        script_tag = soup_complete_source.find('script', {'id': '__NEXT_DATA__'})
        json_data = json.loads(script_tag.contents[0])
        ads = json_data.get('props', {}).get('pageProps', {}).get('ads', [])
        for ad in ads:
            print(ad)
            print('\n')
        # print(script_tag)
        # print(soup)
        # print(type(soup))
        for line in soup:
            # print(line)
            full_address = line.select_one(".olx-ad-card__location-date-container p.olx-text.olx-text--caption.olx-text--block.olx-text--regular")
            if full_address is not None:
                full_address = full_address.text.strip()

                # print(full_address)
                # print('\n')
                address.append(full_address.replace('\n', ''))
                    # if any(prefix in full_address for prefix in ['Rua', 'Avenida', 'Travessa', 'Alameda']):
                #     neighbor_text = re.search(r'-(.*?),', full_address)
                #     neighbor.append(neighbor_text.group(1) if neighbor_text else '-')
                # else:
                #     neighbor_text = full_address.split(',')[0] if ',' in full_address else full_address.split('-')[0]
                #     neighbor.append(neighbor_text)

                # full_link = line.select_one('.olx-ad-card__title-link')['href']
                # link_imovel.append(f'https://www.olx.com.br{full_link}')
                # print(full_link)

                # full_area_element = line.select_one('.olx-ad-card__labels-item span[aria-label$="metros quadrados"]')
                # area.append(full_area_element.text.strip() if full_area_element else None)
                # print(full_area_element)

                # full_tipo = line.select_one('.olx-text olx-text--subtitle-medium olx-text--block olx-ad-card__subtitle').text.split()[0].replace(' ', '').replace('\n', '')
                # tipo.append(full_tipo)
                # print(full_tipo)

                # full_room = re.sub(r'\D', '', line.select_one('.olx-ad-card__labels-item span[aria-label$="quartos"]').text.strip())
                # room.append(full_room)
                # print(full_room)

                # full_bath = re.sub(r'\D', '', line.select_one('.olx-ad-card__labels-item span[aria-label$="banheiros"]').text.strip())
                # bath.append(full_bath)
                # print(full_bath)

                # full_park = re.sub(r'\D', '', line.select_one('.olx-ad-card__labels-item span[aria-label$="vagas de garagem"]').text.strip())
                # park.append(full_park)
                # print(full_park)
                # print(line.select_one(".olx-text olx-text--body-large olx-text--block olx-text--semibold olx-ad-card__price"))
                # full_price = re.sub(r'\D', '', line.select_one(".olx-text olx-text--body-large olx-text--block olx-text--semibold olx-ad-card__price").text.strip())
                # price.append(full_price)
                # print(full_price)

            # except AttributeError:
            #     print('Erro')

        # if page < pages_number:
        #     try:
        #         next_page_button = WebDriverWait(driver, 10).until(
        #             EC.presence_of_element_located((By.CSS_SELECTOR, 'button.js-change-page[title="Próxima página"]'))
        #         )
        #         next_page_button.click()

        #         WebDriverWait(driver, 10).until(
        #             EC.url_changes(driver.current_url)
        #         )

        #     except Exception as e:
        #         print(f"Erro ao processar a página {page}: {e}")
        #         break
        page += 1

    driver.quit()
    return link_imovel, address, neighbor, area, tipo, room, bath, park, price  


if __name__ == "__main__":
    pages_number = 1
    price_range = "350000"
    property_types = "casa_residencial,apartamento_residencial"
    num_bedrooms = ""
    num_bathrooms = ""
    min_area = ""
    max_area = ""
    num_parking_slots = ""
    neighborhoods_part1 = [
        "Centro", "Jardim Higienópolis", "Jardim Petrópolis", "Quebec", "Vila Brasil",
        "Casoni", "Vila Ipiranga", "Vila Nova", "Recreio", "Aeroporto", "Cidade Industrial 2",
        "Conjunto Ernani Moura Lima", "Operaria","Jardim Perola","Lago Juliana","Jardim Guararapes",
        "Vitoria Regia", "Antares", "Brasília", "California", "Ideal", "Jardim Interlagos", "Interlagos"
    ]

    link_imovel, address, neighbor, area, tipo, room, bath, park, price = scrape_data_olx(pages_number, price_range, property_types, num_bedrooms, num_bathrooms, min_area, max_area, num_parking_slots, neighborhoods_part1)
    print(link_imovel)
    print(address)
    print(neighbor)
    print(area)
    print(tipo)
    print(room)
    print(bath)
    print(park)
    print(price)