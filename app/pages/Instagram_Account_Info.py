import streamlit as st
from core.settings import settings
import src.apify_functions as apify

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

client = apify.authenticate_apify(
    token=settings.APIFY_API_KEY
)

with st.columns(3, gap="large")[1]:
    st.image("resources/instagram.png",
            width=200)

st.title("Consultar estadísticas de perfiles de instagram")

profiles = st.text_input(label="Perfil o perfiles",
                        help="Separa con comas")

run_button = st.button("Extraer")

if run_button:

    run_input = {
    "usernames": profiles.split(",")
}
    progress_text = "Progreso: "
    my_bar = st.progress(0, text=progress_text)

    with st.spinner("Realizando query, espera un momento"):
        run = apify.query_instagram_info(client=client, run_input=run_input)

    my_bar.progress(100, text=progress_text)
    st.dataframe(run)

    csv = convert_df(run)

    st.download_button(
        label="Descargar como CSV",
        data=csv,
        file_name=f'instagram.csv',
        mime='text/csv',
    )
