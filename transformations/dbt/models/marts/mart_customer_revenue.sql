with customer_revenue as (
    select
        c.customer_id,
        c.full_name,
        c.region,
        c.segment,
        count(distinct s.order_id) as order_count,
        sum(s.net_amount) as total_revenue,
        max(s.order_date) as latest_order_date
    from {{ ref('stg_customers') }} c
    left join {{ ref('stg_sales_orders') }} s
        on c.customer_id = s.customer_id
    group by
        c.customer_id,
        c.full_name,
        c.region,
        c.segment
)

select
    customer_id,
    full_name,
    region,
    segment,
    order_count,
    coalesce(total_revenue, 0) as total_revenue,
    latest_order_date,
    case
        when order_count > 0 then true
        else false
    end as is_active_customer
from customer_revenue

