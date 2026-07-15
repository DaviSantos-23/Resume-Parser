import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from src.parser import PDFParser
from src.extractor import ResumeExtractor
from src.exporter import CSVExporter


# ==========================
# Configuração da página
# ==========================
st.set_page_config(
    page_title="Resume Data Extractor",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Data Extractor")

st.write(
    "Extraia automaticamente informações de currículos em PDF."
)


# ==========================
# Upload dos arquivos
# ==========================
pdfs = st.file_uploader(
    "Selecione um ou mais currículos",
    type=["pdf"],
    accept_multiple_files=True
)


# ==========================
# Processamento
# ==========================
if pdfs:

    registros = []

    for pdf in pdfs:

        texto = PDFParser.extract_text(pdf)

        dados = ResumeExtractor.extract_all(texto)

        dados["arquivo"] = pdf.name

        registros.append(dados)

    df = pd.DataFrame(registros)

    # ==========================
    # Quantidade de Skills
    # ==========================
    df["total_skills"] = df["skills"].apply(
        lambda x: len(x.split(", ")) if x else 0
    )

    # ==========================
    # Ordenação
    # ==========================
    df = df.sort_values(
        by="total_skills",
        ascending=False
    )

    completos = len(
    df[df["status"] == "🟢 Completo"]
    )

    parciais = len(
    df[df["status"] == "🟡 Parcial"]
    )

    insuficientes = len(
    df[df["status"] == "🔴 Insuficiente"]
    )

    # ==========================
    # Métricas
    # ==========================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📄 Currículos",
        len(df)
    )

    col2.metric(
        "🟢 Completos",
        completos
    )

    col3.metric(
        "🟡 Parciais",
        parciais
    )

    col4.metric(
        "🔴 Insuficientes",
        insuficientes
    )

    # ==========================
    # Tabela
    # ==========================
    st.subheader("📊 Resultados")

    st.dataframe(
        df,
        use_container_width=True
    )

    # ==========================
    # Exportação CSV
    # ==========================
    arquivo_csv = CSVExporter.export(df)

    with open(arquivo_csv, "rb") as file:

        st.download_button(
            label="⬇ Exportar CSV",
            data=file,
            file_name="curriculos_extraidos.csv",
            mime="text/csv"
        )

    st.success(
        f"✅ {len(df)} currículo(s) processado(s) com sucesso!"
    )