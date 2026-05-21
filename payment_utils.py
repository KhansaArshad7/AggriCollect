# payment_utils.py - Payment distribution (pro-rata and equal)
import pandas as pd

def distribute_payment_pro_rata(farmers, total_payment, crop_type=None):
    """Distribute based on land acres (for given crop or all farmers)"""
    df = pd.DataFrame(farmers)
    if crop_type:
        df = df[df["crop"] == crop_type].copy()
    if df.empty:
        return {}
    total_land = df["land_acres"].sum()
    distribution = {}
    for _, row in df.iterrows():
        share = (row["land_acres"] / total_land) * total_payment
        distribution[row["id"]] = round(share, 2)
    return distribution

def distribute_payment_equal(farmers, total_payment, crop_type=None):
    """Equal distribution among all farmers (or crop-specific)"""
    df = pd.DataFrame(farmers)
    if crop_type:
        df = df[df["crop"] == crop_type].copy()
    if df.empty:
        return {}
    count = len(df)
    each_share = total_payment / count
    distribution = {row["id"]: round(each_share, 2) for _, row in df.iterrows()}
    return distribution

def update_farmer_dues(farmers, distribution):
    for farmer in farmers:
        if farmer["id"] in distribution:
            farmer["payment_due"] += distribution[farmer["id"]]
    return farmers