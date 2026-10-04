import pandas as pd

from backend.app.ai.query_parser import parse_query
from backend.app.ai.semantic_search import semantic_search
from backend.app.ai.constraint_filter import apply_constraints
from backend.app.ai.reorder_engine import get_available_reorders


def add_source(results, source):

    if results.empty:
        return results

    results = results.copy()

    results["source"] = source

    return results


def get_discovery_results(
    parsed_query,
    top_k=20
):

    query = parsed_query["query"]

    if not query:
        return pd.DataFrame()

    results = semantic_search(
        query,
        top_k=top_k
    )

    results = apply_constraints(
        results,
        max_budget=parsed_query["max_budget"],
        max_delivery_days=parsed_query["max_delivery_days"],
        excluded_brands=parsed_query["excluded_brands"]
    )

    return results


def get_reorder_results(
    customer_id,
    parsed_query,
    top_k=5
):

    results = get_available_reorders(
        customer_id,
        top_k=top_k
    )

    if results.empty:
        return results

    results = apply_constraints(
        results,
        max_budget=parsed_query["max_budget"],
        max_delivery_days=parsed_query["max_delivery_days"],
        excluded_brands=parsed_query["excluded_brands"]
    )

    return results


def combine_results(
    reorder_results,
    discovery_results,
    final_k=10
):

    # --------------------------------------------------
    # Mixed ranking strategy
    # Reserve slots for both recommendation sources
    # --------------------------------------------------

    if reorder_results.empty and discovery_results.empty:
        return pd.DataFrame()

    if reorder_results.empty:
        discovery_results = discovery_results.copy()

        if "similarity_score" not in discovery_results.columns:
            discovery_results["similarity_score"] = 0.0

        discovery_results["reorder_score"] = 0.0

        discovery_results["similarity_score"] = (
            pd.to_numeric(
                discovery_results["similarity_score"],
                errors="coerce"
            ).fillna(0.0)
        )

        discovery_results["final_score"] = (
            discovery_results["similarity_score"]
        )

        return (
            discovery_results
            .sort_values(
                "final_score",
                ascending=False
            )
            .head(final_k)
        )

    if discovery_results.empty:
        reorder_results = reorder_results.copy()

        if "reorder_score" not in reorder_results.columns:
            reorder_results["reorder_score"] = 0.0

        reorder_results["similarity_score"] = 0.0

        reorder_results["reorder_score"] = (
            pd.to_numeric(
                reorder_results["reorder_score"],
                errors="coerce"
            ).fillna(0.0)
        )

        reorder_results["final_score"] = (
            reorder_results["reorder_score"]
        )

        return (
            reorder_results
            .sort_values(
                "final_score",
                ascending=False
            )
            .head(final_k)
        )

    # --------------------------------------------------
    # Clean scores
    # --------------------------------------------------

    reorder_results = reorder_results.copy()
    discovery_results = discovery_results.copy()

    if "similarity_score" not in reorder_results.columns:
        reorder_results["similarity_score"] = 0.0

    if "reorder_score" not in discovery_results.columns:
        discovery_results["reorder_score"] = 0.0

    reorder_results["similarity_score"] = 0.0

    reorder_results["reorder_score"] = (
        pd.to_numeric(
            reorder_results["reorder_score"],
            errors="coerce"
        ).fillna(0.0)
    )

    discovery_results["reorder_score"] = 0.0

    discovery_results["similarity_score"] = (
        pd.to_numeric(
            discovery_results["similarity_score"],
            errors="coerce"
        ).fillna(0.0)
    )

    # --------------------------------------------------
    # Calculate individual scores
    # --------------------------------------------------

    reorder_results["final_score"] = (
        0.4 * reorder_results["reorder_score"]
    )

    discovery_results["final_score"] = (
        0.6 * discovery_results["similarity_score"]
    )

    # --------------------------------------------------
    # Reserve slots for both sources
    # --------------------------------------------------

    reorder_slots = min(
        len(reorder_results),
        max(1, final_k // 3)
    )

    discovery_slots = final_k - reorder_slots

    top_reorders = (
        reorder_results
        .sort_values(
            "final_score",
            ascending=False
        )
        .head(reorder_slots)
    )

    top_discovery = (
        discovery_results
        .sort_values(
            "final_score",
            ascending=False
        )
        .head(discovery_slots)
    )

    # --------------------------------------------------
    # Combine and rank
    # --------------------------------------------------

    combined = pd.concat(
        [
            top_reorders,
            top_discovery
        ],
        ignore_index=True
    )

    combined = combined.drop_duplicates(
        subset=["product_id"],
        keep="first"
    )

    combined = combined.sort_values(
        "final_score",
        ascending=False
    )

    return combined.head(final_k)

def shopping_search(
    user_query,
    customer_id,
    final_k=10
):

    parsed_query = parse_query(
        user_query
    )

    request_type = parsed_query[
        "request_type"
    ]

    reorder_results = pd.DataFrame()

    discovery_results = pd.DataFrame()

    if request_type in [
        "discovery",
        "mixed"
    ]:

        discovery_results = get_discovery_results(
            parsed_query,
            top_k=20
        )

        discovery_results = add_source(
            discovery_results,
            "discovery"
        )

    if request_type in [
        "reorder",
        "mixed"
    ]:

        reorder_results = get_reorder_results(
            customer_id,
            parsed_query,
            top_k=5
        )

        reorder_results = add_source(
            reorder_results,
            "reorder"
        )

    final_results = combine_results(
        reorder_results,
        discovery_results,
        final_k=final_k
    )

    return parsed_query, final_results


if __name__ == "__main__":

    customer_id = 1

    user_query = (
        "Reorder my usual products and "
        "find comfortable shoes under 500"
    )

    parsed_query, results = shopping_search(
        user_query,
        customer_id,
        final_k=10
    )

    print("\n" + "=" * 60)
    print("MIXED SHOPPING SEARCH")
    print("=" * 60)

    print("\nUser Query:")
    print(user_query)

    print("\nParsed Query:")
    print(parsed_query)

    print("\nResults:")
    print("=" * 60)

    if results.empty:

        print("No products found.")

    else:

        for _, product in results.iterrows():

            print(
                f"\nProduct: "
                f"{product['product_name']}"
            )

            print(
                f"Source: "
                f"{product['source']}"
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
                f"Final Score: "
                f"{product['final_score']:.4f}"
            )