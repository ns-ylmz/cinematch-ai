from vector_store import MovieVectorStore

def run_semantic_test():
    store = MovieVectorStore()

    # Test queries
    queries = [
        "A movie about space travel and loneliness",
        "Christopher Nolan style mind-bending thrillers",
        "İnsan zihninin derinlerine inen rüya temalı filmler",
        "Crime, Power, Family"
    ]
    
    for q in queries:
        print(f"\n🔍 Query: '{q}'")
        results = store.search_movies(q, n_results=3)
        
        # Print the results
        for i in range(len(results['ids'][0])):
            title = results['metadatas'][0][i]['title']
            score = results['distances'][0][i] # lower is better, 0 is perfect match
            print(f"🎬 {i+1}: {title} (Score: {score:.4f})")

if __name__ == "__main__":
    run_semantic_test()