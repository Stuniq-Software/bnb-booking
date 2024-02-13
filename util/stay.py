import requests
import os
from typing import Optional


def calculate_total_price(stay_id: str, nights: int) -> float:
    print(f"Nights: {nights}")
    stay = get_stay(stay_id)
    if stay is not None:
        return stay['price_per_night'] * nights
    return 0


def get_stay(stay_id: str) -> Optional[dict]:
    response = requests.get(f"{os.getenv('STAY_SVC_URL')}/api/v1/stays/{stay_id}")
    if response.status_code == 200:
        return response.json().get('data')
    return None
