from query_parser import parse_query
from semantic_search import semantic_search
from constraint_filter import apply_constraints


def rank_results(results, top_k=5):

    if results.empty:
        return results

    results = results.sort_values(
        by="similarity_score",
        ascending=False
    )

    return results.head(top_k)


def search_products(
    user_query,
    top_k=20,
    final_k=5
):

    # Step 1: Understand user query
    parsed_query = parse_query(user_query)

    # Step 2: Semantic search
    semantic_query = parsed_query["query"]

    results = semantic_search(
        semantic_query,
        top_k=top_k
    )

    # Step 3: Apply constraints
    filtered_results = apply_constraints(
        results,
        max_budget=parsed_query["max_budget"],
        max_delivery_days=parsed_query["max_delivery_days"],
        excluded_brands=parsed_query["excluded_brands"]
    )

    # Step 4: Rank final results
    ranked_results = rank_results(
        filtered_results,
        top_k=final_k
    )

    return parsed_query, ranked_results


if __name__ == "__main__":

    user_query = (
        "I want comfortable shoes for travelling "
        "under 500, deliver within 3 days, "
        "and don't show Brand 11"
    )

    parsed_query, results = search_products(
        user_query,
        top_k=20,
        final_k=5
    )

    print("\n" + "=" * 60)
    print("SHOPPING ASSISTANT")
    print("=" * 60)

    print("\nUser Query:")
    print(user_query)

    print("\nParsed Query:")
    print(parsed_query)

    print("\nRecommended Products:")
    print("=" * 60)

    if results.empty:

        print(
            "No products satisfy the "
            "requested constraints."
        )

    else:

        for _, product in results.iterrows():

            print(
                f"\nProduct: "
                f"{product['product_name']}"
            )

            print(
                f"Category: "
                f"{product['category']}"
            )

            print(
                f"Brand: "
                f"{product['brand']}"
            )

            print(
                f"Price: ₹{product['price']}"
            )

            print(
                f"Stock: "
                f"{product['stock']}"
            )

            print(
                f"Delivery: "
                f"{product['delivery_days']} days"
            )

            print(
                f"Similarity: "
                f"{product['similarity_score']:.4f}"
            )

            print(
                f"Description: "
                f"{product['description']}"
            )