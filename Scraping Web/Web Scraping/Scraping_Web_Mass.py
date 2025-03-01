#Librerías para Web Scrapping y Tratamiento de Datos
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd

#Obtener Fecha en Python - Para nombrar el archivo. 
from datetime import datetime
now = datetime.now()

## Inicio del Proceso Web Scrapping
#Invocación de chromedriver - Version /115.0.5790.102 /
driver = webdriver.Chrome("chromedriver.exe")

#URL
paginaScrapy = "https://www.tiendasmass.com.pe/ubicame/"

#Entrar a la página web
driver.get(paginaScrapy)

#Obtención del Contenido de la Página
contenido = driver.page_source

#Mejorando Legibilidad del Contenido con BeautifulSoup
soup = bs(contenido)

#Obtener la Ciudad de la Tienda MASS
data_ciudad = []
for tarjeta in soup.find_all("li", attrs={"data-ciudad":True}):
    data_ciudad.append(tarjeta["data-ciudad"])

#Obtener el Distrito de la Tienda MASS
data_distrito = []
for tarjeta in soup.find_all("li", attrs={"data-distrito":True}):
    data_distrito.append(tarjeta["data-distrito"])

#Obtener la Latitud de la Tienda MASS
data_latitud = []
for tarjeta in soup.find_all("li", attrs={"data-lat":True}):
    data_latitud.append(tarjeta["data-lat"])
#Obtener la longitud de la Tienda MASS
data_longitud = []
for tarjeta in soup.find_all("li", attrs={"data-lng":True}):
    data_longitud.append(tarjeta["data-lng"])

#Obtener el Nombre de la Tienda 
nombre_tienda = []
for tarjeta in soup.find_all("p", attrs={"class":"tienda-nombre"}):
    nombre_tienda.append(tarjeta.text)

#Obtener la Direccion de la Tienda
direccion_tienda = []
for tarjeta in soup.find_all("p", attrs={"class":"tienda-direccion"}):
    direccion_tienda.append(tarjeta.text)

#Diccionario para Consumirlo en DataFrame
#Existe un error de la propia página - se intercambia nombre con direccion
data = dict(nombre_tienda = direccion_tienda, direccion_tienda = nombre_tienda, ciudad = data_ciudad, distrito = data_distrito, latitud = data_latitud, longitud = data_longitud ) 

#Creamos el DataFrame
df = pd.DataFrame(data)

#Tratamiento de los Datos
df["latitud"] = df["latitud"].astype("float")
df["longitud"] = df["longitud"].astype("float")

#Obteniendo los datos en un Excel
df.to_excel(f'Direcciones_Tiendas_Mass_{now.strftime("%Y-%m-%d")}.xlsx',index=False)