from .ml.negotiator import predict_min_price, round_up_commercial

MAX_ROUNDS = 3
COUNTER_TOLERANCE = 0.05      # within 5% of floor -> give a real counter
FAR_OFF_TOLERANCE = 0.20      # within 20% of floor -> vague nudge, no number
COUNTER_MARKUP = 0.02         # counter is 2% above the true floor, never equal to it


def evaluate_offer(product, customer_segment, negotiation_round, customer_offer):
    predicted_min_price = predict_min_price(product, customer_segment, negotiation_round)
    difference = predicted_min_price - customer_offer

    close_threshold = predicted_min_price * COUNTER_TOLERANCE
    far_threshold = predicted_min_price * FAR_OFF_TOLERANCE

    if customer_offer >= predicted_min_price:
        decision = "ACCEPT"
        final_price = customer_offer

    elif difference <= close_threshold:
        # Close enough — give a real counter, but ABOVE the true floor
        decision = "COUNTER"
        counter_raw = predicted_min_price * (1 + COUNTER_MARKUP)
        final_price = round_up_commercial(counter_raw)

    elif difference <= far_threshold:
        # In range but not close — nudge them up without revealing a number
        decision = "COUNTER_VAGUE"
        final_price = None

    else:
        # Way too low — reject without any number
        decision = "TOO_LOW"
        final_price = None

    return {
        "decision": decision,
        "predicted_min_price": round(predicted_min_price, 2),  # keep this server-side only, don't render it!
        "customer_offer": customer_offer,
        "final_price": final_price,
        "negotiation_round": negotiation_round,
        "rounds_left": MAX_ROUNDS - negotiation_round,
    }