from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
import os
from datetime import datetime

from api.models import Cotizacion, CotizacionList
from services.storage import JSONStorage
from services.scraper import obtener_informe_merval


router = APIRouter()


def get_storage() -> JSONStorage:
    # default path; in a more advanced setup this would be injected/configured
    return JSONStorage('data/cotizaciones.json')


@router.get('/')
def list_shares(limit: int = 200, q: str = '', storage: JSONStorage = Depends(get_storage)) -> Dict[str, Any]:
    """Return a JSON object with `items` and non-breaking `meta` metadata so
    the dashboard can consume summary info without frontend changes.
    """
    items = storage.read_all()
    if q:
        q_lower = q.lower()
        items = [i for i in items if q_lower in (i.get('ticker', '') + i.get('nombre', '')).lower()]

    sliced = items[:limit]

    # metadata: total count and last update timestamp (from file mtime when available)
    meta: Dict[str, Any] = {'totalCount': len(items)}
    try:
        path = storage.path
        if os.path.exists(path):
            mtime = os.path.getmtime(path)
            meta['last_updated'] = datetime.fromtimestamp(mtime).isoformat()
    except Exception:
        # don't fail the request if metadata cannot be computed
        pass

    return {'items': sliced, 'meta': meta}


@router.get('/{ticker}', response_model=Cotizacion)
def get_share(ticker: str, storage: JSONStorage = Depends(get_storage)):
    item = storage.find_by_ticker(ticker)
    if not item:
        raise HTTPException(status_code=404, detail='No encontrado')
    return item


