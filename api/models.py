from typing import List
from pydantic import BaseModel


class Cotizacion(BaseModel):
	ticker: str
	nombre: str
	cotizacion: str
	variacion: str
	volumen: str
	precio_apertura: str
	baja: str
	alta: str
	precio_cierre: str
	fecha_cierre: str


class CotizacionList(BaseModel):
	items: List[Cotizacion]
