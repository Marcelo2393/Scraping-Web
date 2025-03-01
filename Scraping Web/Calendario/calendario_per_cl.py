import requests
from lxml import html
import csv

def scrape_feriados(url):
    response = requests.get(url)
    if response.status_code == 200:
        feriados = []
        tree = html.fromstring(response.content)
        tables = tree.xpath("/html/body/div[1]/div[5]/div[1]/div/div[1]/div/div[13]/div[1]/table")
        for table in tables:
            rows = table.xpath(".//tr")
            for row in rows:
                cols = row.xpath(".//td")
                if len(cols) == 3:
                    fecha = cols[0].text.strip()
                    mes = cols[1].text.strip()
                    nombre = cols[2].text.strip()
                    feriado = {
                        "fecha": fecha + " " + mes,
                        "nombre": nombre
                    }
                    feriados.append(feriado)
        return feriados
    else:
        print("Error al obtener la página:", response.status_code)
        return []

# Obtener feriados para cada año
feriados = []

# Definir los URLs de cada año para Chile
urls_chile = {
    2018: "https://www.cuandoenelmundo.com/calendario/chile/2018",
    2019: "https://www.cuandoenelmundo.com/calendario/chile/2019",
    2020: "https://www.cuandoenelmundo.com/calendario/chile/2020",
    2021: "https://www.cuandoenelmundo.com/calendario/chile/2021",
    2022: "https://www.cuandoenelmundo.com/calendario/chile/2022",
    2023: "https://www.cuandoenelmundo.com/calendario/chile/2023",
    2024: "https://www.cuandoenelmundo.com/calendario/chile/2024",
    2025: "https://www.cuandoenelmundo.com/calendario/chile/2025",
    2026: "https://www.cuandoenelmundo.com/calendario/chile/2026"
}

# Definir los URLs de cada año para Perú
urls_peru = {
    2018: "https://www.cuandoenelmundo.com/calendario/peru/2018",
    2019: "https://www.cuandoenelmundo.com/calendario/peru/2019",
    2020: "https://www.cuandoenelmundo.com/calendario/peru/2020",
    2021: "https://www.cuandoenelmundo.com/calendario/peru/2021",
    2022: "https://www.cuandoenelmundo.com/calendario/peru/2022",
    2023: "https://www.cuandoenelmundo.com/calendario/peru/2023",
    2024: "https://www.cuandoenelmundo.com/calendario/peru/2024",
    2025: "https://www.cuandoenelmundo.com/calendario/peru/2025",
    2026: "https://www.cuandoenelmundo.com/calendario/peru/2026"
}

# Obtener feriados para cada año y agregarlos a la lista para Chile
for year, url in urls_chile.items():
    feriados.append({"país": "Chile", "año": year, "feriados": scrape_feriados(url)})

# Obtener feriados para cada año y agregarlos a la lista para Perú
for year, url in urls_peru.items():
    feriados.append({"país": "Perú", "año": year, "feriados": scrape_feriados(url)})

# Escribir los feriados en un archivo CSV
with open("feriados_chile_peru.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["País", "Año", "Fecha", "Nombre"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for feriados_pais in feriados:
        pais, year, feriados = feriados_pais["país"], feriados_pais["año"], feriados_pais["feriados"]
        for feriado in feriados:
            fecha, nombre = feriado["fecha"], feriado["nombre"]
            writer.writerow({"País": pais, "Año": year, "Fecha": fecha, "Nombre": nombre})