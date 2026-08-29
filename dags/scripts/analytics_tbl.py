"""
    Auteur: Germain Tegomo
    Description: Ce module permet de créer la table store_sales_summary à
                partir la table exploded_data.
"""

from psycopg2.extensions import connection

def t_store_sales_summary(conn_db: connection) -> None:
    """
        Description: creer la table store_sales_summary a partir de la table exploded_products
        Parameter: connection
        Return: None
    """
    try:
        with conn_db.cursor() as cur:

            cur.execute(
                """
                    DROP TABLE IF EXISTS store_sales_summary;
                    CREATE TABLE store_sales_summary AS
                    WITH unique_store_sales AS (
                        SELECT DISTINCT 
                            store_id, 
                            store_name, 
                            store_country, 
                            store_city, 
                            store_type,
                            total_amount,
                            total_quantity_sold
                        FROM exploded_products
                    )
                    SELECT 
                        store_id, 
                        store_name, 
                        store_country, 
                        store_city, 
                        store_type,
                        SUM(total_amount) OVER (PARTITION BY store_id) AS total_sales_amount,
                        SUM(total_quantity_sold) OVER (PARTITION BY store_id) AS total_quantity_sold
                    FROM unique_store_sales;

                """
            )

            conn_db.commit()
    except Exception:
        conn_db.rollback()
        raise
    finally:
        conn_db.close()

def daily_sales_country_currency(conn_db: connection) -> None:
    """
        Description: creer la table daily_sales_country_currency a partir
                    de la table exploded_products.
        Parameter: connection
        Return: None
    """
    try:
        with conn_db.cursor() as cur:

            cur.execute(
                """
                    DROP TABLE IF EXISTS daily_sales_country_currency;
                    CREATE TABLE daily_sales_country_currency AS
                    WITH unique_sales AS (
                        SELECT DISTINCT transaction_id, purchase_timestamp::DATE AS purchase_date,
                                        total_amount, discount_applied, store_country, currency
                        FROM exploded_products
                    )
                    SELECT purchase_date, store_country, currency,
                        SUM(ROUND((total_amount-discount_applied)::NUMERIC, 2)) 
                        OVER (PARTITION BY purchase_date) AS daily_total_sales,
                        COUNT(transaction_id) OVER 
                        (PARTITION BY purchase_date) AS number_of_transactions,
                        ROUND(AVG((total_amount - discount_applied)::numeric) 
                        OVER (PARTITION BY purchase_date), 2) AS average_transaction_value
                    FROM unique_sales;
                """
            )

            conn_db.commit()

    except Exception:
        conn_db.rollback()
        raise

    finally:
        conn_db.close()

def payment_method_analysis(conn_db: connection) -> None:
    """
        Description: creer la table payment_method_analysis a partir
                    de la table exploded_products.
        Parameter: connection
        Return: None
    """
    try:
        with conn_db.cursor() as cur:

            cur.execute(
                """
                    DROP TABLE IF EXISTS payment_method_analysis;
                    CREATE TABLE payment_method_analysis AS
                    WITH sales AS(
                        SELECT DISTINCT transaction_id, payment_method, total_amount, 
                                total_quantity_sold, discount_applied, return_status
                        FROM exploded_products
                        )
                    SELECT payment_method, COUNT(transaction_id) AS total_transactions, 
                    ROUND(SUM(total_amount-discount_applied)::NUMERIC, 2) AS total_sales_amount,
                    ROUND(AVG(discount_applied)::NUMERIC, 2) AS average_discount, 
                    ROUND(COUNT(transaction_id) FILTER (WHERE return_status = 'Returned')::NUMERIC / 
                    COUNT(transaction_id) * 100, 2) AS return_rate,
                    ROUND(AVG(total_quantity_sold)::NUMERIC, 2) AS average_items_per_transaction
                    FROM sales GROUP BY payment_method;
                """
            )

            conn_db.commit()

    except Exception:
        conn_db.rollback()
        raise

    finally:
        conn_db.close()
