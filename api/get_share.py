#!/usr/bin/python3

import json
import requests
from bs4 import BeautifulSoup

def obtener_informe_merval(url):
	try:
		response = requests.get(url)
		response.raise_for_status()
		soup = BeautifulSoup(response.content, 'html.parser')
	except requests.exceptions.RequestException as e:
		print(f"Error al acceder a la URL: {e}")
		return []
	
	data = []
	rows = soup.select('table.table tbody tr')
	print(f"Total de filas encontradas: {len(rows)}")

	for i, row in enumerate(rows):
		try:
			cols = row.find_all('td')
			if len(cols) < 9:
				print(f"Fila {i} no tiene suficientes columnas, se omite.")
				continue

			stock = {
			'ticker' : cols[0].find('a').text.strip(),
			'nombre' : cols[0].find('p').text.strip(),
			'cotizacion' : cols[1].text.strip(),
			'variacion' : cols[2].text.strip(),
			'volumen' : cols[3].text.strip(),
			'precio_apertura' : cols[4].text.strip(),
			'baja' :  cols[5].text.strip(),
			'alta' : cols[6].text.strip(),
			'precio_cierre' : cols[7].text.strip(),
			'fecha_cierre' : cols[8].text.strip()		
			}
				
			data.append(stock)
			
		except Exception as e:
			print(f"Error en fila {i}: {e}")

	return data

#solucionar el problema con el protocolo https puerto 443
if __name__ == "__main__":
	#url = "http://localhost/share"
	url = "https://www.portfoliopersonal.com/Cotizaciones/Acciones"
	json_data = obtener_informe_merval(url)

	if json_data:
		with open('../data/cotizaciones.json', 'w', encoding='utf-8') as f:
			json.dump(json_data, f, ensure_ascii=False, indent=2)
			print(f"{len(json_data)} cotizaciones exportadas a cotizaciones.json")
	else:
		print("No se pudo obtener ningún dato.")
