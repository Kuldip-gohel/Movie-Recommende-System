import streamlit as st
import pickle
import pandas as pd
import requests


# ----------------------------------------

st.markdown("""
<style>

/* Full page background */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.6)),
                url("https://images.unsplash.com/photo-1524985069026-dd778a71c7b4");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}


.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: white;
}


.movie-card {
    text-align: center;
    background-color: rgba(28, 28, 28, 0.85);
    padding: 10px;
    border-radius: 12px;
    transition: 0.3s;
}

.movie-card:hover {
    transform: scale(1.05);
}

.movie-title {
    font-size: 14px;
    color: white;
    margin-top: 10px;
}
                       
body {
    background-color: #0E1117;
}
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: white;
}
.movie-card {
    text-align: center;
    background-color: #1c1c1c;
    padding: 10px;
    border-radius: 10px;
}
.movie-title {
    font-size: 14px;
    color: white;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b446681075b63a1a26cfff75f7a54ccd"
        response = requests.get(url)
        data = response.json()

        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies_df.iloc[i[0]].movie_id
       
        recommended_movies.append(movies_df.iloc[i[0]].title)
         # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters



movies_df = pickle.load(open('movies.pkl','rb'))
movies_list = movies_df['title'].values

similarity = pickle.load(open('similarity.pkl','rb'))

# show title in webpage
st.markdown("<div class='title'>🎬 Movie Recommender System</div>", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    '',
    movies_list
)

st.markdown("<br>", unsafe_allow_html=True)
if st.button('🎯 Recommend Movies'):
    names,posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.markdown(f"<p style='text-align: center;'>{names[0]}</p>", unsafe_allow_html=True)

    with col2:
        st.image(posters[1])
        st.markdown(f"<p style='text-align: center;'>{names[1]}</p>", unsafe_allow_html=True)

    with col3:
        st.image(posters[2])
        st.markdown(f"<p style='text-align: center;'>{names[2]}</p>", unsafe_allow_html=True)

    with col4:
        st.image(posters[3])
        st.markdown(f"<p style='text-align: center;'>{names[3]}</p>", unsafe_allow_html=True)

    with col5:
        st.image(posters[4])
        st.markdown(f"<p style='text-align: center;'>{names[4]}</p>", unsafe_allow_html=True)