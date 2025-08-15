import streamlit as st
import pandas as pd
import pickle

# Load Data
music_list = pickle.load(open("music.pkl","rb"))
music = pd.DataFrame(music_list)
similarity = pickle.load(open('similarity.pkl','rb'))



def recommend_by_music(music_title):
    index = music[music["Music_Name"] == music_title].index[0]
    distances = similarity[index]
    similar_music = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:25]

    recommendations = []
    for i in similar_music:
        song_name = music.iloc[i[0]].Music_Name
        song_url = music.iloc[i[0]].Youtube_url   # Make sure column name matches your DataFrame
        recommendations.append((song_name, song_url))

    return recommendations



# st.title('Music Streamlit App')
#
# selected_music = st.selectbox("Pick one",music_list)





# if st.button("🎯 Recommend Similar music"):
#     with st.spinner("🔍 Finding similar music..."):
#         results = recommend_by_music(selected_music)
#         st.subheader(f"🎞️ Music similar to: {selected_music}")
#         for song, link in results:
#             st.markdown(f"[{song}]({link})")  # Clickable link
#





# if st.button("🎯 Recommend Similar music"):
#     with st.spinner("🔍 Finding similar music..."):
#         results = recommend_by_music(selected_music)
#         st.subheader(f"🎞️ Music similar to: {selected_music}")
#         for song, link in results:
#             with st.expander(song):  # collapsible title
#                 st.video(link)


# if st.button("🎯 Recommend Similar music"):
#     with st.spinner("🔍 Finding similar music..."):
#
#         # Show the selected song first
#         st.subheader(f"🎵 You selected: {selected_music}")
#         selected_url = music.loc[music["Music_Name"] == selected_music, "Youtube_url"].values[0]
#         st.video(selected_url)
#
#         # Now show recommendations
#         results = recommend_by_music(selected_music)
#         st.subheader(f"🎞️ Music similar to: {selected_music}")
#         for song, link in results:
#             with st.expander(song):  # collapsible title
#                 st.video(link)
#


# Function to embed YouTube without logo/suggestions
def embed_youtube(url, autoplay=0):
    video_id = url.split("v=")[-1]
    embed_url = f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1&autoplay={autoplay}"
    st.markdown(
        f'<iframe width="100%" height="400" src="{embed_url}" frameborder="0" '
        'allow="autoplay; encrypted-media" allowfullscreen></iframe>',
        unsafe_allow_html=True
    )

# Set up app
st.set_page_config(layout="wide")
st.title("🎵 Music Streamlit App")

# Store state
if "current_video" not in st.session_state:
    st.session_state.current_video = None
if "playlist" not in st.session_state:
    st.session_state.playlist = []

selected_music = st.selectbox("Music",music_list)

# Recommend button
if st.button("🎯 Recommend Similar music"):
    recs = recommend_by_music(selected_music)
    selected_url = music.loc[music["Music_Name"] == selected_music, "Youtube_url"].values[0]
    st.session_state.current_video = (selected_music, selected_url)
    st.session_state.playlist = recs

# Layout
col_left, col_right = st.columns([3, 1.5])

# Left: Player
with col_left:
    if st.session_state.current_video:
        title, url = st.session_state.current_video
        embed_youtube(url, autoplay=1)
        st.subheader(title)

# # Right: Recommendations
# with col_right:
#     if st.session_state.playlist:
#         st.subheader("Recommended Music")
#         for idx, (song, link) in enumerate(st.session_state.playlist):
#             if st.button(song, key=f"rec_btn_{idx}"):
#                 st.session_state.current_video = (song, link)
#                 st.rerun()


# Right: Recommendations
with col_right:
    if st.session_state.playlist:
        st.subheader("Recommended Music")
        for idx, (song, link) in enumerate(st.session_state.playlist):
            video_id = link.split("v=")[-1]
            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/default.jpg"

            # Black box with thumbnail and button inside
            st.markdown(
                f"""
                <div style="
                    border: 2px solid black;
                    border-radius: 8px;
                    padding: 8px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-bottom: 8px;
                ">
                    <img src="{thumbnail_url}" height="80" width="80" style="border-radius: 4px;">
                </div>
                """,
                unsafe_allow_html=True
            )

            # Streamlit button trigger
            if st.button(song, key=f"rec_btn_{idx}"):
                st.session_state.current_video = (song, link)
                st.rerun()
