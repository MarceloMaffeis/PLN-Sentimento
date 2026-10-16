"""
Analisador de Sentimentos Offline
Licença: MIT License
"""

from typing import Tuple
import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator


# ==========================================
# Configuração Inicial da Página
# ==========================================
st.set_page_config(
    page_title="Analisador de Sentimentos (Offline)",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ==========================================
# Funções Utilitárias e de Processamento
# ==========================================
def translate_to_english(text: str) -> str:
    """
    Traduz de forma transparente o texto de entrada para o inglês
    utilizando a biblioteca deep-translator, permitindo que o TextBlob
    opere com máxima precisão.
    """
    try:
        # source='auto' detecta o idioma original automaticamente
        translated = GoogleTranslator(source="auto", target="en").translate(text)
        return translated if translated else text
    except Exception:
        # Fallback resiliente: caso ocorra timeout ou erro de rede, utiliza o texto original
        return text


def analyze_sentiment(polarity: float) -> Tuple[str, str, str]:
    """
    Classifica a polaridade do TextBlob em faixas de sentimento
    e define os parâmetros visuais de exibição.
    
    Retorna: (categoria, mensagem, tipo_componente)
    """
    # Limiares clássicos de polaridade (-1.0 a 1.0)
    if polarity > 0.1:
        return (
            "Positivo",
            f"Sentimento detectado: **Positivo** (Polaridade: {polarity:+.2f})",
            "success",
        )
    elif polarity < -0.1:
        return (
            "Negativo",
            f"Sentimento detectado: **Negativo** (Polaridade: {polarity:+.2f})",
            "error",
        )
    else:
        return (
            "Neutro",
            f"Sentimento detectado: **Neutro** (Polaridade: {polarity:+.2f})",
            "warning",
        )


# ==========================================
# Interface do Usuário (Streamlit)
# ==========================================
def main() -> None:
    st.title("🧠 Analisador de Sentimentos")
    st.caption(
        "Versão **Offline / Local** baseada em bibliotecas clássicas de NLP (TextBlob) "
        "sem dependência de APIs pagas de LLMs."
    )
    st.markdown("---")

    st.write(
        "Digite ou cole o texto abaixo (em português ou inglês). "
        "O algoritmo processará o léxico semântico para determinar a polaridade do sentimento."
    )

    user_input = st.text_area(
        label="Texto para análise:",
        placeholder="Ex: Este produto superou todas as minhas expectativas, adorei a experiência!",
        height=140,
    )

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        btn_analyze = st.button("Analisar", use_container_width=True, type="primary")

    if btn_analyze:
        if not user_input.strip():
            st.warning("⚠️ Por favor, insira algum texto antes de analisar.")
            return

        with st.spinner("Processando texto e calculando polaridade..."):
            # 1. Tradução intermediária silenciosa para garantir precisão com TextBlob
            english_text = translate_to_english(user_input.strip())

            # 2. Análise léxica com TextBlob
            blob = TextBlob(english_text)
            polarity_score = blob.sentiment.polarity
            subjectivity_score = blob.sentiment.subjectivity

            # 3. Classificação do resultado
            sentiment, message, alert_type = analyze_sentiment(polarity_score)

        # Exibição do feedback visual principal
        st.markdown("### Resultado da Avaliação")
        if alert_type == "success":
            st.success(f"😊 {message}")
        elif alert_type == "error":
            st.error(f"🙁 {message}")
        else:
            st.warning(f"😐 {message}")

        # Métricas complementares para transparência analítica
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Índice de Polaridade",
                value=f"{polarity_score:.2f}",
                help="-1.0 (muito negativo) a +1.0 (muito positivo)",
            )
        with col2:
            st.metric(
                label="Subjetividade",
                value=f"{subjectivity_score:.2f}",
                help="0.0 (muito objetivo/fato) a 1.0 (muito subjetivo/opinião)",
            )

    # Rodapé com informações de licenciamento
    st.markdown("---")
    st.markdown(
        "<small style='color: gray;'>Distribuído sob a Licença MIT. Projeto de código aberto.</small>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
