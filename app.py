import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import gspread

# Configurazione della pagina
st.set_page_config(page_title="Valutazione Progetto: WHAT vs HOW", layout="wide", page_icon="📊")

st.title("📊 Valutazione Progetto: Matrice WHAT vs HOW")
st.write("Valuta il personale interno, inserisci note qualitative e salva i dati nel database Google Sheets.")

# CONFIGURAZIONE LINK / ID GOOGLE SHEETS
# Sostituisci con l'ID del tuo Google Sheet (la stringa tra /d/ e /edit nel link del foglio)
SPREADSHEET_ID = "INSERISCI_QUI_IL_TUO_ID_SHEET"

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
        gc = gspread.public_credentials()
        # Modalità pubblicazione CSV diretta da Google Sheets
        sheet_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv"
        df_existing = pd.read_csv(sheet_url)
        st.success(f"Connessione al foglio riuscita! Righe presenti: {len(df_existing)}")
    except Exception as e:
        st.info("Nota: Per abilitare la scrittura diretta su Google Sheets, configura le credenziali gspread oppure scarica la scheda CSV con il pulsante qui sotto.")

# ==================== DOWNLOAD DIRECT CSV / REPORT ====================
df_dettagli = pd.DataFrame([{
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

st.download_button(
    label="📥 Scarica Valutazione Singola (CSV)",
    data=df_dettagli.to_csv(index=False).encode('utf-8'),
    file_name=f"Valutazione_{nome.replace(' ', '_')}.csv",
    mime="text/csv"
)
