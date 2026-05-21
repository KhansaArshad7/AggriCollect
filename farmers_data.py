# farmers_data.py - Farmer management logic
import random
import streamlit as st
from config import DEFAULT_FARMER_COUNT, MIN_LAND_ACRES, MAX_LAND_ACRES, CROP_OPTIONS

def generate_farmer(id, name_prefix="Kisan"):
    return {
        "id": id,
        "name": f"{name_prefix} {id}",
        "land_acres": round(random.uniform(MIN_LAND_ACRES, MAX_LAND_ACRES), 1),
        "crop": random.choice(CROP_OPTIONS),
        "joined": True,
        "payment_due": 0.0,
        "investment": round(random.uniform(5000, 50000), 0)  # optional contribution
    }

def get_default_farmers():
    farmers = []
    for i in range(1, DEFAULT_FARMER_COUNT + 1):
        farmers.append(generate_farmer(i))
    return farmers

def add_farmer(farmers):
    new_id = len(farmers) + 1
    farmers.append(generate_farmer(new_id))
    return farmers

def get_group_stats(farmers):
    import pandas as pd
    df = pd.DataFrame(farmers)
    total_land = df["land_acres"].sum()
    crop_counts = df["crop"].value_counts().to_dict()
    total_investment = df["investment"].sum() if "investment" in df else 0
    return total_land, crop_counts, df, total_investment