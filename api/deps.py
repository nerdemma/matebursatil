from pathlib import Path
import json
from functools import lru_cache
from typing import Dict, Any
from pydantic import BaseSettings, Field
from fastapi import Depends

# /home/emmanuel/projects/matebursatil/api/deps.py
# Dependencias y configuración mediante variables de entorno


# Configuración via ENV (leer .env automáticamente si existe)
class Settings(BaseSettings):
    # Ruta al JSON (puede ser absoluta o relativa al proyecto)
    json_path: Path = Field(Path("data/data.json"), env="MATEBURSATIL_JSON_PATH")
    # Entorno de la aplicación: development / production / test
    env: str = Field("development", env="MATEBURSATIL_ENV")
    # Si true, recarga el JSON en cada petición (útil para desarrollo)
    reload_json: bool = Field(False, env="MATEBURSATIL_RELOAD_JSON")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Cachea la instancia de settings para usarla como dependencia
@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Función interna que lee el JSON (sin dependencias de FastAPI)
def _read_json_file(path: Path) -> Dict[str, Any]:
    p = path if path.is_absolute() else Path.cwd() / path
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


# Cachea por ruta de archivo para evitar leer disco en cada petición (salvo reload)
@lru_cache(maxsize=32)
def _read_json_cached(path_str: str) -> Dict[str, Any]:
    return _read_json_file(Path(path_str))


# Dependencia de FastAPI que devuelve el contenido del JSON según la configuración
def get_json_data(settings: Settings = Depends(get_settings)) -> Dict[str, Any]:
    """
    Devuelve el JSON configurado en settings.json_path.
    Si settings.reload_json es True fuerza lectura desde disco.
    """
    json_path = settings.json_path
    if settings.reload_json:
        return _read_json_file(json_path)
    return _read_json_cached(str(json_path))


# Ejemplo de uso en FastAPI:
# from fastapi import APIRouter
# router = APIRouter()
#
# @router.get("/items")
# def read_items(data: dict = Depends(get_json_data)):
#     return data