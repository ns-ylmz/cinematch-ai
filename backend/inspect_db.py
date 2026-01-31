from vector_store import MovieVectorStore

store = MovieVectorStore()

res = store.collection.get()

print(f"Total number of records in the vector store: {len(res['ids'])}")

for i in range(len(res['ids'])):
    print(f"--- Record {i+1} ---")
    print(f"ID: {res['ids'][i]}")
    print(f"Text (Document): {res['documents'][i][:200]}...")
    print(f"Metadata: {res['metadatas'][i]}")
    print("-" * 20)