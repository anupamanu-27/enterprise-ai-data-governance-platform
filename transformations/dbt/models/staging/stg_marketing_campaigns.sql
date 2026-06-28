select
    campaign_id,
    campaign_name,
    channel,
    region,
    budget,
    start_date,
    end_date,
    owner_name
from {{ source('raw', 'marketing_campaigns') }}

