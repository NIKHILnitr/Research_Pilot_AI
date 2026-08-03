from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def chunk_text(
    text,
    chunk_size=800,
    overlap=100
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


def create_vector_store(text):

    chunks = chunk_text(text)

    embeddings = embedding_model.encode(chunks)

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index, chunks


def retrieve_chunks(
    index,
    chunks,
    question,
    top_k=3
):

    query_embedding = embedding_model.encode(
        [question]
    )

    query_embedding = np.array(
        query_embedding,
        dtype=np.float32
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    retrieved = []

    for idx in indices[0]:
        retrieved.append(chunks[idx])

    return "\n\n".join(retrieved)