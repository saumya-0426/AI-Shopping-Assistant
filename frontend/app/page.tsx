"use client";

import { useEffect, useState } from "react";

interface Product {
  product_id: number;
  product_name: string;
  brand: string;
  price: number;
  stock: number;
  delivery_days: number;
  source: string;
  score: number;
}

interface CartItem {
  product_id: number;
  product_name: string;
  brand: string;
  price: number;
  quantity: number;
  subtotal: number;
  stock: number;
  delivery_days: number;
  source: string;
  score: number;
}

interface SmartCart {
  items: CartItem[];
  item_count: number;
  total_amount: number;
}

interface ParsedQuery {
  request_type: string;
  query: string;
  max_budget: number | null;
  max_delivery_days: number | null;
  excluded_brands: string[];
}

interface SearchResponse {
  customer_id: number;
  query: string;
  parsed_query: ParsedQuery;
  products: Product[];
  smart_cart: SmartCart;
}

export default function Home() {
  const [customers, setCustomers] = useState<number[]>([]);

  const [customerId, setCustomerId] = useState<number>(1);

  const [query, setQuery] = useState("");

  const [results, setResults] =
    useState<SearchResponse | null>(null);

  const [loadingCustomers, setLoadingCustomers] =
    useState(true);

  const [loadingSearch, setLoadingSearch] =
    useState(false);

  const [error, setError] = useState("");

  // ============================================================
  // LOAD ALL CUSTOMERS
  // ============================================================

  useEffect(() => {
    const loadCustomers = async () => {
      try {
        setLoadingCustomers(true);
        setError("");

        const response = await fetch(
          "http://127.0.0.1:8000/api/customers"
        );

        if (!response.ok) {
          throw new Error(
            "Failed to load customers"
          );
        }

        const data = await response.json();

        // IMPORTANT:
        // Do NOT use slice(0, 10)
        // We want every valid customer ID.

        setCustomers(data.customers);

        // Set first available customer as default
        if (
          data.customers &&
          data.customers.length > 0
        ) {
          setCustomerId(data.customers[0]);
        }

      } catch (err) {
        console.error(err);

        setError(
          "Unable to load customers. Make sure the backend is running."
        );

      } finally {
        setLoadingCustomers(false);
      }
    };

    loadCustomers();
  }, []);

  // ============================================================
  // SEARCH
  // ============================================================

  const handleSearch = async () => {
    if (!query.trim()) {
      setError("Please enter a shopping query.");
      return;
    }

    try {
      setLoadingSearch(true);
      setError("");

      const response = await fetch(
        "http://127.0.0.1:8000/api/shop",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            customer_id: customerId,
            query: query,
            final_k: 10,
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
          errorData.detail ||
            "Shopping search failed"
        );
      }

      const data: SearchResponse =
        await response.json();

      setResults(data);

    } catch (err) {
      console.error(err);

      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError(
          "Something went wrong while searching."
        );
      }

    } finally {
      setLoadingSearch(false);
    }
  };

  // ============================================================
  // ENTER KEY SEARCH
  // ============================================================

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      handleSearch();
    }
  };

  // ============================================================
  // UI
  // ============================================================

  return (
    <main
      style={{
        maxWidth: "1100px",
        margin: "0 auto",
        padding: "40px 20px",
        fontFamily: "Arial, sans-serif",
      }}
    >

      {/* ====================================================== */}
      {/* HEADER */}
      {/* ====================================================== */}

      <div
        style={{
          textAlign: "center",
          marginBottom: "35px",
        }}
      >
        <h1
          style={{
            fontSize: "36px",
            marginBottom: "10px",
          }}
        >
          AI Shopping Assistant
        </h1>

        <p
          style={{
            color: "#666",
            fontSize: "16px",
          }}
        >
          Personalized product discovery and
          intelligent reordering
        </p>
      </div>

      {/* ====================================================== */}
      {/* SEARCH SECTION */}
      {/* ====================================================== */}

      <div
        style={{
          padding: "25px",
          border: "1px solid #ddd",
          borderRadius: "12px",
          marginBottom: "30px",
        }}
      >

        {/* CUSTOMER SELECTOR */}

        <label
          style={{
            display: "block",
            fontWeight: "bold",
            marginBottom: "8px",
          }}
        >
          Select Customer
        </label>

        <select
          value={customerId}
          onChange={(event) =>
            setCustomerId(
              Number(event.target.value)
            )
          }
          disabled={loadingCustomers}
          style={{
            width: "100%",
            padding: "12px",
            fontSize: "16px",
            borderRadius: "8px",
            border: "1px solid #ccc",
            marginBottom: "20px",
          }}
        >

          {loadingCustomers ? (
            <option>
              Loading customers...
            </option>
          ) : customers.length === 0 ? (
            <option>
              No customers found
            </option>
          ) : (

            /*
             * IMPORTANT CHANGE:
             *
             * We use customers.map()
             *
             * NOT:
             *
             * customers.slice(0, 10).map(...)
             *
             * Therefore every valid customer is shown.
             */

            customers.map((customer) => (
              <option
                key={customer}
                value={customer}
              >
                Customer {customer}
              </option>
            ))

          )}

        </select>

        {/* QUERY */}

        <label
          style={{
            display: "block",
            fontWeight: "bold",
            marginBottom: "8px",
          }}
        >
          What are you looking for?
        </label>

        <div
          style={{
            display: "flex",
            gap: "10px",
          }}
        >

          <input
            type="text"
            value={query}
            onChange={(event) =>
              setQuery(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="e.g. comfortable shoes under 500"
            style={{
              flex: 1,
              padding: "12px",
              fontSize: "16px",
              borderRadius: "8px",
              border: "1px solid #ccc",
            }}
          />

          <button
            onClick={handleSearch}
            disabled={
              loadingSearch ||
              loadingCustomers ||
              customers.length === 0
            }
            style={{
              padding: "12px 25px",
              fontSize: "16px",
              borderRadius: "8px",
              border: "none",
              cursor: "pointer",
            }}
          >
            {loadingSearch
              ? "Searching..."
              : "Search"}
          </button>

        </div>

      </div>

      {/* ====================================================== */}
      {/* ERROR */}
      {/* ====================================================== */}

      {error && (
        <div
          style={{
            padding: "15px",
            marginBottom: "25px",
            borderRadius: "8px",
            border: "1px solid #ffcccc",
          }}
        >
          {error}
        </div>
      )}

      {/* ====================================================== */}
      {/* SEARCHING */}
      {/* ====================================================== */}

      {loadingSearch && (
        <div
          style={{
            textAlign: "center",
            padding: "30px",
          }}
        >
          Searching as{" "}
          <strong>
            Customer {customerId}
          </strong>
          ...
        </div>
      )}

      {/* ====================================================== */}
      {/* RESULTS */}
      {/* ====================================================== */}

      {results && !loadingSearch && (
        <>

          <div
            style={{
              marginBottom: "30px",
            }}
          >

            <h2>
              Customer {results.customer_id}'s Results
            </h2>

            <p>
              <strong>Query:</strong>{" "}
              {results.query}
            </p>

            <p>
              <strong>Request Type:</strong>{" "}
              {results.parsed_query.request_type}
            </p>

          </div>

          {/* ================================================== */}
          {/* PRODUCTS */}
          {/* ================================================== */}

          <h2
            style={{
              marginBottom: "20px",
            }}
          >
            Recommended Products
          </h2>

          {results.products.length === 0 ? (

            <div
              style={{
                padding: "30px",
                border: "1px solid #ddd",
                borderRadius: "10px",
                marginBottom: "30px",
              }}
            >
              No products found for this request.
            </div>

          ) : (

            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(auto-fit, minmax(280px, 1fr))",
                gap: "20px",
                marginBottom: "40px",
              }}
            >

              {results.products.map(
                (product) => (

                  <div
                    key={product.product_id}
                    style={{
                      border: "1px solid #ddd",
                      borderRadius: "12px",
                      padding: "20px",
                    }}
                  >

                    <h3>
                      {product.product_name}
                    </h3>

                    <p>
                      <strong>
                        Brand:
                      </strong>{" "}
                      {product.brand}
                    </p>

                    <p>
                      <strong>
                        Price:
                      </strong>{" "}
                      ₹{product.price}
                    </p>

                    <p>
                      <strong>
                        Stock:
                      </strong>{" "}
                      {product.stock}
                    </p>

                    <p>
                      <strong>
                        Delivery:
                      </strong>{" "}
                      {product.delivery_days} days
                    </p>

                    <p>
                      <strong>
                        Source:
                      </strong>{" "}
                      {product.source}
                    </p>

                    <p>
                      <strong>
                        AI Score:
                      </strong>{" "}
                      {product.score.toFixed(4)}
                    </p>

                  </div>

                )
              )}

            </div>

          )}

          {/* ================================================== */}
          {/* SMART CART */}
          {/* ================================================== */}

          <div
            style={{
              border: "1px solid #ddd",
              borderRadius: "12px",
              padding: "25px",
            }}
          >

            <h2>
              Smart Cart
            </h2>

            <p>
              <strong>Items:</strong>{" "}
              {results.smart_cart.item_count}
            </p>

            <p
              style={{
                fontSize: "20px",
                fontWeight: "bold",
              }}
            >
              Total: ₹
              {results.smart_cart.total_amount}
            </p>

            <div
              style={{
                marginTop: "20px",
              }}
            >

              {results.smart_cart.items.map(
                (item) => (

                  <div
                    key={item.product_id}
                    style={{
                      display: "flex",
                      justifyContent:
                        "space-between",
                      padding: "12px 0",
                      borderBottom:
                        "1px solid #eee",
                    }}
                  >

                    <span>
                      {item.product_name}
                    </span>

                    <span>
                      ₹{item.subtotal}
                    </span>

                  </div>

                )
              )}

            </div>

          </div>

        </>
      )}

    </main>
  );
}