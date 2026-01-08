import os
import json
from sqlalchemy import create_engine, text


def main():
    db_url = os.getenv('DATABASE_URL', 'sqlite+pysqlite:///./matebursatil.db')
    engine = create_engine(db_url, future=True)

    with engine.connect() as conn:
        # Count rows
        try:
            r = conn.execute(text('SELECT COUNT(*) as cnt FROM cotizaciones'))
            cnt = r.scalar_one()
        except Exception as e:
            print('Error al contar filas en cotizaciones:', e)
            return

        print(f'Filas en tabla cotizaciones: {cnt}')

        # Fetch first 10 rows from current snapshot
        r = conn.execute(text('SELECT ticker, nombre, cotizacion, fecha_cierre FROM cotizaciones ORDER BY id LIMIT 10'))
        # SQLAlchemy Row is not directly a dict in all versions; use the mapping view
        rows = [dict(row._mapping) for row in r]
        print('\nPrimeros registros (hasta 10):')
        print(json.dumps(rows, ensure_ascii=False, indent=2))

        # Also show history table stats
        try:
            r2 = conn.execute(text('SELECT COUNT(*) FROM cotizaciones_history'))
            hist_cnt = r2.scalar_one()
            print(f'\nFilas en tabla cotizaciones_history: {hist_cnt}')

            r3 = conn.execute(text('SELECT ticker, nombre, cotizacion, fecha, hora FROM cotizaciones_history ORDER BY id DESC LIMIT 10'))
            rows3 = [dict(row._mapping) for row in r3]
            print('\nÚltimos registros en history (hasta 10):')
            print(json.dumps(rows3, ensure_ascii=False, indent=2))
        except Exception as e:
            print('No se pudo leer cotizaciones_history:', e)


if __name__ == '__main__':
    main()
