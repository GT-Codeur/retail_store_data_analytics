"""
    Auteur: Germain Tegomo
    Description: Ce module permet de créer la table store_sales_summary à partir la table exploded_data
"""

from psycopg2.extensions import connection
from airflow.providers.postgres.hooks.postgres import PostgresHook

def t_store_sales_summary(conn_db: connection) -> None:
    """
        Description: creer la table store_sales_summary a partir de la table exploded_products
        Parameter: None
        Return: None
    """
    try:
        with conn_db.cursor() as cur:

            cur.execute(
                """
                    DROP TABLE IF EXISTS store_sales_summary;
                    CREATE TABLE store_sales_summary AS
                    SELECT store_id, store_name, store_country, store_city, store_type,
                        SUM(total_amount) AS total_sales_amount,
                        SUM(total_quantity_sold) AS total_quantity_sold
                    FROM exploded_products
                    GROUP BY store_id, store_name, store_country, store_city, store_type;
                """
            )

            conn_db.commit()
    except Exception:
        conn_db.rollback()
        raise
    finally:
        conn_db.close()
