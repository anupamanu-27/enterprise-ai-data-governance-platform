select
    asset_id,
    asset_name,
    business_domain,
    owner_name,
    contains_pii,
    trust_score,
    case
        when trust_score >= 85 then 'high_trust'
        when trust_score >= 70 then 'medium_trust'
        else 'needs_attention'
    end as trust_band
from governance.data_assets

