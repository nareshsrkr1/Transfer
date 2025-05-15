UPDATE u
SET 
    u.CLIENT_TYPE = d.CLIENT_TYPE,
    u.CLIENT_SUBTTPE = d.CLIENT_SUBTTPE,
    u.TIER = d.TIER
FROM unfd_positions_dt u
JOIN dynamic_overrides_mapping d
    ON RTRIM(u.customer_legal_entity_name) = RTRIM(d.customer_legal_entity_name)
