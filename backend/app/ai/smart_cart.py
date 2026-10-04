import pandas as pd


def build_smart_cart(
    results,
    default_quantity=1
):

    if results.empty:

        return {
            "items": [],
            "item_count": 0,
            "total_amount": 0.0
        }

    cart_items = []

    total_amount = 0.0

    for _, product in results.iterrows():

        quantity = default_quantity

        price = float(
            product["price"]
        )

        subtotal = price * quantity

        total_amount += subtotal

        cart_items.append(
            {
                "product_id": int(
                    product["product_id"]
                ),
                "product_name": str(
                    product["product_name"]
                ),
                "brand": str(
                    product["brand"]
                ),
                "price": price,
                "quantity": quantity,
                "subtotal": round(
                    subtotal,
                    2
                ),
                "stock": int(
                    product["stock"]
                ),
                "delivery_days": int(
                    product["delivery_days"]
                ),
                "source": str(
                    product["source"]
                ),
                "score": round(
                    float(
                        product["final_score"]
                    ),
                    4
                )
            }
        )

    return {
        "items": cart_items,
        "item_count": len(cart_items),
        "total_amount": round(
            total_amount,
            2
        )
    }


if __name__ == "__main__":

    data = pd.DataFrame(
        [
            {
                "product_id": 101,
                "product_name": "Product 101",
                "brand": "Brand 1",
                "price": 250,
                "stock": 20,
                "delivery_days": 2,
                "source": "discovery",
                "final_score": 0.82
            },
            {
                "product_id": 102,
                "product_name": "Product 102",
                "brand": "Brand 2",
                "price": 300,
                "stock": 10,
                "delivery_days": 3,
                "source": "reorder",
                "final_score": 0.76
            }
        ]
    )

    cart = build_smart_cart(data)

    print(cart)