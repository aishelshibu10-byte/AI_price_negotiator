import pandas as pd
import joblib

# -----------------------------
# Load ML Model
# -----------------------------

model = joblib.load("negotiator_model.pkl")
preprocessor = joblib.load("negotiator_preprocessor.pkl")

print("ML model loaded successfully!")


# -----------------------------
# Product / Negotiation Details
# -----------------------------
# -----------------------------
# Available Products
# -----------------------------

products = [
    {
        "brand": "Apple",
        "name": "iPhone 16",
        "category": "Smartphone",
        "price": 80000,
        "stock": 20
    },
    {
        "brand": "Samsung",
        "name": "Samsung Galaxy S25 Ultra",
        "category": "Smartphone",
        "price": 95000,
        "stock": 15
    },
    {
        "brand": "Apple",
        "name": "MacBook Air M4",
        "category": "Laptop",
        "price": 110000,
        "stock": 10
    },
    {
        "brand": "Sony",
        "name": "PlayStation 5",
        "category": "Gaming Console",
        "price": 55000,
        "stock": 25
    },
    {
        "brand": "Sony",
        "name": "Sony WH-1000XM6",
        "category": "Headphones",
        "price": 32000,
        "stock": 40
    },
    {
        "brand": "Apple",
        "name": "Apple Watch Series 10",
        "category": "Smartwatch",
        "price": 50000,
        "stock": 30
    },
    {
        "brand": "Dell",
        "name": "Dell XPS 13",
        "category": "Laptop",
        "price": 120000,
        "stock": 12
    },
    {
        "brand": "Canon",
        "name": "Canon EOS R50",
        "category": "Camera",
        "price": 75000,
        "stock": 18
    },
    {
        "brand": "Apple",
        "name": "iPad Air M3",
        "category": "Tablet",
        "price": 65000,
        "stock": 35
    },
    {
        "brand": "ASUS",
        "name": "ASUS ROG Zephyrus G16",
        "category": "Laptop",
        "price": 160000,
        "stock": 8
    }
]

# -----------------------------
# Product Selection
# -----------------------------

print("\n==============================")
print("      AI PRICE NEGOTIATOR")
print("==============================")

for i, product in enumerate(products, start=1):
    print(
        f"{i}. {product['name']} - ₹{product['price']:,}"
    )

while True:

    try:
        choice = int(input("\nSelect a product (1-10): "))

        if 1 <= choice <= len(products):
            selected_product = products[choice - 1]
            break

        print("Please select a number between 1 and 10.")

    except ValueError:
        print("Please enter a valid number.")


# Selected product information
product_brand = selected_product["brand"]
product_name = selected_product["name"]
product_category = selected_product["category"]
original_price = selected_product["price"]
stock = selected_product["stock"]

print("\nProduct selected:", product_name)
print("Original Price: ₹", f"{original_price:,}")
print("Available Stock:", stock)


# -----------------------------
# Customer Type
# -----------------------------

print("\nCustomer Type")
print("1. New")
print("2. Returning")
print("3. Premium")

while True:

    try:
        customer_choice = int(
            input("Select customer type (1-3): ")
        )

        if customer_choice == 1:
            customer_type = "New"
            break

        elif customer_choice == 2:
            customer_type = "Returning"
            break

        elif customer_choice == 3:
            customer_type = "Premium"
            break

        else:
            print("Please select 1, 2, or 3.")

    except ValueError:
        print("Please enter 1, 2, or 3.")

print("Customer Type:", customer_type)



# -----------------------------
# Festival Sale
# -----------------------------

festival_choice = input(
    "\nIs there a festival sale? (y/n): "
).lower()

festival_sale = 1 if festival_choice == "y" else 0




# -----------------------------
# Multi-Round Negotiation
# -----------------------------

negotiation_round = 1

while negotiation_round <= 3:

    print("\n==============================")
    print("Negotiation Round:", negotiation_round)
    print("==============================")

    # -----------------------------
    # Create Current Scenario
    # -----------------------------

    scenario = pd.DataFrame([{
        "brand": product_brand,
        "product_name": product_name,
        "category": product_category,
        "original_price": original_price,
        "stock": stock,
        "customer_type": customer_type,
        "negotiation_round": negotiation_round,
        "festival_sale": festival_sale
    }])

    # -----------------------------
    # Preprocess Scenario
    # -----------------------------

    scenario_encoded = preprocessor.transform(scenario)

    # -----------------------------
    # Predict Minimum Price
    # -----------------------------

    predicted_min_price = model.predict(
        scenario_encoded
    )[0]

    print(
        "Predicted Minimum Price: ₹",
        round(predicted_min_price)
    )

    # -----------------------------
    # Get Customer Offer
    # -----------------------------

    customer_offer = float(
        input("Enter your offer price: ₹")
    )

    # -----------------------------
    # Calculate Difference
    # -----------------------------

    difference = predicted_min_price - customer_offer

    # 5% negotiation range
    counter_threshold = predicted_min_price * 0.05

    # -----------------------------
    # Decision
    # -----------------------------

    if customer_offer >= predicted_min_price:

        decision = "Accept"
        counter_offer = None

    elif difference <= counter_threshold:

        decision = "Counter"

        # Counter slightly above minimum
        counter_offer = round(
            predicted_min_price + 500
        )

    else:

        decision = "Too Low"

        counter_offer = round(
            predicted_min_price
        )

    # -----------------------------
    # Display Result
    # -----------------------------

    print("\n--- Negotiation Result ---")

    print(
        "Your Offer: ₹",
        round(customer_offer)
    )

    print(
        "Minimum Acceptable Price: ₹",
        round(predicted_min_price)
    )

    # -----------------------------
    # ACCEPT
    # -----------------------------

    if decision == "Accept":

        print(
            "\n🤝 Great! Your offer has been accepted."
        )

        print(
            "We can close the deal at ₹",
            round(customer_offer)
        )

        break

    # -----------------------------
    # COUNTER
    # -----------------------------

    elif decision == "Counter":

        print(
            "\n🤝 Thank you for your offer."
        )

        print(
            "We can't close the deal at ₹",
            round(customer_offer),
            "but we can offer it for ₹",
            counter_offer
        )

        print(
            "If you're comfortable with this price, "
            "we can close the deal."
        )

        negotiation_round += 1

    # -----------------------------
    # TOO LOW
    # -----------------------------

    else:

        print(
            "\n🙂 Thank you for your offer."
        )

        print(
            "Unfortunately, we wouldn't be able "
            "to provide this item at ₹",
            round(customer_offer)
        )

        print(
            "If you're comfortable with ₹",
            round(predicted_min_price),
            "or above, we'd be happy to close the deal."
        )

        print(
            "You can make another offer."
        )

        negotiation_round += 1


# -----------------------------
# Maximum Rounds Reached
# -----------------------------

if negotiation_round > 3:

    print("\n==============================")
    print("Negotiation Ended")
    print("==============================")

    print(
        "We've reached the maximum number "
        "of negotiation rounds."
    )

    print(
        "Thank you for considering the product!"
    )