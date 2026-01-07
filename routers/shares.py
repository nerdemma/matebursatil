from fastapi import APIRouter, HTTPException, Depends
from typing import List
import os

from api.models import Cotizacion, CotizacionList
from services.storage import JSONStorage
from services.scraper import obtener_informe_merval


def _create_storage_from_env():
    """Factory: choose storage backend based on STORAGE env var.

    - STORAGE=json (default) -> JSONStorage('data/cotizaciones.json')
    - STORAGE=postgres -> PostgresStorage(DATABASE_URL)
    """
    storage_type = os.getenv('STORAGE', 'json').lower()
    if storage_type == 'postgres':
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            raise RuntimeError('DATABASE_URL not set for postgres storage')
        # import lazily so project can run without SQLAlchemy installed
        try:
            from services.db import PostgresStorage

            return PostgresStorage(db_url)
        except Exception as e:
            # re-raise as runtime error so FastAPI surfaces a clear message
            raise RuntimeError(f'failed to initialize PostgresStorage: {e}')
    return JSONStorage('data/cotizaciones.json')


router = APIRouter()


def get_storage() -> JSONStorage:
    # default path; in a more advanced setup this would be injected/configured
    return _create_storage_from_env()


@router.get('/', response_model=CotizacionList)
def list_shares(limit: int = 200, q: str = '', storage: JSONStorage = Depends(get_storage)):
    items = storage.read_all()
    if q:
        q_lower = q.lower()
        items = [i for i in items if q_lower in (i.get('ticker','') + i.get('nombre','')).lower()]
    return {'items': items[:limit]}


@router.get('/{ticker}', response_model=Cotizacion)
def get_share(ticker: str, storage: JSONStorage = Depends(get_storage)):
    item = storage.find_by_ticker(ticker)
    if not item:
        raise HTTPException(status_code=404, detail='No encontrado')
    return item


@router.post('/refresh')
def refresh(storage: JSONStorage = Depends(get_storage)):
    url = 'https://www.portfoliopersonal.com/Cotizaciones/Acciones'
    try:
        data = obtener_informe_merval(url)
        if not data:
            raise HTTPException(status_code=503, detail='No data from scraper')
        storage.write_all(data)
        return {'imported': len(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
