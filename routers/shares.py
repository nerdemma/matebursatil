from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import os

from api.models import Cotizacion, CotizacionList
from supabase import create_client, Client

router = APIRouter()

# Variables de entorno para Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inicialización del cliente
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def _get_latest_record() -> Dict[str, Any]:
    """Función auxiliar para obtener la última captura de cotizaciones desde Supabase."""
    try:
        response = (
            supabase.table('cotizaciones')
            .select('data, created_at')
            .order('created_at', desc=True)
            .limit(1)
            .execute()
        )
        if response.data and len(response.data) > 0:
            return response.data[0]
    except Exception as e:
        print(f"[Supabase Error] Error al consultar cotizaciones: {e}")
    
    return {"data": [], "created_at": None}


@router.get('/')
def list_shares(limit: int = 200, q: str = '') -> Dict[str, Any]:
    """Retorna los ítems filtrados y la metadata correspondiente obtenida desde Supabase."""
    latest_record = _get_latest_record()
    items = latest_record.get('data', [])
    created_at = latest_record.get('created_at')

    # Filtrar por parámetro de búsqueda si existe (ticker o nombre)
    if q:
        q_lower = q.lower()
        items = [
            i for i in items 
            if q_lower in (i.get('ticker', '') + i.get('nombre', '')).lower()
        ]

    sliced = items[:limit]

    # Metadata de la última actualización
    meta: Dict[str, Any] = {
        'totalCount': len(items),
        'last_updated': created_at
    }

    return {'items': sliced, 'meta': meta}


@router.get('/cotizaciones')
async def get_cotizaciones():
    """Endpoint directo para devolver el array completo de cotizaciones actuales."""
    latest_record = _get_latest_record()
    return latest_record.get('data', [])


@router.get('/{ticker}', response_model=Cotizacion)
def get_share(ticker: str):
    """Busca una cotización específica por ticker dentro de la última actualización."""
    latest_record = _get_latest_record()
    items = latest_record.get('data', [])

    ticker_upper = ticker.upper()
    item = next((i for i in items if i.get('ticker', '').upper() == ticker_upper), None)

    if not item:
        raise HTTPException(status_code=404, detail='No encontrado')

    return item