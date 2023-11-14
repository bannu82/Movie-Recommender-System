import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)


def fetch_poster(movies_id):
    url = f"https://api.themoviedb.org/3/movie/{movies_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0Y2RlMzM1NjBiM2Y5ZjI3ZGZmYzdhOGFiODM0OTYxMiIsInN1YiI6IjY1NGNlYjRiMWFjMjkyN2IyZWJlOTZkMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.dqemjpPznAGptqs59irdULJNaA0zDvpKhGgFA2PGtTc "
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    return " https://image.tmdb.org/t/p/original" + data['poster_path']


# print(fetch_poster(49026))


def recommend(movie):
    movies_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movies_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommend_movies_poster


similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'how would u like to connect ?',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    # col1, col2, col3 = st.columns(3)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
