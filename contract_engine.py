# contract_engine.py - Mill negotiation and contract logic
import time
import random
from config import MARKET_RATE_RANGE

def add_agent_log(logs, msg):
    from datetime import datetime
    logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def negotiate_contract(mill_name, offered_price_per_kg, crop_type, quantity_kg, logs):
    add_agent_log(logs, f"Starting negotiation with {mill_name} for {quantity_kg}kg {crop_type}")
    time.sleep(0.8)
    market_rate = random.randint(MARKET_RATE_RANGE[0], MARKET_RATE_RANGE[1])
    if offered_price_per_kg >= market_rate:
        add_agent_log(logs, f"Offered PKR {offered_price_per_kg} >= market PKR {market_rate} → Accepted")
        return True, offered_price_per_kg, market_rate
    else:
        counter = market_rate - 5
        add_agent_log(logs, f"Offered low. Counter offer PKR {counter}")
        if counter <= offered_price_per_kg + 10:
            add_agent_log(logs, f"Mill accepted counter offer at PKR {counter}")
            return True, counter, market_rate
        else:
            add_agent_log(logs, f"Negotiation failed. Mill rejected.")
            return False, None, market_rate