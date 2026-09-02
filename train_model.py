import pandas as pd

# Load our dataset
df = pd.read_csv("negotiation_dataset.csv")

# Display basic information
print("Dataset loaded successfully!")

print("\nNumber of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head())

# Input features
X = df.drop(
    ["minimum_acceptable_price", "product_id"],
    axis=1
)
# Target value
y = df["minimum_acceptable_price"]

print("\nInput features:")
print(X.columns.tolist())

print("\nTarget:")
print(y.name)

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Categorical columns
categorical_features = [
    "brand",
    "product_name",
    "category",
    "customer_type"
]

# Numerical columns
numerical_features = [
    "original_price",
    "stock",
    "negotiation_round",
    "festival_sale"
]

# Preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)

# Convert the data
X_encoded = preprocessor.fit_transform(X)

print("\nData preprocessing completed!")
print("Encoded data shape:", X_encoded.shape)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_encoded,
    y,
    test_size=0.2,
    random_state=42
)

print("\nData split completed!")

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)

from sklearn.ensemble import RandomForestRegressor

# Create the ML model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

# Train the model
model.fit(X_train, y_train)

print("\nModel training completed!")
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Make predictions on test data
y_pred = model.predict(X_test)

# Calculate evaluation metrics
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\nModel Evaluation")
print("-------------------------")
print("Mean Absolute Error:", round(mae, 2))
print("Root Mean Squared Error:", round(rmse, 2))
print("R² Score:", round(r2, 4))

import joblib

# Save the trained model
joblib.dump(model, "negotiator_model.pkl")

# Save the preprocessor too
joblib.dump(preprocessor, "negotiator_preprocessor.pkl")

print("\nModel saved successfully!")
print("Created: negotiator_model.pkl")
print("Created: negotiator_preprocessor.pkl")