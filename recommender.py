import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize

class MovieRecommender:
    def __init__(self, data_path='data/ml-32m'):
        self.data_path = data_path
        self.df = None
        self.count_mat = None
        self.indices = None
        self._load_data()

    def _load_data(self):
        print("Loading ML-32M datasets...")
        movies = pd.read_csv(os.path.join(self.data_path, 'movies.csv'))
        
        # We need tags to enrich the soup
        tags = pd.read_csv(os.path.join(self.data_path, 'tags.csv'), usecols=['movieId', 'tag'])
        tags_grouped = tags.groupby('movieId')['tag'].apply(lambda x: ' '.join(x.astype(str))).reset_index()
        
        df = movies.merge(tags_grouped, on='movieId', how='left')
        
        # Load ratings to get vote_average (optimized load for memory)
        print("Calculating average ratings...")
        ratings = pd.read_csv(os.path.join(self.data_path, 'ratings.csv'), 
                              usecols=['movieId', 'rating'], 
                              dtype={'movieId': np.int32, 'rating': np.float32})
        avg_ratings = ratings.groupby('movieId')['rating'].mean().reset_index()
        avg_ratings.rename(columns={'rating': 'vote_average'}, inplace=True)
        
        df = df.merge(avg_ratings, on='movieId', how='left')

        # Clean fields
        df['tag'] = df['tag'].fillna('')
        df['genres'] = df['genres'].str.replace('|', ' ', regex=False).str.lower()
        
        # Extract release date and clean title
        df['release_date'] = df['title'].str.extract(r'\((\d{4})\)', expand=False)
        df['clean_title'] = df['title'].str.replace(r'\s*\(\d{4}\)', '', regex=True)
        
        def fix_articles(t):
            if isinstance(t, str):
                for article in [', The', ', A', ', An', ', Les', ', Le', ', La', ', L\'', ', Il']:
                    if t.endswith(article):
                        return article[2:] + ' ' + t[:-len(article)]
            return t
            
        df['clean_title'] = df['clean_title'].apply(fix_articles)
        df['clean_title'] = df['clean_title'].fillna('')

        # Create soup
        df['soup'] = df['genres'] + ' ' + df['tag']

        print("Vectorizing...")
        count = CountVectorizer(stop_words='english')
        self.count_mat = count.fit_transform(df['soup'])
        self.count_mat = normalize(self.count_mat, norm='l2', axis=1)
        
        # Use clean title as our index for easier searching
        self.df = df.reset_index(drop=True)
        self.indices = pd.Series(self.df.index, index=self.df['clean_title'].str.lower())
        print("Model ready!")

    def get_recs(self, title, top_n=5):
        title_lower = title.lower()
        
        if title_lower not in self.indices:
            # Try partial match (using regex escapes to avoid broken searches)
            try:
                matches = self.indices.index[self.indices.index.str.contains(title_lower, na=False, regex=False)]
            except:
                return []
            if len(matches) == 0:
                return []
            idx = self.indices[matches[0]]
            if isinstance(idx, pd.Series): 
                idx = idx.iloc[0]
        else:
            idx = self.indices[title_lower]
            if isinstance(idx, pd.Series): 
                idx = idx.iloc[0]

        # Compute cosine similarity for this movie only against all movies
        # Since self.count_mat is already L2 normalized, dot product is exactly cosine similarity
        sim_scores_array = self.count_mat[idx].dot(self.count_mat.T).toarray().flatten()
        
        # Only suggest movies that have at least somewhat similar tags/genres to avoid empty nonsense
        sim_scores = list(enumerate(sim_scores_array))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top matching (excluding itself, which is at index 0)
        sim_scores = sim_scores[1:top_n+1]
        movie_indices = [i[0] for i in sim_scores]
        
        # Rename 'tag' to 'overview' so UI displays it nicely
        columns = ['title', 'vote_average', 'release_date', 'tag']
        res = self.df[columns].iloc[movie_indices].copy()
        res.rename(columns={'tag': 'overview'}, inplace=True)
        
        res['overview'] = res['overview'].apply(lambda x: x[:300] + '...' if len(x) > 300 else x)
        
        # Fill na
        res.fillna('', inplace=True)
        return res.to_dict('records')
