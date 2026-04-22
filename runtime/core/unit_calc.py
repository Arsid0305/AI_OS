def calculate_unit_economics(
    price,
    cogs,
    commission_percent,
    logistics,
    traffic,
    cvr,
    ad_percent=None,
):
    """
    Strict numerical unit economics calculator.
    All percents must be passed as numbers like 15 for 15%.
    CVR must be passed as decimal (e.g., 0.074 for 7.4%).
    """

    # --- Sales ---
    sales = traffic * cvr

    # --- Revenue ---
    revenue = sales * price

    # --- Commission ---
    commission_per_unit = price * (commission_percent / 100)

    # --- Advertising ---
    if ad_percent is None:
        ad_cost_per_unit = 0
    else:
        ad_cost_per_unit = price * (ad_percent / 100)

    # --- Unit Contribution ---
    unit_contribution = (
        price
        - commission_per_unit
        - cogs
        - logistics
        - ad_cost_per_unit
    )

    # --- Monthly Contribution ---
    monthly_contribution = unit_contribution * sales

    return {
        "sales_units": round(sales, 2),
        "revenue": round(revenue, 2),
        "commission_per_unit": round(commission_per_unit, 2),
        "ad_cost_per_unit": round(ad_cost_per_unit, 2),
        "unit_contribution": round(unit_contribution, 2),
        "monthly_contribution": round(monthly_contribution, 2),
    }