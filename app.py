from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from recommender import MovieRecommender
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI(title="Movie Recommender API")
recommender = MovieRecommender()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecRequest(BaseModel):
    title: str

@app.post("/api/recommend")
def recommend_movies(req: RecRequest):
    try:
        recs = recommender.get_recs(req.title, top_n=5)
        if not recs:
            raise HTTPException(status_code=404, detail="Movie not found. Please check your spelling or try another movie.")
        return {"recommendations": recs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
