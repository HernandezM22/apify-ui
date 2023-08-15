import streamlit as st

title = st.columns(3)
with title[1]:
    st.image("resources/datlas.png", width=350)

with st.columns(3)[1]:
    st.header("Repositorio de APIs")

logos = st.columns(5, gap="large")

with logos[0]:
    st.image("resources/instagram.png",
            width=150)

with logos[1]:
    st.image("resources/twitter.png",
            width=150)

with logos[2]:
    st.image("resources/airbnb.png",
            width=150)

with logos[3]:
    st.image("resources/tripadvisor.png",
            width=150)

with logos[4]:
    st.image("resources/google.png",
            width=150)