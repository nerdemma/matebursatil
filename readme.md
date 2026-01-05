# Mercados y Valores Argentinos

Una Web API para obtener las últimas cotizaciones del mercado bursátil argentino. Diseñada para ser consumida desde cualquier cliente HTTP (curl, Postman, aplicaciones web, herramientas de línea de comandos, etc.).

## Descripción
La aplicación extrae cotizaciones públicas mediante técnicas de scraping (Beautiful Soup y expresiones regulares) y las expone a través de una API REST. Está implementada principalmente en Python, con scripts auxiliares en Bash cuando corresponde. El resultado se puede devolver directamente en JSON o almacenarse localmente para consultas posteriores.

## Características
- Endpoints simples para consultar cotizaciones por ticker.
- Respuesta en JSON lista para ser consumida por cualquier cliente.
- Posibilidad de ejecutar scrapers periódicos (scheduler opcional).
- Scripts auxiliares para tareas puntuales (opcional).

## Requisitos
- Python 3.8+
- pip
- Dependencias listadas en requirements.txt (BeautifulSoup, requests, etc.)

## Instalación
1. Clonar el repositorio:
    git clone <repo-url>
2. Entrar al proyecto e instalar dependencias:
    cd <repo>
    pip install -r requirements.txt

## Ejecución
Arrancar la API (ejemplo con FastAPI + uvicorn):
uvicorn main:app --host 0.0.0.0 --port 8000

(O sciptear el arranque según la implementación incluida en el repo, p. ej. run.sh o app.py)

## Uso (ejemplos)
- Obtener cotización de GGAL con curl:
  curl -s "http://localhost:8000/quote/GGAL"

- Usar Postman:
  Hacer una petición GET al endpoint /quote/{ticker} con el ticker deseado.

Ejemplo de respuesta:
{
  "ticker": "GGAL",
  "nombre": "Banco Galicia y Buenos Aires",
  "precio": 123.45,
  "moneda": "ARS",
  "fecha": "2026-01-05T12:34:56Z",
  "fuente": "nombre_de_fuente"
}

Si no se encuentra la cotización, la API devolverá un 404 o un cuerpo JSON con mensaje: "No encontrado".

## Endpoints (ejemplo)
- GET /quote/{ticker} — devuelve la última cotización para el ticker.
- GET /health — estado de la aplicación.
(Ajustar según el diseño real de la API en el proyecto.)

## Ejecución periódica (opcional)
Si necesita actualizaciones automáticas, puede usar un scheduler externo (cron, systemd timers, o un job interno). La aplicación no requiere ejecutarse en entorno Unix exclusivo: puede desplegarse en servidores, contenedores o plataformas en la nube.

## Contribuciones
PRs y issues bienvenidos. Indique el propósito del cambio y añada pruebas cuando corresponda.

## Renuncia de responsabilidad
Esta aplicación tiene fines educativos e informativos y no constituye asesoramiento financiero, legal ni de inversión. No se garantiza la exactitud o integridad de los datos. El uso es bajo su propio riesgo; consulte con un profesional antes de tomar decisiones financieras.


