import time
import pandas as pd
from vivaReal import scrape_data_viva_real
from olx import scrape_data_olx

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

neighborhoods_part2 = [
    "Residencial Abussafe", "Residencial Abussafe II", "Conjunto Alexandre Urbanas",
    "Jardim Portal dos Pioneiros", "Fraternidade", "Vale dos Tucanos", "Alto da Av Inglaterra", "Igapo",
    "Jardim Piza", "Parque Guanabara", "Bela Suica", "Jardim Shangri La"
]

pages_number = int(input('Quantas paginas? (Enter 0 to scrape until the end) '))
tic = time.time()

# First part of neighborhoods
# link_imovel1, address1, neighbor1, area1, tipo1, room1, bath1, park1, price1 = scrape_data_viva_real(pages_number, price_range, property_types, num_bedrooms, num_bathrooms, min_area, max_area, num_parking_slots, neighborhoods_part1)

# # Second part of neighborhoods
# link_imovel2, address2, neighbor2, area2, tipo2, room2, bath2, park2, price2 = scrape_data_viva_real(pages_number, price_range, property_types, num_bedrooms, num_bathrooms, min_area, max_area, num_parking_slots, neighborhoods_part2)

# # Combine the results
# link_imovel = link_imovel1 + link_imovel2
# address = address1 + address2
# neighbor = neighbor1 + neighbor2
# area = area1 + area2
# tipo = tipo1 + tipo2
# room = room1 + room2
# bath = bath1 + bath2
# park = park1 + park2
# price = price1 + price2

link_imovel, address, neighbor, area, tipo, room, bath, park, price = scrape_data_olx(pages_number, price_range, property_types, num_bedrooms, num_bathrooms, min_area, max_area, num_parking_slots, neighborhoods_part1)

header_written = False
data_list = []
print(len(neighbor))
# Combine the results
for i in range(0, len(link_imovel)):
    combinacao = {
        'Link': link_imovel[i],
        'Address': address[i],
        'Neighbor': neighbor[i],
        'Area': area[i],
        'Type': tipo[i],
        'Rooms': room[i],
        'Bathrooms': bath[i],
        'Parking': park[i],
        'Price': price[i]
    }
    data_list.append(combinacao)
print(data_list)
df = pd.DataFrame(data_list)
df.to_csv('Olx.csv', sep=';', encoding='utf-8-sig', index=False) 

# Tempo de execução
toc = time.time()
get_time=round(toc-tic,3)
print('Finished in ' + str(get_time) + ' seconds')
print(str(len(price))+' results!')
