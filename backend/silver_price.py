# silver_price.py

import requests
import os
import logging

# Load API key from env
METALPRICE_API_KEY = os.getenv("METALPRICE_API_KEY")

def get_silver_price():
    if not METALPRICE_API_KEY:
        logging.error("❌ METALPRICE_API_KEY not set in env.")
        return None

    url = f"https://api.metalpriceapi.com/v1/latest?base=XAG&currencies=INR&apikey={METALPRICE_API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if "rates" in data and "INR" in data["rates"]:
            silver_price_inr = data["rates"]["INR"]
            logging.info(f"✅ Silver price fetched: ₹{silver_price_inr:.2f}/oz")
            return silver_price_inr
        else:
            logging.warning(f"⚠️ Unexpected response from MetalPriceAPI: {data}")
            return None

    except Exception as e:
        logging.error(f"❌ Failed to fetch silver price: {e}")
        return None
