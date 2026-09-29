import os
from datetime import datetime, time as dt_time
from zoneinfo import ZoneInfo
from typing import Optional

from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from supabase import create_client, Client
from services.scraper import obtener_informe_merval
from routers.shares import router as shares_router

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
CRON_SECRET = os.getenv("CRON_SECRET")

SCRAPE_URL = 'https://www.portfoliopersonal.com/Cotizaciones/Acciones'
ARGENTINA_TZ = ZoneInfo("America/Argentina/Buenos_Aires")
MARKET_OPEN = dt_time(10, 0)
MARKET_CLOSE = dt_time(17, 0)

# Inicializamos el cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def market_is_open() -> bool:
    now = datetime.now(ARGENTINA_TZ)
    if now.weekday() >= 5:  # Sábado o Domingo
        return False
    return MARKET_OPEN <= now.time() <= MARKET_CLOSE


def create_app() -> FastAPI:
    app = FastAPI(title="MateBursatil API", version="0.1.0")

    # Montar estáticos
    static_mounts = [
        (os.path.join('templates', 'js'), '/js', 'js'),
        (os.path.join('templates', 'css'), '/css', 'css'),
        (os.path.join('templates', 'images'), '/images', 'images'),
    ]

    for directory, route, name in static_mounts:
        os.makedirs(directory, exist_ok=True)
        app.mount(route, StaticFiles(directory=directory), name=name)

    @app.get('/', include_in_schema=False)
    async def root():
        return FileResponse('templates/index.html')
    
    
    # Endpoint para probar manualmente la inserción en la DB desde el navegador/Postman
    @app.get('/api/test-scrape')
    async def test_scrape(ignore_market_hours: bool = True):
        now = datetime.now(ARGENTINA_TZ)

        # Si pasas ignore_market_hours=True (por defecto), forzamos la prueba sin importar la hora
        if not ignore_market_hours and not market_is_open():
            return {
                "status": "skipped",
                "message": f"Mercado cerrado ({now.strftime('%Y-%m-%d %H:%M:%S')})."
            }

        try:
            print("[Prueba] Iniciando scraping...")
            data = obtener_informe_merval(SCRAPE_URL)
            
            if data:
                print(f"[Prueba] Datos obtenidos ({len(data)} elementos). Insertando en Supabase...")
                response = supabase.table('cotizaciones').insert({"data": data}).execute()
                
                return {
                    "status": "success",
                    "inserted_records": len(data),
                    "supabase_response": response.data,
                    "timestamp": now.strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                return {"status": "error", "message": "No se obtuvieron datos del scraper."}

        except Exception as e:
            print(f"[Prueba] Error: {e}")
            raise HTTPException(status_code=500, detail=f"Error al conectar/guardar en Supabase: {str(e)}")

    app.include_router(shares_router, prefix='/shares')
    return app

app = create_app()