select
    order_id,
    customer_id,
    product_id,
    order_date,
    quantity,
    net_amount,
    sales_channel
from {{ source('raw', 'sales_orders') }}

