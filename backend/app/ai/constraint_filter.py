import pandas as pd


def filter_by_budget(products, max_budget=None):

    if max_budget is None:
        return products.copy()

    return products[
        products["price"] <= max_budget
    ].copy()


def filter_by_stock(products):

    return products[
        products["stock"] > 0
    ].copy()


def filter_by_delivery(products, max_delivery_days=None):

    if max_delivery_days is None:
        return products.copy()

    return products[
        products["delivery_days"] <= max_delivery_days
    ].copy()


def filter_by_exclusions(products, excluded_brands=None):

    if not excluded_brands:
        return products.copy()

    excluded_brands = [
        brand.lower()
        for brand in excluded_brands
    ]

    return products[
        ~products["brand"]
        .str.lower()
        .isin(excluded_brands)
    ].copy()


def apply_constraints(
    products,
    max_budget=None,
    max_delivery_days=None,
    excluded_brands=None
):

    filtered = products.copy()

    # Stock constraint
    filtered = filter_by_stock(filtered)

    # Budget constraint
    filtered = filter_by_budget(
        filtered,
        max_budget
    )

    # Delivery constraint
    filtered = filter_by_delivery(
        filtered,
        max_delivery_days
    )

    # Brand exclusion
    filtered = filter_by_exclusions(
        filtered,
        excluded_brands
    )

    return filtered


if __name__ == "__main__":

    products = pd.DataFrame({
        "product_name": [
            "Product 1",
            "Product 2",
            "Product 3",
            "Product 4"
        ],
        "brand": [
            "Brand 1",
            "Brand 11",
            "Brand 2",
            "Brand 3"
        ],
        "price": [
            250,
            400,
            600,
            300
        ],
        "stock": [
            10,
            0,
            5,
            20
        ],
        "delivery_days": [
            2,
            1,
            4,
            3
        ]
    })

    filtered = apply_constraints(
        products,
        max_budget=500,
        max_delivery_days=3,
        excluded_brands=["Brand 11"]
    )

    print("=" * 60)
    print("CONSTRAINT FILTERING RESULTS")
    print("=" * 60)

    print(filtered)