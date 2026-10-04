# AI Shopping Assistant

## Author
**Saumya Kumari**  
Computer Engineering Student

## Project Title
**AI Shopping Assistant — Personalized Natural Language Shopping & Reorder System**

## Introduction

AI Shopping Assistant is an AI-powered e-commerce system that allows users to search for products using natural language. It combines semantic product search with customer purchase history to provide personalized recommendations and automatically generate a smart cart.

## Problem

Traditional shopping systems mainly depend on keywords and fixed filters. They often fail to understand natural-language intent or personalize recommendations based on what a customer has purchased before.

For example, a user may ask:

> "Reorder my usual products and find comfortable shoes under 500"

The system should understand both the reorder request and the new product discovery request.

## Tech Stack

- **Frontend:** Next.js, React, TypeScript
- **Backend:** Python, FastAPI
- **AI/ML:** Groq LLM, Sentence Transformers
- **Data Processing:** Pandas, NumPy
- **Search:** Semantic Search, Cosine Similarity
- **Database/Data:** CSV-based dataset
- **Tools:** Git, GitHub, REST API

## Dataset

The project uses the **Customer Purchase History Dataset** from Kaggle:

[Customer Purchase History Dataset](https://www.kaggle.com/datasets/mmumairkhattak/customer-purchase-history-dataset)

Main files used:

- `customers.csv`
- `products.csv`
- `transactions.csv`

## How We Solved It

The system follows an end-to-end AI shopping pipeline:

```text
User Query
    ↓
LLM Query Parser
    ↓
Intent + Constraints
    ↓
Semantic Search / Reorder Engine
    ↓
Constraint Filtering
    ↓
Result Ranking
    ↓
Smart Cart
    ↓
Next.js Frontend


The LLM extracts the shopping intent, budget, delivery requirements, and brand exclusions. Sentence Transformers generate product embeddings for semantic search, while the reorder engine analyzes purchase frequency and recency.

For mixed searches, both discovery and reorder results are combined and ranked.

## Main Functionality

- Natural-language product search
- Discovery, reorder, and mixed search
- Semantic product recommendations
- Personalized reorder recommendations
- Budget filtering
- Delivery-time filtering
- Brand exclusion
- Stock availability filtering
- AI-based result ranking
- Customer selection and personalization
- Automatic smart-cart generation
- FastAPI REST API
- Interactive Next.js frontend

### Example Queries

```text
"comfortable shoes under 500"

"Reorder my usual products"

"Reorder my usual products and find comfortable shoes under 500"

"Find comfortable shoes under 500, deliver within 3 days, and don't show Brand 11"


## Results

The system successfully converts natural-language requests into structured queries and returns ranked products based on semantic relevance, purchase history, and user constraints.

### Example

```text
Query: comfortable shoes under 500

Product: Product 370
Brand: Brand 1
Price: ₹252.35
Delivery: 1 day
Source: discovery
AI Score: 0.5746


The system also generates a smart cart containing the recommended products and automatically calculates the total amount.

## Outcomes

The project successfully demonstrates an end-to-end personalized shopping workflow:

**Natural Language → AI Understanding → Search → Personalization → Ranking → Smart Cart**

It provides a foundation for building more intelligent and personalized e-commerce platforms.

## Limitations

- Uses a static Kaggle dataset instead of live e-commerce data.
- Product quality depends on the available product descriptions.
- Recommendations depend on available customer purchase history.
- No real-time payment or checkout system.
- Inventory is not connected to a live inventory service.
- LLM query parsing requires an external Groq API.

## Future Improvements

- Real-time inventory and pricing
- User authentication
- Product images and reviews
- Advanced recommendation models
- Conversation memory
- Voice-based shopping
- Real payment and checkout
- Agentic shopping workflows
- Multi-store product comparison
Real payment and checkout
Agentic shopping workflows
Multi-store product comparison
