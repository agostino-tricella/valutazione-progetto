import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import urllib.parse

# Configurazione della pagina
st.set_page_config(page_title="Valutazione Progetto: WHAT vs HOW", layout="wide", page_icon="📊")

st.title("📊 Valutazione Progetto: Matrice WHAT vs HOW")
st.write("Valuta il personale interno, inserisci note qualitative e salva i dati direttamente su Google Sheets.")

# LINK BASE DEL GOOGLE FORM
FORM_BASE_URL = "https://docs.google.com/forms/d/e/1FAIpQLSecva6sLSBuaDDhVADMTtjXlVmScPCOg5ffi8hESsKU7yjNqg/viewform"

# MAPPA DELLE 11 ENTRY ESTRATTE DAL FORM
ENTRY_MAP = {
    "data": "entry.724133456",
    "nome": "entry.756219816",
    "ruolo": "entry.673061402",
    "valutatore": "entry.1824122495",
    "media_what": "entry.465627857",
    "media_how": "entry.483643984",
    "x_pos": "entry.969822932",
    "y_pos": "entry.1057253397",
    "profilo": "entry.814279471",
    "dettagli": "entry.849542168",
    "commento": "entry.408649876"
}

# ==================== SIDEBAR: INPUT DATI ====================
st.sidebar.header("👤 Dati Dipendente")
nome = st.sidebar.text_input("Nome e Cognome", "Mario Rossi")
ruolo = st.sidebar.text_input("Ruolo nel Progetto", "Developer / Analyst")
valutatore = st.sidebar.text_input("Valutatore (PM)", "Giuseppe Bianchi")

st.sidebar.markdown("---")
st.sidebar.header("🎯 1. OBIETTIVI DI PROGETTO (WHAT)")
w1 = st.sidebar.slider("1. Erogazione BBP (Tempi)", 1, 5, 3, key="w1")
w2 = st.sidebar.slider("2. Completamento UAT (Qualità)", 1, 5, 3, key="w2")
w3 = st.sidebar.slider("3. Rispetto Stime/Budget", 1, 5, 3, key="w3")
w4 = st.sidebar.slider("4. Qualità Deliverable (No Rework)", 1, 5, 3, key="w4")
w5 = st.sidebar.slider("5. Documentazione e Handover", 1, 5, 3, key="w5")

st.sidebar.markdown("---")
st.sidebar.header("🤝 2. SOFT SKILLS (HOW)")
h1 = st.sidebar.slider("1. Lavoro in Team e Proattività", 1, 5, 3, key="h1")
h2 = st.sidebar.slider("2. Problem Solving e Iniziativa", 1, 5, 3, key="h2")
h3 = st.sidebar.slider("3. Comunicazione ed Escalation", 1, 5, 3, key="h3")
h4 = st.sidebar.slider("4. Adattabilità e Gestione Stress", 1, 5, 3, key="h4")
h5 = st.sidebar.slider("5. Ownership e Affidabilità", 1, 5, 3, key="h5")

st.sidebar.markdown("---")
st.sidebar.header("💬 3. COMMENTO QUALITATIVO")
commento = st.sidebar.text_area(
    "Commento e note sulla valutazione:",
    value="Punti di forza: ottima competenza tecnica e puntualità.\nAree di miglioramento: promuovere maggiore collaborazione durante le fasi critiche.",
    height=120
)

# ==================== CALCOLI ====================
media_what = round(float(np.mean([w1, w2, w3, w4, w5])), 2)
media_how = round(float(np.mean([h1, h2, h3, h4, h5])), 2)

x_pos = int(np.clip(round(media_what), 1, 5))
y_pos = int(np.clip(round(media_how), 1, 5))

profili = {
    (5, 5): "Role Model", (4, 5): "Top Performer", (3, 5): "Core Player Solido", (2, 5): "Volenteroso / Inefficace", (1, 5): "Volenteroso / Inefficace",
    (5, 4): "Top Performer", (4, 4): "Top Performer", (3, 4): "Core Player Solido", (2, 4): "Volenteroso / Inefficace", (1, 4): "Volenteroso / Inefficace",
    (5, 3): "Core Player Solido", (4, 3): "Core Player Solido", (3, 3): "Core Player", (2, 3): "Da Sviluppare", (1, 3): "Underperformer",
    (5, 2): "Lupo Solitario", (4, 2): "Mercenario (Rischio)", (3, 2): "Mercenario (Rischio)", (2, 2): "Underperformer", (1, 2): "Underperformer",
    (5, 1): "Lupo Solitario (Tossico)", (4, 1): "Lupo Solitario", (3, 1): "Mercenario (Rischio)", (2, 1): "Underperformer", (1, 1): "Azione Immediata (PIP)"
}

profilo_risultante = profili.get((x_pos, y_pos), "Non Definito")

# ==================== LAYOUT PRINCIPALE ====================
col1, col2, col3 = st.columns(3)
col1.metric("Punteggio Medio WHAT (X)", f"{media_what} / 5")
col2.metric("Punteggio Medio HOW (Y)", f"{media_how} / 5")
col3.metric("Profilo Mappato", profilo_risultante)

st.markdown("---")

# ==================== MATRICE GRAFICA INTERATTIVA ====================
st.subheader("🗺️ Matrice Posizionamento 5x5")

x_labels = ['1 (Basso)', '2 (M. Basso)', '3 (Standard)', '4 (Alto)', '5 (Eccellente)']
y_labels = ['1 (Basso)', '2 (M. Basso)', '3 (Standard)', '4 (Alto)', '5 (Eccellente)']

grid_labels = [
    ["Azione PIP", "Underperformer", "Mercenario", "Lupo Solitario", "Lupo Tossico"],
    ["Underperformer", "Underperformer", "Mercenario", "Mercenario", "Lupo Solitario"],
    ["Underperformer", "Da Sviluppare", "Core Player", "Core Solido", "Core Solido"],
    ["Volenteroso", "Volenteroso", "Core Solido", "Top Performer", "Top Performer"],
