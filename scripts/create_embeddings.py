import pandas as pd
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DATA = (
    BASE_DIR
    / "data"
    / "processed"
    / "products_processed.csv"
)

EMBEDDING_DIR = BASE_DIR / "data" / "embeddings"
EMBEDDING_FILE = EMBEDDING_DIR / "product_embeddings.npy"


# Part 1: Load model
print("=" * 60)
print("SENTENCE TRANSFORMER EMBEDDING PIPELINE")
print("=" * 60)

print("\nLoading Sentence Transformer model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("✓ Model loaded")


# Part 2: Load product data
products = pd.read_csv(PROCESSED_DATA)

print("\n✓ Dataset loaded")
print(f"Number of products: {len(products)}")

if "product_text" not in products.columns:
    raise ValueError("product_text column not found")

if products["product_text"].isnull().any():
    raise ValueError("Some products have missing product_text")

print("✓ product_text validation passed")


# Part 3: Generate embeddings
print("\nGenerating embeddings...")

texts = products["product_text"].tolist()

embeddings = model.encode(
    texts,
    show_progress_bar=True,
    normalize_embeddings=True
)

print("\n✓ Embeddings generated")
print("Embedding shape:", embeddings.shape)


# Part 4: Save embeddings
EMBEDDING_DIR.mkdir(parents=True, exist_ok=True)

np.save(
    EMBEDDING_FILE,
    embeddings
)

print("\n✓ Embeddings saved")
print(f"Location: {EMBEDDING_FILE}")

print("\n" + "=" * 60)
print("STAGE 3 COMPLETED")
print("=" * 60)