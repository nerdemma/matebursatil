import requests
from bs4 import BeautifulSoup
from typing import List, Dict


def obtener_informe_merval(url: str, timeout: int = 10) -> List[Dict]:
	"""Obtiene las cotizaciones desde la URL dada y devuelve una lista de dicts.

	Lanza requests.exceptions.RequestException si falla la petición.
	"""
	response = requests.get(url, timeout=timeout)
	response.raise_for_status()
	soup = BeautifulSoup(response.content, 'html.parser')

	data = []
	rows = soup.select('table.table tbody tr')

	for i, row in enumerate(rows):
		cols = row.find_all('td')
		if len(cols) < 9:
			# fila inesperada
			continue

		try:
			ticker_el = cols[0].find('a')
			nombre_el = cols[0].find('p')

			stock = {
				'ticker': ticker_el.text.strip() if ticker_el else cols[0].text.strip(),
				'nombre': nombre_el.text.strip() if nombre_el else '',
				'cotizacion': cols[1].text.strip(),
				'variacion': cols[2].text.strip(),
				'volumen': cols[3].text.strip(),
				'precio_apertura': cols[4].text.strip(),
				'baja': cols[5].text.strip(),
				'alta': cols[6].text.strip(),
				'precio_cierre': cols[7].text.strip(),
				'fecha_cierre': cols[8].text.strip(),
			}
			data.append(stock)
		except Exception:
			# skip malformed rows
			continue

	return data


if __name__ == '__main__':
	url = 'https://www.portfoliopersonal.com/Cotizaciones/Acciones'
	try:
		result = obtener_informe_merval(url)
		import json

		# Preferir almacenar en la base de datos. Si no está configurada, hacer
		# fallback a JSON para no perder los datos.
		try:
			from services.db import PostgresStorage
			storage = PostgresStorage()
			storage.write_all(result)
			print(f"{len(result)} cotizaciones guardadas en la base de datos")
		except Exception as db_err:
			# Si ocurre un error al usar la DB, escribir en el archivo JSON como
			# fallback y mostrar la excepción para diagnóstico.
			with open('data/cotizaciones.json', 'w', encoding='utf-8') as f:
				json.dump(result, f, ensure_ascii=False, indent=2)
			print('No fue posible guardar en la base de datos:', db_err)
			print(f"{len(result)} cotizaciones exportadas a data/cotizaciones.json (fallback)")
	except Exception as e:
		print('Error al obtener cotizaciones:', e)
