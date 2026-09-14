import os
import math
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(__file__)

model = joblib.load(os.path.join(BASE_DIR, "negotiator_model.pkl"))
preprocessor = joblib.load(os.path.join(BASE_DIR, "negotiator_preprocessor.pkl"))

# Maps our CustomerProfile.segment (NEW/RETURNING/PREMIUM)
# to the exact strings the ML model was trained on (New/Returning/Premium)
SEGMENT_MAP = {
    "NEW": "New",
    "RETURNING": "Returning",
    "PREMIUM": "Premium",
}


def predict_min_price(product, customer_segment, negotiation_round):
    """
    product: a jet.models.Product instance
    customer_segment: one of 'NEW', 'RETURNING', 'PREMIUM'
    negotiation_round: int, 1-based
    """
    scenario = pd.DataFrame([{
        "brand": product.brand,
        "product_name": product.name,
        "category": product.category,
        "original_price": float(product.original_price),
        "stock": product.stock,
        "customer_type": SEGMENT_MAP.get(customer_segment, "New"),
        "negotiation_round": negotiation_round,
        "festival_sale": int(product.festival_sale),
    }])

    encoded = preprocessor.transform(scenario)
    predicted_price = model.predict(encoded)[0]
    return float(predicted_price)


def round_up_commercial(price):
    """
    Rounds a price UP to the nearest '...999' ending, never below the
    original price. E.g. 72384 -> 72999, 55000 -> 55999.
    """
    thousands = math.ceil(price / 1000) * 1000
    rounded = thousands - 1
    if rounded < price:
        rounded += 1000
    return rounded