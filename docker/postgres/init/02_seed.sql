INSERT INTO raw.customers (
    customer_id,
    full_name,
    email,
    phone,
    region,
    segment,
    signup_date
) VALUES
    ('CUST-001', 'Aarav Mehta', 'aarav.mehta@example.com', '+91-90000-10001', 'West', 'Enterprise', '2024-01-15'),
    ('CUST-002', 'Priya Sharma', 'priya.sharma@example.com', '+91-90000-10002', 'North', 'Mid-Market', '2024-02-20'),
    ('CUST-003', 'Rohan Iyer', 'rohan.iyer@example.com', '+91-90000-10003', 'South', 'Enterprise', '2024-03-12'),
    ('CUST-004', 'Neha Kapoor', 'neha.kapoor@example.com', '+91-90000-10004', 'East', 'SMB', '2024-04-08')
ON CONFLICT (customer_id) DO NOTHING;

INSERT INTO raw.products (
    product_id,
    product_name,
    product_category,
    list_price
) VALUES
    ('PROD-001', 'Data Quality Monitor', 'Governance', 1200.00),
    ('PROD-002', 'Metadata Catalog Pro', 'Catalog', 2500.00),
    ('PROD-003', 'Lineage Explorer', 'Observability', 1800.00),
    ('PROD-004', 'PII Risk Scanner', 'Security', 1500.00)
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO raw.sales_orders (
    order_id,
    customer_id,
    product_id,
    order_date,
    quantity,
    net_amount,
    sales_channel
) VALUES
    ('ORD-001', 'CUST-001', 'PROD-002', '2025-01-10', 2, 5000.00, 'Direct'),
    ('ORD-002', 'CUST-002', 'PROD-001', '2025-01-18', 1, 1200.00, 'Partner'),
    ('ORD-003', 'CUST-003', 'PROD-003', '2025-02-05', 3, 5400.00, 'Direct'),
    ('ORD-004', 'CUST-001', 'PROD-004', '2025-02-11', 1, 1500.00, 'Direct'),
    ('ORD-005', 'CUST-004', 'PROD-001', '2025-03-02', 1, 1200.00, 'Marketplace')
ON CONFLICT (order_id) DO NOTHING;

INSERT INTO raw.support_tickets (
    ticket_id,
    customer_id,
    opened_date,
    priority,
    status,
    issue_category
) VALUES
    ('TCK-001', 'CUST-001', '2025-02-12', 'High', 'Resolved', 'Catalog search latency'),
    ('TCK-002', 'CUST-002', '2025-02-15', 'Medium', 'Open', 'Data quality rule setup'),
    ('TCK-003', 'CUST-003', '2025-03-01', 'High', 'Open', 'Lineage missing upstream job'),
    ('TCK-004', 'CUST-004', '2025-03-04', 'Low', 'Resolved', 'User access request')
ON CONFLICT (ticket_id) DO NOTHING;

INSERT INTO governance.data_assets (
    asset_id,
    asset_name,
    schema_name,
    asset_type,
    owner_name,
    business_domain,
    contains_pii,
    trust_score,
    description
) VALUES
    (
        'raw.customers',
        'Customers',
        'raw',
        'table',
        'Data Steward - Customer Domain',
        'Customer 360',
        TRUE,
        82,
        'Raw customer master data used for customer analytics, segmentation, and governance demonstrations.'
    ),
    (
        'raw.sales_orders',
        'Sales Orders',
        'raw',
        'table',
        'Revenue Analytics Lead',
        'Revenue',
        FALSE,
        88,
        'Raw sales order transactions used for revenue reporting and downstream analytics models.'
    ),
    (
        'raw.support_tickets',
        'Support Tickets',
        'raw',
        'table',
        'Customer Support Operations',
        'Support',
        FALSE,
        76,
        'Customer support cases used to connect operational experience with customer health and governance questions.'
    )
ON CONFLICT (asset_id) DO NOTHING;

INSERT INTO governance.business_glossary (
    term_id,
    term_name,
    definition,
    owner_name,
    related_asset_id
) VALUES
    (
        'term.active_customer',
        'Active Customer',
        'A customer with at least one paid order in the last 12 months.',
        'Revenue Analytics Lead',
        'raw.sales_orders'
    ),
    (
        'term.trust_score',
        'Trust Score',
        'A governance score from 0 to 100 based on freshness, completeness, validation results, ownership, and risk classification.',
        'Data Governance Office',
        'raw.customers'
    ),
    (
        'term.pii',
        'Personally Identifiable Information',
        'Data that can identify a person directly or indirectly, such as name, email, phone number, address, or customer identifier.',
        'Data Privacy Office',
        'raw.customers'
    )
ON CONFLICT (term_id) DO NOTHING;

