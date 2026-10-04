from pydantic import BaseModel, Field
from typing import Optional, List


class ShoppingRequest(BaseModel):

    query: str = Field(
        ...,
        min_length=1,
        description="Natural language shopping query"
    )

    customer_id: int = Field(
        default=1,
        ge=1,
        description="Customer ID"
    )

    final_k: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Number of products to return"
    )


class ParsedQuery(BaseModel):

    request_type: str

    query: str

    max_budget: Optional[float] = None

    max_delivery_days: Optional[int] = None

    excluded_brands: List[str] = Field(
        default_factory=list
    )


class ProductResponse(BaseModel):

    product_id: int

    product_name: str

    brand: str

    price: float

    stock: int

    delivery_days: int

    source: str

    score: float


class CartItem(BaseModel):

    product_id: int

    product_name: str

    brand: str

    price: float

    quantity: int

    subtotal: float

    stock: int

    delivery_days: int

    source: str

    score: float


class SmartCartResponse(BaseModel):

    items: List[CartItem]

    item_count: int

    total_amount: float


class ShoppingResponse(BaseModel):

    query: str

    parsed_query: ParsedQuery

    products: List[ProductResponse]

    smart_cart: SmartCartResponse