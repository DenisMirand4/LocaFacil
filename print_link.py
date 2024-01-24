neighborhoods = ["Antares", "Aeroporto"]

neighborhood_filter = ""
for neighborhood in neighborhoods:
    neighborhood_filter += f',Paran%C3%A1,Londrina,Bairros,{neighborhood},,,neighborhood,BR%3EParana%3ENULL%3ELondrina%3EBarrios%3E{neighborhood},,,;'
neighborhood_filter = neighborhood_filter[:-1]
link = f'onde=Brasil,Paran%C3%A1,Londrina,,,,,,BR%3EParana%3ENULL%3ELondrina,,,;{neighborhood_filter}'
print(link)