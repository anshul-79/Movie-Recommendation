import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Custom CSS for light purple background and black text
st.markdown(
    """
    <style>
    .stApp {
        background-color: #E6E6FA;
    }
    .main-title {
        color: black;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }
    .label-text {
        color: black;
        font-size: 1.2rem;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .recommendation-container {
        display: flex;
        overflow-x: auto; /* Enable horizontal scrolling */
        margin-top: 20px;
        padding: 10px; /* Add padding to container */
    }
    .recommendation-item {
        text-align: center;
        margin-right: 20px; /* Add some space between items */
    }
    .recommendation-item img {
        width: 100px;
        height: 150px;
        border-radius: 10px;
    }
    .recommendation-item div {
        color: black;
        font-size: 1rem;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">Movie Recommender System</div>', unsafe_allow_html=True)

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
st.markdown('<div class="label-text">Type or select a movie from the dropdown</div>', unsafe_allow_html=True)
selected_movie = st.selectbox("", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    st.markdown('<div class="recommendation-container">', unsafe_allow_html=True)
    for name, poster in zip(recommended_movie_names, recommended_movie_posters):
        st.markdown(
            f"""
            <div class="recommendation-item">
                <img src="{poster}" />
                <div>{name}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
