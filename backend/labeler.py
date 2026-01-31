import ollama
import pandas as pd
import time

def get_ai_labels(title, overview):
    # Prompt Engineering: We are giving the AI a role, a task, and a specific output format.
    # We're asking for english keywords because the embedding model is much stronger in english.
    prompt = f"""
    You are a professional movie critic. Analyze the movie below and provide:
    1. A single main genre.
    2. Exactly 3 descriptive keywords in English.
    
    Return ONLY the result in this format: Genre | Keyword1, Keyword2, Keyword3
    
    Movie Title: {title}
    Description: {overview}
    """

    try:
        response = ollama.generate(model="deepseek-r1:8b", prompt=prompt)
        # Clean up the thinking process and get the actual response
        output = response['response'].split('</think>')[-1].strip()
        return output
    except Exception as e:
        print(f"Error labeling {title}: {e}")
        return "Unknown | Unknown, Unknown, Unknown"

def start_enrichment():
    # Load the processed data
    df = pd.read_csv("../data/movies_processed.csv")

    # Enrich the first 10 movies with AI labels to test the pipeline
    sample_size = 10
    print(f"🤖 Starting AI Labeling for {sample_size} movies...")
    
    enriched_data = []

    for index, row in df.head(sample_size).iterrows():
        print(f"🎬 Processing: {row['title']}...")
        labels = get_ai_labels(row['title'], row['overview'])

        try:
            genre_part, keywords_part = labels.split('|')
            row['genre'] = genre_part.strip()
            row['combined_info'] = f"Title: {row['title']}. Genre: {row['genre']}. Keywords: {keywords_part.strip()}. Overview: {row['overview']}" 
        except:
            pass # Don't do anything if the format is not correct
        
        # Add the enriched data to the list
        enriched_data.append(row)
        # Be nice to the API
        time.sleep(1)
    
    # Convert the list to a DataFrame
    enriched_df = pd.DataFrame(enriched_data)
    # Save the enriched data to a new CSV file
    enriched_df.to_csv("../data/movies_enriched.csv", index=False)
    
    print("\n✅ AI Labeling completed! and saved as 'movies_enriched.csv'")

if __name__ == "__main__":
    start_enrichment()