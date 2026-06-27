CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS curated;
CREATE SCHEMA IF NOT EXISTS governance;

CREATE TABLE IF NOT EXISTS raw.customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(30),
    region VARCHAR(50) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    signup_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    product_category VARCHAR(50) NOT NULL,
    list_price NUMERIC(12, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.sales_orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL REFERENCES raw.customers(customer_id),
    product_id VARCHAR(20) NOT NULL REFERENCES raw.products(product_id),
    order_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    net_amount NUMERIC(12, 2) NOT NULL,
    sales_channel VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.support_tickets (
    ticket_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL REFERENCES raw.customers(customer_id),
    opened_date DATE NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(30) NOT NULL,
    issue_category VARCHAR(80) NOT NULL
);

CREATE TABLE IF NOT EXISTS governance.data_assets (
    asset_id VARCHAR(80) PRIMARY KEY,
    asset_name VARCHAR(120) NOT NULL,
    schema_name VARCHAR(80) NOT NULL,
    asset_type VARCHAR(50) NOT NULL,
    owner_name VARCHAR(100) NOT NULL,
    business_domain VARCHAR(80) NOT NULL,
    contains_pii BOOLEAN NOT NULL DEFAULT FALSE,
    trust_score INTEGER NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS governance.business_glossary (
    term_id VARCHAR(80) PRIMARY KEY,
    term_name VARCHAR(120) NOT NULL,
    definition TEXT NOT NULL,
    owner_name VARCHAR(100) NOT NULL,
    related_asset_id VARCHAR(80) REFERENCES governance.data_assets(asset_id)
);

