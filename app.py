import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Configurazione della pagina
st.set_page_config(page_title="Valutazione Progetto: WHAT vs HOW", layout="wide", page_icon="📊")

st.title("📊 Valutazione Progetto: Matrice WHAT vs HOW")
st.write("Valuta il personale interno, inserisci note qualitative e salva i dati nel database Google Sheets.")

# CONFIGURAZIONE LINK GOOGLE SHEETS (Sostituisci con il tuo link)
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1_EqrPXiizq8ZAABNk1Q03zTedrz5VJPduvWKYsU8m14/edit?usp=sharing"

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
    ["Volenteroso", "Volenteroso", "Core Solido", "Top Performer", "Role Model"]
]

color_values = [
    [0, 1, 2, 2, 1],
    [1, 1, 2, 2, 2],
    [1, 2, 3, 4, 4],
    [2, 2, 4, 5, 5],
    [2, 2, 4, 5, 6]
]

fig = go.Figure()

fig.add_trace(go.Heatmap(
    z=color_values,
    x=x_labels,
    y=y_labels,
    colorscale='YlGnBu',
    showscale=False,
    hoverinfo='none'
))

for y_idx in range(5):
    for x_idx in range(5):
        fig.add_annotation(
            x=x_labels[x_idx],
            y=y_labels[y_idx],
            text=grid_labels[y_idx][x_idx],
            showarrow=False,
            font=dict(size=12, color="black")
        )

# Indicatore dinamico
fig.add_trace(go.Scatter(
    x=[x_labels[x_pos - 1]],
    y=[y_labels[y_pos - 1]],
    mode='markers+text',
    marker=dict(size=32, color='red', symbol='x-thin', line=dict(width=5, color='red')),
    text=[f"<b>📍 {nome}</b>"],
    textposition="top center",
    name="In Valutazione"
))

fig.update_layout(
    xaxis_title="<b>WHAT: Obiettivi Concreti (Asse X)</b>",
    yaxis_title="<b>HOW: Comportamenti / Soft Skills (Asse Y)</b>",
    height=500,
    margin=dict(l=40, r=40, t=40, b=40)
)

st.plotly_chart(fig, use_container_width=True, key=f"matrice_{x_pos}_{y_pos}")

# ==================== MOSTRA COMMENTO SULLA SCHEDA ====================
st.markdown("---")
st.subheader("📝 Commento e Note di Valutazione")
st.info(commento if commento.strip() else "Nessun commento inserito.")

st.markdown("---")

# ==================== SALVATAGGIO GOOGLE SHEETS ====================
st.subheader("💾 Salvataggio nel Database (Google Sheets)")

if st.button("💾 Salva Valutazione in Google Sheets", type="primary"):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        df_existing = conn.read(spreadsheet=GOOGLE_SHEET_URL, ttl="0")
        
        nuova_riga = pd.DataFrame([{
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Nome": nome,
            "Ruolo": ruolo,
            "Valutatore": valutatore,
            "Media_WHAT": media_what,
            "Media_HOW": media_how,
            "X_Pos": x_pos,
            "Y_Pos": y_pos,
            "Profilo": profilo_risultante,
            "Dettagli_Voti": f"W:[{w1},{w2},{w3},{w4},{w5}] | H:[{h1},{h2},{h3},{h4},{h5}]",
            "Commento": commento
        }])
        
        df_updated = pd.concat([df_existing, nuova_riga], ignore_index=True)
        conn.update(spreadsheet=GOOGLE_SHEET_URL, data=df_updated)
        
        st.success(f"✅ Valutazione e commento di **{nome}** salvati con successo!")
    except Exception as e:
        st.error(f"Errore durante il salvataggio: {e}. Verificare le impostazioni di condivisione del foglio.")

# ==================== STORICO TEAM ====================
st.markdown("---")
st.subheader("📋 Storico Team Valutato")

if st.button("🔄 Aggiorna / Mostra Tabella Team"):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_team = conn.read(spreadsheet=GOOGLE_SHEET_URL, ttl="0")
        st.dataframe(df_team, use_container_width=True)
    except Exception as e:
        st.info("Clicca sul pulsante per caricare lo storico dal Google Sheet.")
