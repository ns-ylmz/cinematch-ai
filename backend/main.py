from fastapi import FastAPI
from pydantic import BaseModel
from vector_store import MovieVectorStore
import ollama
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Movie Recommender API")
store = MovieVectorStore()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow everything during development
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/search")
async def search_movies(request : QueryRequest):
    # 1 Step: Retrieve 3 nearest movies from the vector store (Retrieval)
    results = store.search_movies(request.query, n_results=3)

    # Turn the raw data coming from the vector store into a text
    context_list = []
    for i in range(len(results["documents"][0])):
        title = results["metadatas"][0][i]["title"]
        doc = results["documents"][0][i]
        context_list.append(f"Movie: {title}\nDetail: {doc}")

    context_text = "\n\n".join(context_list)

    # 2 Step: Send the context and the query to the LLM (DeepSeek) (Generation)
    prompt = f"""
    SYSTEM ROLE: You are an expert cinematic assistant and movie recommender. 
    Your goal is to analyze the movies retrieved from the database and determine their relevance to the user's request.

    USER QUERY: "{request.query}"

    RETRIEVED DATA FROM VECTOR STORE:
    {context_text}

    INSTRUCTIONS:
    1. RELEVANCE CHECK: Critically evaluate if the retrieved movies actually match the user's query intent. 
    2. FILTERING: If a movie is irrelevant (e.g., user asks for 'Crime' but the database returns 'Romance'), do NOT recommend it or clearly state its mismatch.
    3. REASONING: For the relevant movies, provide a one-sentence concise explanation of why they match the query.
    4. LANGUAGE: Provide your final recommendation and explanations in TURKISH.
    5. OUTPUT FORMAT: Be conversational but professional.
    """

    print(f"🤖 DeepSeek is thinking: {request.query}")
    response = ollama.generate(model="deepseek-r1:8b", prompt=prompt)

    # Split the response to get the final answer
    ai_answer = response["response"].split("</think>")[-1].strip()
    
    return {
        "user_query": request.query,
        "recommended_movies": ai_answer,
        "raw_data_source": results["metadatas"][0] # for logging which data was used
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
