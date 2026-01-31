import pandas as pd
import uuid

def prepare_data(file_path):
    # 1. Load the data
    df = pd.read_csv(file_path)

    # 2. Select the required columns
    # 'overview' would be our embedding source
    columns_to_keep = ['id','title', 'overview', 'release_date', 'vote_average']
    df = df[columns_to_keep]

    # 3. Clean up: Remove the movies that don't have an overview from the system
    initial_count = len(df)
    df = df.dropna(subset=['overview'])
    final_count = len(df)
    print(f"🧹 Removed {initial_count - final_count} movies with missing overviews.")

    # 4. Prepare for Auto-Labeling (add genre column as default value and we will populate it later by using DeepSeek)
    df['genre'] = 'Pending AI Labeling'
    
    # 5. Create context for embedding
    df['combined_info'] = df.apply(
        lambda row: f"Title: {row['title']}. Description: {row['overview']}",
        axis=1
    )

    # 6. Start with the small sample to test the pipeline (we will use the full dataset later)
    df_sample = df.head(100).copy()

    print(f"✅ Data prepared! {len(df_sample)} movies ready.")
    return df_sample

if __name__ == "__main__":
    # Check the path of the dataset
    try:
        movies_df = prepare_data("../data/movies.csv")
        # Display the sample output
        print("\n--- The first 3 movies in the dataset ---")
        print(movies_df[['title', 'combined_info']].head(3))

        # Save the processed data to a new CSV file (we will use this file to generate embeddings)
        movies_df.to_csv("../data/movies_processed.csv", index=False)
    except FileNotFoundError:
        print("❌ Error: './data/movies.csv' not found. Please check the path.")
    

    
    
    
    
