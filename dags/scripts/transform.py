"""
    Auteur: Germain Tegomo
    Description: Ce module permet de transformer les donnees extraits du fichier json
    et les stocker dans la table exploded_data
"""
from airflow.providers.postgres.hooks.postgres import PostgresHook

def transform_data(data: list[dict]) -> None:
    """
        Description: insère les donnees dans la table a partir des donnees du fichier json
        Parameter: str
        Return: None
    """

    postgres_hook = PostgresHook(
        postgres_conn_id = "postgresql_connection"
    )

    postgres_hook.run("TRUNCATE TABLE exploded_products;")

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
            postgres_hook.run(
                """INSERT INTO exploded_products 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
                parameters=record
            )
