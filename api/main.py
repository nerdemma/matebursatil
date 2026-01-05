from fastapi import FastAPI
from routers.shares import router as shares_router


def create_app() -> FastAPI:
    app = FastAPI(title="MateBursatil API", version="0.1.0")

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    app.include_router(shares_router, prefix='/shares')
    return app


app = create_app()
