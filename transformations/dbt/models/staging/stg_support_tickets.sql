select
    ticket_id,
    customer_id,
    opened_date,
    priority,
    status,
    issue_category
from {{ source('raw', 'support_tickets') }}

