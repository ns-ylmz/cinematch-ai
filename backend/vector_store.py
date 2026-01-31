import chromadb
import ollama

class MovieVectorStore:
    def __init__(self, path="../data/chroma_db"):
        # 1. set the local file to store the vector database
        self.client = chromadb.PersistentClient(path=path)
        # 2. create the collection or get it if it exists
        self.collection = self.client.get_or_create_collection(
            name="movie_collection",
            metadata={"hnsw:space": "cosine"} # cosine similarity
        )
    
    def get_embedding(self, text):
        """Convert text to embedding using Ollama"""
        response = ollama.embeddings(model="nomic-embed-text", prompt=text)
        return response["embedding"]
    
    def add_movie(self, df):
        """Add the movies that are in the dataframe to the vector store"""
        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for index, row in df.iterrows():
            # a unique id for each record (we can use the Kaggle ID of each movie)
            movie_id = str(row["id"])
            
            # Get embedding for the movie
            vector = self.get_embedding(row["combined_info"])

            ids.append(movie_id)
            embeddings.append(vector)
            documents.append(row["combined_info"]) # original text
            metadatas.append({
                "title": row["title"], 
                "release_date": str(row["release_date"]), 
                "vote_average": row["vote_average"]
            })
        
        # Batch upsert
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        
        print(f"✅ Added {len(ids)} movies to the vector store.")
    
    def search_movies(self, query, n_results=3):
        """Search for movies in the vector store semantically"""
        query_vector = self.get_embedding(query)
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=n_results
        )
        return results

if __name__ == "__main__":
    # Run this script to test the vector store
    import pandas as pd

    # 1. Read the processed movies data
    df = pd.read_csv("../data/movies_processed.csv")
    
    # 2. Initialize the vector store and add the movies to it
    vector_store = MovieVectorStore()
    vector_store.add_movie(df)