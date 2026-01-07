from typing import List, Dict, Optional
import os
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class CotizacionModel(Base):
    __tablename__ = 'cotizaciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(64), unique=True, index=True, nullable=False)
    nombre = Column(Text)
    cotizacion = Column(Text)
    variacion = Column(Text)
    volumen = Column(Text)
    precio_apertura = Column(Text)
    baja = Column(Text)
    alta = Column(Text)
    precio_cierre = Column(Text)
    fecha_cierre = Column(Text)


class PostgresStorage:
    """Simple synchronous Postgres storage using SQLAlchemy ORM.

    Methods mirror the JSONStorage interface used by the app: read_all,
    write_all, find_by_ticker.
    """

    def __init__(self, db_url: Optional[str] = None):
        db_url = db_url or os.getenv('DATABASE_URL')
        if not db_url:
            raise RuntimeError('DATABASE_URL is not set')

        self.engine = create_engine(db_url, future=True)
        self.Session = sessionmaker(bind=self.engine)
        # create tables if they don't exist
        Base.metadata.create_all(self.engine)

    def read_all(self) -> List[Dict]:
        session = self.Session()
        try:
            rows = session.query(CotizacionModel).all()
            return [
                {
                    'ticker': r.ticker,
                    'nombre': r.nombre,
                    'cotizacion': r.cotizacion,
                    'variacion': r.variacion,
                    'volumen': r.volumen,
                    'precio_apertura': r.precio_apertura,
                    'baja': r.baja,
                    'alta': r.alta,
                    'precio_cierre': r.precio_cierre,
                    'fecha_cierre': r.fecha_cierre,
                }
                for r in rows
            ]
        finally:
            session.close()

    def write_all(self, items: List[Dict]) -> None:
        session = self.Session()
        try:
            # simple strategy: delete all and bulk-insert
            session.query(CotizacionModel).delete()
            for it in items:
                obj = CotizacionModel(
                    ticker=it.get('ticker', ''),
                    nombre=it.get('nombre', ''),
                    cotizacion=it.get('cotizacion', ''),
                    variacion=it.get('variacion', ''),
                    volumen=it.get('volumen', ''),
                    precio_apertura=it.get('precio_apertura', ''),
                    baja=it.get('baja', ''),
                    alta=it.get('alta', ''),
                    precio_cierre=it.get('precio_cierre', ''),
                    fecha_cierre=it.get('fecha_cierre', ''),
                )
                session.add(obj)
            session.commit()
        finally:
            session.close()

    def find_by_ticker(self, ticker: str) -> Optional[Dict]:
        session = self.Session()
        try:
            # case-insensitive match
            q = session.query(CotizacionModel).filter(CotizacionModel.ticker.ilike(ticker))
            r = q.first()
            if not r:
                return None
            return {
                'ticker': r.ticker,
                'nombre': r.nombre,
                'cotizacion': r.cotizacion,
                'variacion': r.variacion,
                'volumen': r.volumen,
                'precio_apertura': r.precio_apertura,
                'baja': r.baja,
                'alta': r.alta,
                'precio_cierre': r.precio_cierre,
                'fecha_cierre': r.fecha_cierre,
            }
        finally:
            session.close()
