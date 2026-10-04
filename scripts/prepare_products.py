import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw" / "products.csv"
PROCESSED_DATA = BASE_DIR / "data" / "processed" / "products_processed.csv"


# Part 1: Load and inspect data
products = pd.read_csv(RAW_DATA)

print("=" * 60)
print("PRODUCT DATA PREPARATION")
print("=" * 60)

print(f"\nNumber of products: {len(products)}")

print("\nColumns:")
print(products.columns.tolist())


semantic_columns = [
    "product_name",
    "category",
    "brand",
    "description",
    "features"
]

print("\nSemantic Search Fields:")

for column in semantic_columns:
    print(f"✓ {column}")


# Part 2: Clean text
def clean_text(value):
    if pd.isna(value):
        return ""

    value = str(value)
    value = " ".join(value.split())

    return value.strip()


for column in semantic_columns:
    products[column] = products[column].apply(clean_text)


print("\n✓ Text cleaning completed")


# Part 3: Create combined product text
def create_product_text(row):
    return (
        f"Product: {row['product_name']}. "
        f"Category: {row['category']}. "
        f"Brand: {row['brand']}. "
        f"Description: {row['description']}. "
        f"Features: {row['features']}."
    )


products["product_text"] = products.apply(
    create_product_text,
    axis=1
)


print("✓ Product text created")


print("\nSample Product Text:")
print("-" * 60)
print(products["product_text"].iloc[0])
print("-" * 60)


# Part 4: Save processed data
PROCESSED_DATA.parent.mkdir(
    parents=True,
    exist_ok=True
)

products.to_csv(
    PROCESSED_DATA,
    index=False
)

print(f"\n✓ Processed dataset saved to:")
print(PROCESSED_DATA)

print("\nFinal shape:", products.shape)
print("\n" + "=" * 60)
print("STAGE 2 COMPLETED")
print("=" * 60)