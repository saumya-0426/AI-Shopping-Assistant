const API_URL = "http://127.0.0.1:8000";


export interface ShoppingRequest {
    query: string;
    customer_id: number;
    final_k: number;
}


export interface ParsedQuery {
    request_type: string;
    query: string;
    max_budget: number | null;
    max_delivery_days: number | null;
    excluded_brands: string[];
}


export interface Product {
    product_id: number;
    product_name: string;
    brand: string;
    price: number;
    stock: number;
    delivery_days: number;
    source: string;
    score: number;
}


export interface CartItem {
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


export interface SmartCart {
    items: CartItem[];
    item_count: number;
    total_amount: number;
}


export interface ShoppingResponse {
    query: string;
    parsed_query: ParsedQuery;
    products: Product[];
    smart_cart: SmartCart;
}


export async function searchProducts(
    request: ShoppingRequest
): Promise<ShoppingResponse> {

    const response = await fetch(
        `${API_URL}/api/shop`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(request)
        }
    );


    const data = await response.json();


    if (!response.ok) {

        const message =
            data?.error?.message ||
            data?.detail?.message ||
            "Something went wrong.";

        throw new Error(message);
    }


    return data;
}