from pathlib import Path

import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.app.ai.mixed_search import shopping_search
from backend.app.ai.smart_cart import build_smart_cart


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="AI Shopping Assistant",
    description="Natural language shopping assistant",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST SCHEMA
# ============================================================

class ShoppingRequest(BaseModel):

    customer_id: int

    query: str

    final_k: int = 10


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def home():

    return {
        "message": "AI Shopping Assistant API is running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# GET ALL CUSTOMERS
# ============================================================

@app.get("/api/customers")
def get_customers():

    try:

        # main.py:
        # Shopping/backend/app/main.py
        #
        # parents[0] = app
        # parents[1] = backend
        # parents[2] = Shopping

        base_dir = Path(__file__).resolve().parents[2]

        transactions_file = (
            base_dir
            / "data"
            / "raw"
            / "transactions.csv"
        )

        if not transactions_file.exists():

            raise HTTPException(
                status_code=500,
                detail=(
                    "transactions.csv not found at: "
                    f"{transactions_file}"
                )
            )

        transactions = pd.read_csv(
            transactions_file
        )

        if "customer_id" not in transactions.columns:

            raise HTTPException(
                status_code=500,
                detail=(
                    "customer_id column not found "
                    "in transactions.csv"
                )
            )

        customer_ids = (
            transactions["customer_id"]
            .dropna()
            .astype(int)
            .unique()
            .tolist()
        )

        customer_ids.sort()

        return {
            "customers": customer_ids,
            "count": len(customer_ids)
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to load customers: {str(e)}"
        )


# ============================================================
# SHOPPING API
# ============================================================

@app.post("/api/shop")
def shop(
    request: ShoppingRequest
):

    try:

        # ----------------------------------------------------
        # Validate customer ID
        # ----------------------------------------------------

        if request.customer_id <= 0:

            raise HTTPException(
                status_code=400,
                detail="customer_id must be greater than 0"
            )

        # ----------------------------------------------------
        # Validate query
        # ----------------------------------------------------

        if not request.query.strip():

            raise HTTPException(
                status_code=400,
                detail="Shopping query cannot be empty"
            )

        # ----------------------------------------------------
        # Validate final_k
        # ----------------------------------------------------

        if request.final_k <= 0:

            raise HTTPException(
                status_code=400,
                detail="final_k must be greater than 0"
            )

        if request.final_k > 50:

            raise HTTPException(
                status_code=400,
                detail="final_k cannot be greater than 50"
            )

        # ----------------------------------------------------
        # Run AI shopping search
        # ----------------------------------------------------

        parsed_query, results = shopping_search(
            request.query,
            request.customer_id,
            final_k=request.final_k
        )

        # ----------------------------------------------------
        # Build smart cart
        # ----------------------------------------------------

        cart = build_smart_cart(
            results
        )

        # ----------------------------------------------------
        # Convert DataFrame results to JSON
        # ----------------------------------------------------

        products = []

        for _, product in results.iterrows():

            products.append(
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

                    "price": float(
                        product["price"]
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

        # ----------------------------------------------------
        # Final response
        # ----------------------------------------------------

        return {
            "customer_id": request.customer_id,

            "query": request.query,

            "parsed_query": parsed_query,

            "products": products,

            "smart_cart": cart
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Shopping search failed: {str(e)}"
        )