"""
Local Embedding Model using Sentence Transformers
MiniLM-L6-v2 for sovereign AI vector operations
Sovereign Core Cycle 20 - No API dependencies
"""

from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from typing import List, Union, Optional
import time

class LocalEmbeddingModel:
    """
    Self-contained local embedding model using MiniLM
    No API keys or external dependencies required
    """

    _instance: Optional['LocalEmbeddingModel'] = None
    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialize()

    def _initialize(self):
        """Initialize the local embedding model"""
        print("🚀 Initializing MiniLM Local Embeddings...")
        print(f"   Model: {self.EMBEDDING_MODEL_NAME}")

        # Detect device
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"   Device: {self.device}")

        # Load model
        print("   Loading embedding model...")
        start_time = time.time()

        self._model = SentenceTransformer(
            self.EMBEDDING_MODEL_NAME,
            device=self.device
        )

        load_time = time.time() - start_time
        print(f"✅ MiniLM initialized in {load_time:.2f}s")
        print(f"   Embedding dimension: {self._model.get_sentence_embedding_dimension()}")
        print(f"   Max sequence length: {self._model.get_max_seq_length()}")

        self._initialized = True

    def embed(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        Generate embeddings for input texts

        Args:
            texts: Single text or list of texts

        Returns:
            List of embedding vectors
        """
        if not isinstance(texts, list):
            texts = [texts]

        if not texts:
            return []

        try:
            # Generate embeddings
            embeddings = self._model.encode(
                texts,
                convert_to_numpy=True,
                normalize_embeddings=True
            )

            # Convert to list of lists for JSON serialization
            return embeddings.tolist()

        except Exception as e:
            print(f"Embedding error: {e}")
            return []

    def embed_single(self, text: str) -> List[float]:
        """
        Generate embedding for single text

        Args:
            text: Input text

        Returns:
            Single embedding vector
        """
        embeddings = self.embed([text])
        return embeddings[0] if embeddings else []

    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts

        Args:
            text1: First text
            text2: Second text

        Returns:
            Cosine similarity score
        """
        embeddings = self.embed([text1, text2])
        if len(embeddings) != 2:
            return 0.0

        # Calculate cosine similarity
        vec1 = np.array(embeddings[0])
        vec2 = np.array(embeddings[1])

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def find_most_similar(self, query: str, candidates: List[str], top_k: int = 5) -> List[tuple]:
        """
        Find most similar texts to query

        Args:
            query: Query text
            candidates: List of candidate texts
            top_k: Number of top results to return

        Returns:
            List of (text, similarity_score) tuples
        """
        if not candidates:
            return []

        # Generate embeddings for all texts
        all_texts = [query] + candidates
        embeddings = self.embed(all_texts)

        if len(embeddings) != len(all_texts):
            return []

        query_embedding = np.array(embeddings[0])
        candidate_embeddings = embeddings[1:]

        # Calculate similarities
        similarities = []
        for i, candidate_embedding in enumerate(candidate_embeddings):
            similarity = np.dot(query_embedding, candidate_embedding)
            similarities.append((candidates[i], similarity))

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        return {
            "model_name": self.EMBEDDING_MODEL_NAME,
            "device": self.device,
            "embedding_dimension": self._model.get_sentence_embedding_dimension(),
            "max_sequence_length": self._model.get_max_seq_length(),
            "initialized": hasattr(self, '_initialized') and self._initialized
        }

# Test function
def test_local_embeddings():
    """Test the local embedding functionality"""
    print("🧪 Testing Local MiniLM Embeddings...")

    embedder = LocalEmbeddingModel()

    # Test basic embedding
    test_texts = [
        "What is viral engagement?",
        "Viral engagement is a strategy for content amplification",
        "Machine learning is transforming AI systems"
    ]

    print("Test texts:")
    for i, text in enumerate(test_texts):
        print(f"  {i+1}. {text}")

    embeddings = embedder.embed(test_texts)
    print(f"✅ Generated {len(embeddings)} embeddings")
    print(f"   Embedding dimension: {len(embeddings[0])}")

    # Test similarity
    similarity = embedder.similarity(test_texts[0], test_texts[1])
    print(f"✅ Similarity between 1 and 2: {similarity:.4".4f"

    # Test most similar
    query = "Explain viral engagement"
    most_similar = embedder.find_most_similar(query, test_texts, top_k=2)
    print(f"✅ Most similar to '{query}':")
    for text, score in most_similar:
        print(f"   {score:.4".4f" {text}")

    return True

if __name__ == "__main__":
    test_local_embeddings()
