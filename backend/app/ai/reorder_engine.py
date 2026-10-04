import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[3]

TRANSACTIONS_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "transactions.csv"
)

PRODUCTS_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "products_processed.csv"
)


transactions = pd.read_csv(
    TRANSACTIONS_FILE
)

products = pd.read_csv(
    PRODUCTS_FILE
)

transactions["purchase_date"] = pd.to_datetime(
    transactions["purchase_date"]
)


def get_customer_history(customer_id):

    history = transactions[
        transactions["customer_id"] == customer_id
    ].copy()

    if history.empty:
        return history

    return history.sort_values(
        "purchase_date",
        ascending=False
    )


def get_reorder_candidates(customer_id):

    history = get_customer_history(
        customer_id
    )

    if history.empty:
        return pd.DataFrame()

    summary = (
        history
        .groupby("product_id")
        .agg(
            purchase_count=(
                "transaction_id",
                "count"
            ),
            total_quantity=(
                "quantity",
                "sum"
            ),
            last_purchase=(
                "purchase_date",
                "max"
            )
        )
        .reset_index()
    )

    latest_date = transactions[
        "purchase_date"
    ].max()

    summary["days_since_purchase"] = (
        latest_date
        - summary["last_purchase"]
    ).dt.days

    summary["recency_score"] = (
        1 /
        (1 + summary["days_since_purchase"])
    )

    summary["frequency_score"] = (
        summary["purchase_count"]
        / summary["purchase_count"].max()
    )

    summary["reorder_score"] = (
        0.6 * summary["frequency_score"]
        +
        0.4 * summary["recency_score"]
    )

    return summary.sort_values(
        "reorder_score",
        ascending=False
    )


def get_available_reorders(
    customer_id,
    top_k=5
):

    candidates = get_reorder_candidates(
        customer_id
    )

    if candidates.empty:
        return pd.DataFrame()

    results = candidates.merge(
        products,
        on="product_id",
        how="inner"
    )

    results = results[
        results["stock"] > 0
    ].copy()

    results = results.sort_values(
        "reorder_score",
        ascending=False
    )

    return results.head(top_k)


if __name__ == "__main__":

    customer_id = 1

    results = get_available_reorders(
        customer_id,
        top_k=5
    )

    print("\n" + "=" * 60)
    print("AVAILABLE REORDER RECOMMENDATIONS")
    print("=" * 60)

    if results.empty:

        print(
            "No available reorder products found."
        )

    else:

        for _, product in results.iterrows():

            print(
                f"\nProduct: "
                f"{product['product_name']}"
            )

            print(
                f"Brand: "
                f"{product['brand']}"
            )

            print(
                f"Price: ₹"
                f"{product['price']}"
            )

            print(
                f"Stock: "
                f"{product['stock']}"
            )

            print(
                f"Last Purchase: "
                f"{product['last_purchase']}"
            )

            print(
                f"Purchase Count: "
                f"{product['purchase_count']}"
            )

            print(
                f"Reorder Score: "
                f"{product['reorder_score']:.4f}"
            )