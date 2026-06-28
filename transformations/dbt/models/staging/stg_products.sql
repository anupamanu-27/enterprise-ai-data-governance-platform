select
    product_id,
    product_name,
    product_category,
    list_price
from {{ source('raw', 'products') }}

