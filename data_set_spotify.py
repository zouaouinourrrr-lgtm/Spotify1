# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# 1. Page setup
st.set_page_config(page_title="Spotify Clone", layout="wide", page_icon="🎵")

# 2. Custom CSS for the Spotify "Dark Mode" look
st.markdown("""
    <style>
    .main { background-color: #121212; color: white; }
    .stButton>button { 
        background-color: #1DB954; 
        color: white; 
        border-radius: 20px; 
        border: none;
        padding: 5px 20px;
    }
    .stButton>button:hover {
        background-color: #1ed760;
        color: white;
    }
    div[data-testid="stExpander"] { background-color: #282828; }
    </style>
    """, unsafe_allow_html=True)

# 3. Data Loading
@st.cache_data
def load_data():
    # Make sure this filename matches exactly what is on GitHub
    df = pd.read_csv("spotify_songs_dataset.csv")
    df['duration'] = df['duration'].fillna(0)
    df['release_date'] = pd.to_datetime(df['release_date'])
    return df

try:
    df = load_data()

    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("🎵 Spotify Clone")
    menu = st.sidebar.radio("Menu", ["Home", "Search", "Top Charts"])

    # --- HOME PAGE ---
    if menu == "Home":
        st.title("Good Evening")
        st.subheader("Made for You")
        
        cols = st.columns(4)
        random_songs = df.sample(4)
        for i, (idx, row) in enumerate(random_songs.iterrows()):
            with cols[i]:
                # Using a slightly nicer placeholder for album art
                st.image("https://via.placeholder.com/200/282828/FFFFFF?text=Music", use_container_width=True)
                st.write(f"**{row['song_title']}**")
                st.caption(f"{row['artist']}")

    # --- SEARCH PAGE ---
    elif menu == "Search":
        st.title("Search")
        search_query = st.text_input("What do you want to listen to?", placeholder="Artists, songs, or genres")
        
        if search_query:
            results = df[
                df['song_title'].str.contains(search_query, case=False, na=False) |
                df['artist'].str.contains(search_query, case=False, na=False) |
                df['genre'].str.contains(search_query, case=False, na=False)
            ]
            st.write(f"Found {len(results)} matches:")
            st.dataframe(results[['song_title', 'artist', 'genre', 'popularity', 'release_date']], use_container_width=True)

    # --- TOP CHARTS ---
    elif menu == "Top Charts":
        st.title("Trending Songs")
        trending = df.sort_values(by='popularity', ascending=False).head(10)
        
        for i, (idx, row) in enumerate(trending.iterrows()):
            col1, col2, col3 = st.columns([0.5, 4, 1])
            with col1:
                st.write(f"**{i+1}**")
            with col2:
                st.write(f"**{row['song_title']}**")
                st.caption(f"{row['artist']} • {row['genre']}")
            with col3:
                if st.button("Play", key=f"play_{idx}"):
                    st.toast(f"Playing {row['song_title']}...")

    # --- PLAYER BAR (Sticky Footer) ---
    st.markdown("---")
    f1, f2, f3 = st.columns([1, 2, 1])
    with f2:
        st.write("<div style='text-align: center'>⏮️ &nbsp;&nbsp; ▶️ &nbsp;&nbsp; ⏭️</div>", unsafe_allow_html=True)
        st.progress(30)

except Exception as e:
    st.error(f"Could not load the dataset. Check if 'spotify_songs_dataset.csv' is uploaded to GitHub. Error: {e}")