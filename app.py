import streamlit as st
import pickle
import requests

def main():
    movies_df = pickle.load(open('movies.pkl', 'rb'))
    movies_title_df = movies_df['title'].values
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    def fetchPoster(movie_id):
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9433c57c72dadd3334e4b7e1a715de04&language=en-US'.format(movie_id))
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

    def RecommendMovies(movie):
        # Fetch index of movie in the dataframe
        movie_index = movies_df[movies_df['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []

        for i in movies_list:
            movie_id = movies_df.iloc[i[0]].movie_id
            recommended_movies.append(movies_df.iloc[i[0]].title)
            recommended_movies_posters.append(fetchPoster(movie_id))

        return recommended_movies, recommended_movies_posters

    st.title("Movie Recommender System")
    selcted_movie_name = st.selectbox("Which movie do you want to Recommend", movies_title_df)

    if st.button('Recommend'):
        movie_name, movie_poster = RecommendMovies(selcted_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(movie_poster[0])
            st.header(movie_name[0])
        with col2:
            st.image(movie_poster[1])
            st.header(movie_name[1])
        with col3:
            st.image(movie_poster[2])
            st.header(movie_name[2])
        with col4:
            st.image(movie_poster[3])
            st.header(movie_name[3])
        with col5:
            st.image(movie_poster[4])
            st.header(movie_name[4])

if __name__ == "__main__":
    main()
