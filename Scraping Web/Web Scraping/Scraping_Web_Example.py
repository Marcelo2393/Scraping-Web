from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://peru.as.com/resultados/futbol/peru_apertura/clasificacion/?omnil=mpal'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

#Equipos 
eq = soup.find_all('span', class_='nombre-equipo')

equipos = list()


count = 0
for i in eq:
    if count<19:
        equipos.append(i.text)
    else:
        break
    count +=1

#Puntos 
pt = soup.find_all('td', class_='destacado')

puntos = list()


count = 0
for i in pt:
    if count<19:
        puntos.append(i.text)
    else:
        break
    count +=1

df = pd.DataFrame({'Nombre':equipos,'Puntos':puntos},index=list(range(1,20)))
print(df)

#df.to_csv('Clasificaciòn.csv',index=False)





