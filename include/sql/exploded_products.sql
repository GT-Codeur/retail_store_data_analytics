/*CREATION DE LA TABLE EXPLODED_PRODUCT*/

CREATE TABLE IF NOT EXISTS exploded_products(
    transaction_id VARCHAR(20),
    store_id VARCHAR(20),
    store_name VARCHAR(50),
    store_country VARCHAR(50),
    store_city VARCHAR(50),
    store_type VARCHAR(50),
    purchase_timestamp timestamp,
    payment_method VARCHAR(50),
    currency VARCHAR(50),
    total_amount FLOAT,
    total_quantity_sold INT,
    discount_applied FLOAT,
    return_status VARCHAR(50),
    product_id VARCHAR(50),
    product_name VARCHAR(50),
    products_category VARCHAR(50),
    quantity INT,
    price FLOAT
)