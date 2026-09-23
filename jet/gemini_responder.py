from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_negotiation_reply(decision, product_name, customer_offer, final_price=None):
    """
    Generates a natural-sounding negotiation reply using Gemini.
    Returns None if the call fails, so the caller can fall back to a static message.
    """
    prompt_map = {
        "ACCEPT": (
            f"A customer's offer of ₹{customer_offer} for '{product_name}' has been accepted. "
            f"Write one short, warm, polite sentence confirming the deal is closed at that price. "
            f"Do not mention AI or negotiation strategy."
        ),
        "COUNTER": (
            f"A customer offered ₹{customer_offer} for '{product_name}', which we can't accept, "
            f"but we can offer it at ₹{final_price}. Write one short, polite sentence making this counter-offer "
            f"in a friendly, sales-appropriate tone. Do not reveal any internal pricing logic."
        ),
        "COUNTER_VAGUE": (
            f"A customer's offer for '{product_name}' is somewhat low but in a reasonable range. "
            f"Write one short, encouraging sentence nudging them to raise their offer slightly, "
            f"WITHOUT stating any specific number."
        ),
        "TOO_LOW": (
            f"A customer's offer for '{product_name}' is far too low to be workable. "
            f"Write one short, polite sentence declining the offer and asking them to try a "
            f"significantly higher amount, WITHOUT stating any specific number."
        ),
    }

    prompt = prompt_map.get(decision)
    if not prompt:
        return None

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print("GEMINI ERROR:", e)
    return None