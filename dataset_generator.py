import pandas as pd
import random

# Make the results reproducible
random.seed(42)

# -----------------------------
# Product List
# -----------------------------
products = [
    {"id": "P001", "brand": "Apple", "name": "iPhone 16", "category": "Smartphone", "price": 80000},
    {"id": "P002", "brand": "Samsung", "name": "Samsung Galaxy S25 Ultra", "category": "Smartphone", "price": 95000},
    {"id": "P003", "brand": "Apple", "name": "MacBook Air M4", "category": "Laptop", "price": 110000},
    {"id": "P004", "brand": "Sony", "name": "PlayStation 5", "category": "Gaming Console", "price": 55000},
    {"id": "P005", "brand": "Sony", "name": "Sony WH-1000XM6", "category": "Headphones", "price": 32000},
    {"id": "P006", "brand": "Apple", "name": "Apple Watch Series 10", "category": "Smartwatch", "price": 50000},
    {"id": "P007", "brand": "Dell", "name": "Dell XPS 13", "category": "Laptop", "price": 120000},
    {"id": "P008", "brand": "Canon", "name": "Canon EOS R50", "category": "Camera", "price": 75000},
    {"id": "P009", "brand": "Apple", "name": "iPad Air M3", "category": "Tablet", "price": 65000},
    {"id": "P010", "brand": "ASUS", "name": "ASUS ROG Zephyrus G16", "category": "Laptop", "price": 160000},
]

# -----------------------------
# Base Discount for Each Product
# -----------------------------
product_discount = {
    "iPhone 16": 5,
    "Samsung Galaxy S25 Ultra": 10,
    "MacBook Air M4": 6,
    "PlayStation 5": 7,
    "Sony WH-1000XM6": 15,
    "Apple Watch Series 10": 8,
    "Dell XPS 13": 8,
    "Canon EOS R50": 10,
    "iPad Air M3": 7,
    "ASUS ROG Zephyrus G16": 12
}

# -----------------------------
# Calculate Minimum Acceptable Price
# -----------------------------
def calculate_min_price(
    product_name,
    price,
    stock,
    customer_type,
    negotiation_round,
    festival_sale
):

    # Product-specific starting discount
    discount = product_discount[product_name]

    # Starting minimum price
    min_price = price * (1 - discount / 100)

    # -----------------------------
    # Stock Adjustment
    # -----------------------------
    if stock < 20:
        # Low stock = seller is less flexible
        min_price += price * 0.03

    elif stock > 80:
        # High stock = seller is more flexible
        min_price -= price * 0.02

    # -----------------------------
    # Customer Type Adjustment
    # -----------------------------
    if customer_type == "Returning":
        min_price -= price * 0.01

    elif customer_type == "Premium":
        min_price -= price * 0.02

    # -----------------------------
    # Festival Sale Adjustment
    # -----------------------------
    if festival_sale == 1:
        min_price -= price * 0.02

    # -----------------------------
    # Negotiation Round Adjustment
    # -----------------------------
    if negotiation_round == 2:
        min_price -= price * 0.01

    elif negotiation_round == 3:
        min_price -= price * 0.02

    # -----------------------------
    # Small Random Variation
    # -----------------------------
    noise = random.randint(-500, 500)
    min_price += noise

    # Make sure minimum price never becomes
    # greater than the original price
    min_price = min(min_price, price)

    # Make sure minimum price doesn't become
    # unrealistically low
    min_price = max(min_price, price * 0.70)

    return round(min_price)


# -----------------------------
# Generate 10,000 Records
# -----------------------------
records = []

for i in range(10000):

    product = random.choice(products)

    record = {
        "product_id": product["id"],
        "brand": product["brand"],
        "product_name": product["name"],
        "category": product["category"],
        "original_price": product["price"],
        "stock": random.randint(1, 100),
        "customer_type": random.choice(
            ["New", "Returning", "Premium"]
        ),
        "negotiation_round": random.randint(1, 3),
        "festival_sale": random.choice([0, 1])
    }

    # Calculate target value
    record["minimum_acceptable_price"] = calculate_min_price(
        record["product_name"],
        record["original_price"],
        record["stock"],
        record["customer_type"],
        record["negotiation_round"],
        record["festival_sale"]
    )

    records.append(record)


# -----------------------------
# Convert to DataFrame
# -----------------------------
df = pd.DataFrame(records)


# -----------------------------
# Display Dataset Information
# -----------------------------
print("\nFirst 10 Records:")
print(df.head(10))

print("\nDataset Shape:")
print(df.shape)

print("\nDataset Columns:")
print(df.columns.tolist())


# -----------------------------
# Save Dataset
# -----------------------------
df.to_csv("negotiation_dataset.csv", index=False)

print("\nDataset Saved Successfully!")
print("File: negotiation_dataset.csv")