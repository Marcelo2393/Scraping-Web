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

def obtener_feriados(pais, urls):
    feriados = []
    for year, url in urls.items():
        feriados.append({"país": pais, "año": year, "feriados": scrape_feriados(url)})
    return feriados

def escribir_csv(feriados, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["País", "Año", "Fecha", "Nombre"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for feriados_pais in feriados:
            pais, year, feriados = feriados_pais["país"], feriados_pais["año"], feriados_pais["feriados"]
            for feriado in feriados:
                fecha, nombre = feriado["fecha"], feriado["nombre"]
                writer.writerow({"País": pais, "Año": year, "Fecha": fecha, "Nombre": nombre})

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

# Solicitar al usuario el país
pais = input("Ingrese el país del cual desea extraer los feriados (Chile o Perú): ").lower()

# Verificar la entrada del usuario y obtener los feriados correspondientes
if pais == "chile":
    feriados = obtener_feriados("Chile", urls_chile)
elif pais == "perú" or pais == "peru":
    feriados = obtener_feriados("Perú", urls_peru)
else:
    print("País no válido.")
    exit()

# Escribir los feriados en un archivo CSV
filename = f"feriados_{pais}.csv"
escribir_csv(feriados, filename)
print(f"Se han extraído los feriados de {pais.capitalize()} y se han guardado en el archivo {filename}.")