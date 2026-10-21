import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configurazione della pagina
st.set_page_config(page_title="Valutazione Progetto: WHAT vs HOW", layout="wide")

st.title("📊 Valutazione Progetto: Matrice WHAT vs HOW")
st.write("Valuta il personale interno bilanciando gli obiettivi raggiunti (WHAT) e i comportamenti organizzativi (HOW).")

# ==================== SIDEBAR: INPUT DATI ====================
st.sidebar.header("👤 Dati Dipendente")
nome = st.sidebar.text_input("Nome e Cognome", "Mario Rossi")
ruolo = st.sidebar.text_input("Ruolo nel Progetto", "Developer / Analyst")
valutatore = st.sidebar.text_input("Valutatore (PM)", "Giuseppe Bianchi")

st.sidebar.markdown("---")
st.sidebar.header("🎯 1. OBIETTIVI DI PROGETTO (WHAT)")
w1 = st.sidebar.slider("1. Erogazione BBP (Tempi)", 1, 5, 3)
w2 = st.sidebar.slider("2. Completamento UAT (Qualità)", 1, 5, 3)
w3 = st.sidebar.slider("3. Rispetto Stime/Budget", 1, 5, 3)
w4 = st.sidebar.slider("4. Qualità Deliverable (No Rework)", 1, 5, 3)
w5 = st.sidebar.slider("5. Documentazione e Handover", 1, 5, 3)

st.sidebar.markdown("---")
st.sidebar.header("🤝 2. SOFT SKILLS (HOW)")
h1 = st.sidebar.slider("1. Lavoro in Team e Proattività", 1, 5, 3)
h2 = st.sidebar.slider("2. Problem Solving e Iniziativa", 1, 5, 3)
h3 = st.sidebar.slider("3. Comunicazione ed Escalation", 1, 5, 3)
h4 = st.sidebar.slider("4. Adattabilità e Gestione Stress", 1, 5, 3)
h5 = st.sidebar.slider("5. Ownership e Affidabilità", 1, 5, 3)

# ==================== CALCOLI ====================
media_what = round(np.mean([w1, w2, w3, w4, w5]), 2)
media_how = round(np.mean([h1, h2, h3, h4, h5]), 2)

# Arrotondamento per posizionamento sulla matrice 5x5 (1 to 5)
x_pos = int(np.clip(round(media_what), 1, 5))
y_pos = int(np.clip(round(media_how), 1, 5))

# Mappa delle etichette dei ruoli
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

# ==================== MATRICE GRAFICA INTERATTIVA (PLOTLY) ====================
st.subheader("🗺️ Matrice Posizionamento 5x5")

# Testi delle caselle
grid_labels = [
    ["Volenteroso", "Volenteroso", "Core Solido", "Top Performer", "Role Model"],
    ["Volenteroso", "Volenteroso", "Core Solido", "Top Performer", "Top Performer"],
    ["Underperformer", "Da Sviluppare", "Core Player", "Core Solido", "Core Solido"],
    ["Underperformer", "Underperformer", "Mercenario", "Mercenario", "Lupo Solitario"],
    ["Azione PIP", "Underperformer", "Mercenario", "Lupo Solitario", "Lupo Tossico"]
]

# Matrice dei colori di sfondo
color_values = [
    [2, 2, 4, 5, 6],
    [2, 2, 4, 5, 5],
    [1, 2, 3, 4, 4],
    [1, 1, 2, 2, 2],
    [0, 1, 2, 2, 1]
]

fig = go.Figure()

# Heatmap di sfondo
fig.add_trace(go.Heatmap(
    z=color_values[::-1],
    x=['1 (Basso)', '2 (M. Basso)', '3 (Standard)', '4 (Alto)', '5 (Eccellente)'],
    y=['1 (Basso)', '2 (M. Basso)', '3 (Standard)', '4 (Alto)', '5 (Eccellente)'],
    colorscale='YlGnBu',
    showscale=False,
    hoverinfo='none'
))

# Testi dentro le caselle
for y_idx, row in enumerate(grid_labels[::-1]):
    for x_idx, label in enumerate(row):
        fig.add_annotation(
            x=x_idx, y=y_idx,
            text=label,
            showarrow=False,
            font=dict(size=12, color="black")
        )

# Indicatore / Punto evidenziato per il dipendente valutato
fig.add_trace(go.Scatter(
    x=[x_pos - 1],
    y=[y_pos - 1],
    mode='markers+text',
    marker=dict(size=30, color='red', symbol='cross-thin', line=dict(width=4, color='red')),
    text=[f"<b>{nome}</b>"],
    textposition="top center",
    name="Posizione Dipendente"
))

fig.update_layout(
    xaxis_title="<b>WHAT: Obiettivi Concreti (Asse X)</b>",
    yaxis_title="<b>HOW: Comportamenti / Soft Skills (Asse Y)</b>",
    height=550,
    margin=dict(l=40, r=40, t=40, b=40)
)

st.plotly_chart(fig, use_container_width=True)
