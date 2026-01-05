import json
import threading
from typing import List, Dict


class JSONStorage:
	"""Simple JSON file storage for cotizaciones.

	This is a lightweight wrapper around a JSON file that provides thread-safe
	read/write operations. It is intentionally simple to make swapping to a DB
	later straightforward.
	"""

	def __init__(self, path: str):
		self.path = path
		self._lock = threading.Lock()

	def read_all(self) -> List[Dict]:
		with self._lock:
			try:
				with open(self.path, 'r', encoding='utf-8') as f:
					return json.load(f)
			except FileNotFoundError:
				return []

	def write_all(self, items: List[Dict]) -> None:
		with self._lock:
			with open(self.path, 'w', encoding='utf-8') as f:
				json.dump(items, f, ensure_ascii=False, indent=2)

	def find_by_ticker(self, ticker: str) -> Dict:
		items = self.read_all()
		ticker_upper = ticker.upper()
		for it in items:
			if it.get('ticker', '').upper() == ticker_upper:
				return it
		return None
