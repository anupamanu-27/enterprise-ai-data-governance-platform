select
    customer_id,
    full_name,
    email,
    phone,
    region,
    segment,
    signup_date
from {{ source('raw', 'customers') }}

