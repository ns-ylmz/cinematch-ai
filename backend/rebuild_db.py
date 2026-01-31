from vector_store import MovieVectorStore
import pandas as pd
import shutil
import os

def rebuild():
    # 1. Check the path and the data
    db_path = "../data/chroma_db"
    enriched_csv = "../data/movies_enriched.csv"
    
    if not os.path.exists(db_path):
        print(f"❌ Error: {enriched_csv} not found! Please run 'labeler.py' first.")
        return
    
    # 2. Remove the old database
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
        print("🗑️ Deleted old ChromaDB")
    
    # 3. Read the enriched data
    df_enriched = pd.read_csv(enriched_csv)
    print(f"📄 Loading {len(df_enriched)} enriched movies...")
    
    # 4. Initialize the store and add the movies
    store = MovieVectorStore()
    store.add_movie(df_enriched)
    print("\n✨ Rebuilt the new database successfully!")

if __name__ == "__main__":
    rebuild()    