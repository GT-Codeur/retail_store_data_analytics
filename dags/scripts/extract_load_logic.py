"""
    Auteur: Germain Tegomo
    Description: Ce module permet d'extraire les données d'un fichier json,
    créer une table et y sauvegarder les données du fichier json.
    L'utilisation de la librairie psycopg2 est le choix ideal pour cette tache
    vu le gros de volume de donnees a traiter, elle traite tres rapidement les requetes
    a la difference du PostgresHook.
    La diiference est abyssale: quelques secondes contre pres de 15 minutes

    J'ai utiliser la methode extract load pour ingerer plus rapidement le gros
    volume de donnees de la source et eviter les problemes lies a la memoire avec xcom
"""
import json
from typing import Any
from psycopg2.extensions import connection

def extract_from_json(file_path: str) -> None:
    """
        Description: Cette function ouvre le fichier en lecture et extrait les données
        Parameter: str
        Return: None
    """
    with open(file_path, 'r', encoding='utf-8') as stream:
        return json.load(stream)

def load_to_exploded_tbl(conn_db: connection, data: list[dict[str, Any]]) -> None:
    """
        Description: Dans cette fonction, je load les donnees extrait du json dans ma base de donnee
                    postgresql
        Parameter: connection, list[dict[str, Any]]
        Return: None
    """
    try:
        with conn_db.cursor() as cur:
            cur.execute("TRUNCATE TABLE exploded_products;")
            for row in data:
                for product in row["products"]:
                    record = (
                        row["transaction_id"],
                        row["store_id"],
                        row["store_name"],
                        row["store_country"],
                        row["store_city"],
                        row["store_type"],
                        row["purchase_timestamp"],
                        row["payment_method"],
                        row["currency"],
                        row["total_amount"],
                        row["total_quantity_sold"],
                        row["discount_applied"],
                        row["return_status"],
                        product["product_id"],
                        product["product_name"],
                        product["products_category"],
                        product["quantity"],
                        product["price"]
                    )
                    cur.execute(
                        """
                            INSERT INTO exploded_products VALUES
                            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """, record)
            conn_db.commit()
    except Exception:
        conn_db.rollback()
        raise
    finally:
        conn_db.close()
