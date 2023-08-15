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
    st.image("resources/airbnb.png",
            width=200)

st.title("Consultar airbnbs por ciudad")

city_name = st.text_input(label="Nombre de la ciudad")
results = st.text_input(label="Cantidad de resultados",
                        help="Entre más grande, más tardará y más cuesta. Ten cuidado.")

currency = st.text_input(label="Tipo de cambio",
                        help="Introduce el código (ej: MXN, USD, EUR)")

run_button = st.button("Extraer")

if run_button:

    run_input = {
    "locationQuery": city_name,
    "maxListings": int(results),
    "includeReviews": True,
    "maxReviews": 10,
    "startUrls": [],
    "calendarMonths": 0,
    "currency": currency,
    "proxyConfiguration": { "useApifyProxy": True },
    "maxConcurrency": 50,
    "limitPoints": 100,
    "timeoutMs": 60000,
}

    progress_text = "Progreso: "
    my_bar = st.progress(0, text=progress_text)

    with st.spinner("Realizando query, espera un momento"):
        run = apify.query_airbnbs(client=client, run_input=run_input)

    my_bar.progress(100, text=progress_text)
    st.dataframe(run)

    csv = convert_df(run)

    st.download_button(
        label="Descargar como CSV",
        data=csv,
        file_name=f'airbnb_{city_name}.csv',
        mime='text/csv',
    )

