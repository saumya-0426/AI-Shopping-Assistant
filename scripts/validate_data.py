import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

customers_path = DATA_DIR / "customers.csv"
transactions_path = DATA_DIR / "transactions.csv"
products_path = DATA_DIR / "products.csv"


def check_file(path):
    if not path.exists():
        print(f"❌ Missing file: {path}")
        return False
    print(f"✓ Found: {path.name}")
    return True


def main():
    print("=" * 60)
    print("DATASET VALIDATION")
    print("=" * 60)

    files = [customers_path, transactions_path, products_path]

    if not all(check_file(file) for file in files):
        print("\n❌ Validation stopped because a file is missing.")
        return

    customers = pd.read_csv(customers_path)
    transactions = pd.read_csv(transactions_path)
    products = pd.read_csv(products_path)

    print("\n" + "=" * 60)
    print("DATASET SHAPES")
    print("=" * 60)

    print(f"Customers    : {customers.shape[0]} rows, {customers.shape[1]} columns")
    print(f"Transactions : {transactions.shape[0]} rows, {transactions.shape[1]} columns")
    print(f"Products     : {products.shape[0]} rows, {products.shape[1]} columns")

    print("\n" + "=" * 60)
    print("COLUMN VALIDATION")
    print("=" * 60)

    required_columns = {
        "customers": ["customer_id"],
        "transactions": ["customer_id", "product_id"],
        "products": [
            "product_id",
            "category",
            "product_name",
            "brand",
            "price",
            "description",
            "features",
            "stock",
            "delivery_days"
        ]
    }

    datasets = {
        "customers": customers,
        "transactions": transactions,
        "products": products
    }

    validation_passed = True

    for name, required in required_columns.items():
        missing = [column for column in required if column not in datasets[name].columns]

        if missing:
            print(f"❌ {name}: Missing columns: {missing}")
            validation_passed = False
        else:
            print(f"✓ {name}: All required columns present")

    print("\n" + "=" * 60)
    print("MISSING VALUE CHECK")
    print("=" * 60)

    for name, df in datasets.items():
        missing = df.isnull().sum()
        missing = missing[missing > 0]

        if len(missing) == 0:
            print(f"✓ {name}: No missing values")
        else:
            print(f"❌ {name}: Missing values found")
            print(missing)

    print("\n" + "=" * 60)
    print("DUPLICATE ID CHECK")
    print("=" * 60)

    if "customer_id" in customers.columns:
        duplicate_customers = customers["customer_id"].duplicated().sum()

        if duplicate_customers == 0:
            print("✓ customers.csv: No duplicate customer IDs")
        else:
            print(f"❌ customers.csv: {duplicate_customers} duplicate customer IDs")

    if "product_id" in products.columns:
        duplicate_products = products["product_id"].duplicated().sum()

        if duplicate_products == 0:
            print("✓ products.csv: No duplicate product IDs")
        else:
            print(f"❌ products.csv: {duplicate_products} duplicate product IDs")

    print("\n" + "=" * 60)
    print("DATA TYPE CHECK")
    print("=" * 60)

    print("\nProducts:")
    print(products.dtypes)

    print("\nTransactions:")
    print(transactions.dtypes)

    print("\n" + "=" * 60)
    print("RELATIONSHIP CHECK")
    print("=" * 60)

    if "customer_id" in customers.columns and "customer_id" in transactions.columns:
        customer_ids = set(customers["customer_id"])
        transaction_customer_ids = set(transactions["customer_id"])

        invalid_customers = transaction_customer_ids - customer_ids

        if len(invalid_customers) == 0:
            print("✓ All transaction customer IDs exist in customers.csv")
        else:
            print(
                f"❌ {len(invalid_customers)} transaction customer IDs "
                "do not exist in customers.csv"
            )

    if "product_id" in products.columns and "product_id" in transactions.columns:
        product_ids = set(products["product_id"])
        transaction_product_ids = set(transactions["product_id"])

        invalid_products = transaction_product_ids - product_ids

        if len(invalid_products) == 0:
            print("✓ All transaction product IDs exist in products.csv")
        else:
            print(
                f"❌ {len(invalid_products)} transaction product IDs "
                "do not exist in products.csv"
            )

    print("\n" + "=" * 60)
    print("PRODUCT CONSTRAINT CHECK")
    print("=" * 60)

    if "price" in products.columns:
        if (products["price"] < 0).any():
            print("❌ Products contain negative prices")
        else:
            print("✓ Product prices are valid")

    if "stock" in products.columns:
        if (products["stock"] < 0).any():
            print("❌ Products contain negative stock values")
        else:
            print("✓ Stock values are valid")

    if "delivery_days" in products.columns:
        if (products["delivery_days"] < 0).any():
            print("❌ Products contain negative delivery days")
        else:
            print("✓ Delivery days are valid")

    print("\n" + "=" * 60)

    if validation_passed:
        print("✅ BASIC DATA VALIDATION COMPLETED")
    else:
        print("⚠️ VALIDATION COMPLETED WITH ERRORS")

    print("=" * 60)


if __name__ == "__main__":
    main()