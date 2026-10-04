import pandas as pd
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parents[3]

PRODUCT_DATA = (
    BASE_DIR
    / "data"
    / "processed"
    / "products_processed.csv"
)

EMBEDDING_FILE = (
    BASE_DIR
    / "data"
    / "embeddings"
    / "product_embeddings.npy"
)


# Part 1: Load model, products and embeddings

print("=" * 60)
print("SEMANTIC SEARCH")
print("=" * 60)

model = SentenceTransformer("all-MiniLM-L6-v2")

products = pd.read_csv(PRODUCT_DATA)

product_embeddings = np.load(EMBEDDING_FILE)

print("✓ Model loaded")
print(f"✓ Products loaded: {len(products)}")
print(f"✓ Embeddings shape: {product_embeddings.shape}")


# Part 2: Query embedding

def create_query_embedding(query):

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    return query_embedding


# Part 3: Cosine similarity

def calculate_similarity(query_embedding):

    similarities = cosine_similarity(
        query_embedding.reshape(1, -1),
        product_embeddings
    )[0]

    return similarities


# Part 4: Top-K semantic search

def semantic_search(query, top_k=5):

    query_embedding = create_query_embedding(query)

    similarities = calculate_similarity(query_embedding)

    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = products.iloc[top_indices].copy()

    results["similarity_score"] = similarities[top_indices]

    return results


# Test

if __name__ == "__main__":

    query = "I want comfortable shoes for travelling"

    results = semantic_search(query, top_k=5)

    print("\n" + "=" * 60)
    print(f"QUERY: {query}")
    print("=" * 60)

    for _, product in results.iterrows():

        print(f"\nProduct: {product['product_name']}")
        print(f"Category: {product['category']}")
        print(f"Brand: {product['brand']}")
        print(f"Price: {product['price']}")
        print(f"Similarity: {product['similarity_score']:.4f}")
        print(f"Description: {product['description']}")