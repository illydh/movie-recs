# Movie Recommender

A content-based movie recommendation engine built with Python, FastAPI, and Vanilla JS. This application allows users to find their next favorite films by analyzing plot keywords, genres, and user-generated tags from the massive MovieLens 32M dataset.

## Overview

- **High-Performance Inference Optimization:** Refactored standard similarity computation from $O(N^2)$ global matrix comparisons to optimized $O(N)$ dot product operations using pre-calculated L2-normalized sparse vectors. This achieved a **99.9% reduction in latency**, bringing inference time from over 2 minutes down to **~100ms**.
- **Big Data Handling (32M Records):** Engineered a memory-efficient data pipeline to ingest and process the **MovieLens 32M dataset** (32 million ratings, 87k+ movies, 2M+ tags).
- **Asynchronous API Design:** Implemented a robust backend using **FastAPI**, leveraging asynchronous request handling for seamless interaction between the AI model and the web interface.
- **Intelligent Text Processing:** Built a custom feature engineering pipeline ("metadata soup") that aggregates multidimensional data (genres, user tags, release years) and employs **Scikit-learn's CountVectorizer** for feature extraction.
- **Premium UX/UI:** Designed a modern, responsive frontend using **Vanilla JavaScript and CSS**, featuring glassmorphism aesthetics, background lighting animations, and staggered UI transitions for a premium user experience.

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **ML/Processing:** Scikit-learn, Pandas, NumPy
- **Frontend:** Vanilla HTML5, CSS3 (Glassmorphism), JavaScript (ES6+)
- **Dataset:** MovieLens 32M

## Getting Started

### 1. Prerequisites

- Python 3.10+
- The MovieLens 32M dataset stored in `data/ml-32m/` (specifically `movies.csv`, `tags.csv`, and `ratings.csv`).

### 2. Setup Environment

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install fastapi uvicorn pandas scikit-learn
```

### 3. Start the Server

```bash
python app.py
```

_Note: The first startup may take 30-60 seconds as it vectorizes the 32M dataset. Subsequent searches are nearly instantaneous._

### 4. Access the App

Open your browser and navigate to:
[http://localhost:8000](http://localhost:8000)

## Citation

> F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4, Article 19 (December 2015), 19 pages. DOI: [10.1145/2827872](http://dx.doi.org/10.1145/2827872)
