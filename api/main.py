from fastapi import FastAPI
from routers.shares import router as shares_router

import threading
import os
from typing import Optional

from services.scraper import obtener_informe_merval
from services.storage import JSONStorage

# Config
SCRAPE_URL = 'https://www.portfoliopersonal.com/Cotizaciones/Acciones'
SCRAPE_INTERVAL = 10 * 60  # seconds (10 minutes)
DATA_PATH = 'data/cotizaciones.json'


def _periodic_scrape(path: str, url: str, interval: int, stop_event: threading.Event) -> None:
    storage = JSONStorage(path)

    # Run once immediately
    try:
        data = obtener_informe_merval(url)
        if data:
            storage.write_all(data)
            print(f"[scraper] Inicial: {len(data)} cotizaciones guardadas en {path}")
        else:
            print("[scraper] Inicial: no se obtuvieron datos")
    except Exception as e:
        print(f"[scraper] Error inicial: {e}")

    # Periodic loop
    while not stop_event.wait(interval):
        try:
            data = obtener_informe_merval(url)
            if data:
                storage.write_all(data)
                print(f"[scraper] Actualizado: {len(data)} cotizaciones guardadas en {path}")
            else:
                print("[scraper] Actualizado: no se obtuvieron datos")
        except Exception as e:
            print(f"[scraper] Error en actualización: {e}")


def create_app() -> FastAPI:
    app = FastAPI(title="MateBursatil API", version="0.1.0")

    # Ensure data directory exists
    os.makedirs(os.path.dirname(DATA_PATH) or 'data', exist_ok=True)

    app.include_router(shares_router, prefix='/shares')
    return app


app = create_app()
