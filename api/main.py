from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from routers.shares import router as shares_router

import threading
import os
from typing import Optional

from datetime import datetime,  time as dt_time
from zoneinfo import ZoneInfo

from services.scraper import obtener_informe_merval
from services.storage import JSONStorage

# Configuracion
SCRAPE_URL = 'https://www.portfoliopersonal.com/Cotizaciones/Acciones'
SCRAPE_INTERVAL = 10 * 60  # 10 minutos
DATA_PATH = 'data/cotizaciones.json'
ARGENTINA_TZ = ZoneInfo("America/Argentina/Buenos_Aires") #zona horaria

MARKET_OPEN = dt_time(10,30) #horario de apertura
MARKET_CLOSE = dt_time(17,0) #horario de cierre


def market_is_open():
    now = datetime.now(ARGENTINA_TZ)

    if now.weekday() >=5:
        return False

    return MARKET_OPEN <= now.time() < MARKET_CLOSE


def _periodic_scrape(path: str, url: str, interval: int, stop_event: threading.Event) -> None:
    storage = JSONStorage(path)

    while not stop_event.is_set():
        if market_is_open():
            try:
                data = obtener_informe_merval(url)
                if data:
                    storage.write_all(data)
                    now = datetime.now(ARGENTINA_TZ)

                    print(
                        f"[scraper] Actualizado:"
                        f"{len(data)} cotizaciones guardadas en {path}"
                        f"({now.strftime('%Y-%m-%d %H:%M:%S')})"
                    )
                else:
                    print("[scraper] No se obtuvieron datos");

            except Exception as e:
                print(f"[scraper] Error en la actualizacion {e}")

        if stop_event.wait(interval):
            break

        else:
            print(
                f"[Scraper] Mercado cerrado"
                f"({now.strftime('%Y-%m-%d %H:%M:%S')})"
                f"Se conserva el ultimo JSON Disponible"
                )
            if stop_event.wait(60):
                break
                



def create_app() -> FastAPI:
    app = FastAPI(title="MateBursatil API", version="0.1.0")

    # Ensure data directory exists
    os.makedirs(os.path.dirname(DATA_PATH) or 'data', exist_ok=True)

    # Mount static asset directories (templates contains css/, js/, images/)
    static_mounts = [
        (os.path.join('templates', 'js'), '/js', 'js'),
        (os.path.join('templates', 'css'), '/css', 'css'),
        (os.path.join('templates', 'images'), '/images', 'images'),
    ]

    for directory, route, name in static_mounts:
        # create dir if missing to avoid runtime errors
        os.makedirs(directory, exist_ok=True)
        app.mount(route, StaticFiles(directory=directory), name=name)

    @app.get('/', include_in_schema=False)
    async def root():
        return FileResponse('templates/index.html')

    app.include_router(shares_router, prefix='/shares')
    return app


app = create_app()
