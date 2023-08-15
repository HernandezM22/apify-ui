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
    st.image("resources/google.png",
            width=200)

st.title("Consultar resultados de google para busqueda")

search_term = st.text_input(label="Palabra o frase")
country_code = st.text_input(label="Código de país",
                            help="Ej. US, MX, FR, etc")

language_code = st.text_input(label="Código de idioma",
                            help="Ej. EN, ES")

max_pages = st.text_input(label="Número de páginas a revisar")
results_per_page = st.text_input(label="Número de resultados por página")

run_button = st.button("Extraer")

if run_button:

    run_input = {
    "countryCode": country_code,
    "includeUnfilteredResults": False,
    "languageCode": language_code,
    "maxPagesPerQuery": int(max_pages),
    "mobileResults": False,
    "queries": search_term,
    "resultsPerPage": int(results_per_page),
    "saveHtml": False,
    "saveHtmlToKeyValueStore": False,
    "maxConcurrency": 10
    }

    progress_text = "Progreso: "
    my_bar = st.progress(0, text=progress_text)

    with st.spinner("Realizando query, espera un momento"):
        run = apify.query_google_results(client=client, run_input=run_input)

    my_bar.progress(100, text=progress_text)
    st.dataframe(run)

    csv = convert_df(run)

    st.download_button(
        label="Descargar como CSV",
        data=csv,
        file_name=f'results_{search_term}.csv',
        mime='text/csv',
    )
