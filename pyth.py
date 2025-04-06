import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    
    if "poster_path" in data and data["poster_path"]:
        return "http://image.tmdb.org/t/p/w500" + data["poster_path"]
    else:
        return "https://via.placeholder.com/160x240?text=No+Image"

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

# Load movies and similarity data
movies_dict = pickle.load(open("movie_list.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Sample movies classified by genre
genre_movies = {
    "Action": ["Mad Max: Fury Road", "Gladiator", "Die Hard", "Avengers: Endgame", "The Dark Knight Rises"],
    "Thriller": ["Inception", "Se7en", "Zodiac", "Gone Girl", "Shutter Island"],
    "Fictional": ["Interstellar", "Dune", "The Matrix", "Blade Runner 2049", "The Martian"],
    "Fantasy": ["Harry Potter", "The Lord of the Rings", "Pirates of the Caribbean", "The Chronicles of Narnia", "Maleficent"],
    "Rom-Com": ["Crazy Rich Asians", "The Proposal", "10 Things I Hate About You", "Notting Hill", "Love Actually"],
    "Comedy": ["Superbad", "The Hangover", "Step Brothers", "Dumb and Dumber", "Anchorman"]
}

# Streamlit UI
st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox("Select a Movie:", movies["title"].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    # Display recommended movies
    st.subheader("Recommended Movies:")
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], width=160)
            st.markdown(f"**{names[idx]}**")

# Display movies by genre
st.subheader("Movies")
for genre, movie_list in genre_movies.items():
    st.markdown(f"### {genre}")

    cols = st.columns(5)
    for idx, movie in enumerate(movie_list):
        with cols[idx % 5]:  # Distribute movies evenly in rows
            # Fetch poster from TMDb API
            response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key=8265bd1679663a7ea12ac168da84d2e8&query={movie}")
            data = response.json()
            poster_url = "https://via.placeholder.com/160x240?text=No+Image"
            if data["results"]:
                poster_url = "http://image.tmdb.org/t/p/w500" + data["results"][0]["poster_path"]

            st.image(poster_url, width=160)
            st.markdown(f"**{movie}**")
