import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Configurazione della pagina
st.set_page_config(page_title="Valutazione Progetto: WHAT vs HOW", layout="wide", page_icon="📊")

st.title("📊 Valutazione Progetto: Matrice WHAT vs HOW")
st.write("Valuta il personale interno bilanciando gli obiettivi raggiunti (WHAT) e i comportamenti organizzativi (HOW).")

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

# ==================== CALCOLI ====================
media_what = round(float(np.mean([w1, w2, w3, w4, w5])), 2)
media_how = round(float(np.mean([h1, h2, h3, h4, h5])), 2)

# Arrotondamento per posizionamento sulla matrice 5x5 (da 1 a 5)
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

# Heatmap di sfondo
fig.add_trace(go.Heatmap(
    z=color_values,
    x=x_labels,
    y=y_labels,
    colorscale='YlGnBu',
    showscale=False,
    hoverinfo='none'
))

# Testi dentro le caselle
for y_idx in range(5):
    for x_idx in range(5):
        fig.add_annotation(
            x=x_labels[x_idx],
            y=y_labels[y_idx],
            text=grid_labels[y_idx][x_idx],
            showarrow=False,
            font=dict(size=12, color="black")
        )

# Indicatore / Punto dinamico per il dipendente
fig.add_trace(go.Scatter(
    x=[x_labels[x_pos - 1]],
    y=[y_labels[y_pos - 1]],
    mode='markers+text',
    marker=dict(size=32, color='red', symbol='x-thin', line=dict(width=5, color='red')),
    text=[f"<b>📍 {nome}</b>"],
    textposition="top center",
    name="Posizione Dipendente"
))

fig.update_layout(
    xaxis_title="<b>WHAT: Obiettivi Concreti (Asse X)</b>",
    yaxis_title="<b>HOW: Comportamenti / Soft Skills (Asse Y)</b>",
    height=550,
    margin=dict(l=40, r=40, t=40, b=40)
)

st.plotly_chart(fig, use_container_width=True, key=f"matrice_{x_pos}_{y_pos}")

st.markdown("---")

# ==================== ESPORTAZIONE DATI ====================
st.subheader("📥 Esportazione Valutazione")

# Creazione DataFrame dei dettagli
df_dettagli = pd.DataFrame({
    "Categoria": ["Dati", "Dati", "Dati", " WHAT", "WHAT", "WHAT", "WHAT", "WHAT", "HOW", "HOW", "HOW", "HOW", "HOW", "Sintesi", "Sintesi", "Sintesi"],
    "Parametro / Voce": [
        "Nome Dipendente", "Ruolo", "Valutatore",
        "1. Erogazione BBP", "2. Completamento UAT", "3. Rispetto Stime/Budget", "4. Qualità Deliverable", "5. Documentazione e Handover",
        "1. Lavoro in Team", "2. Problem Solving", "3. Comunicazione", "4. Adattabilità", "5. Ownership",
        "Media WHAT (Asse X)", "Media HOW (Asse Y)", "Profilo Risultante"
    ],
    "Valore / Punteggio": [
        nome, ruolo, valutatore,
        w1, w2, w3, w4, w5,
        h1, h2, h3, h4, h5,
        media_what, media_how, profilo_risultante
    ]
})

col_exp1, col_exp2 = st.columns(2)

# Download CSV / Excel
csv_data = df_dettagli.to_csv(index=False).encode('utf-8')
col_exp1.download_button(
    label="📄 Scarica Scheda Valutazione (CSV / Excel)",
    data=csv_data,
    file_name=f"Valutazione_{nome.replace(' ', '_')}.csv",
    mime="text/csv"
)

# Stampa / Salva in PDF
html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        h2 {{ color: #2C3E50; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .highlight {{ font-weight: bold; color: #2980B9; }}
    </style>
</head>
<body>
    <h2>Scheda Valutazione Progetto: WHAT vs HOW</h2>
    <p><b>Dipendente:</b> {nome} | <b>Ruolo:</b> {ruolo} | <b>Valutatore:</b> {valutatore}</p>
    <hr>
    <h3>Risultati Sintetici</h3>
    <p class="highlight">Punteggio Medio WHAT (X): {media_what} / 5</p>
    <p class="highlight">Punteggio Medio HOW (Y): {media_how} / 5</p>
    <p class="highlight">Profilo Assegnato: {profilo_risultante}</p>
    <hr>
    <h3>Dettaglio Valutazioni</h3>
    <table>
        <tr><th>Categoria</th><th>Voce</th><th>Punteggio</th></tr>
        {"".join([f"<tr><td>{r['Categoria']}</td><td>{r['Parametro / Voce']}</td><td>{r['Valore / Punteggio']}</td></tr>" for _, r in df_dettagli.iterrows()])}
    </table>
</body>
</html>
"""

col_exp2.download_button(
    label="🖨️ Scarica Report per Stampa / PDF",
    data=html_report,
    file_name=f"Report_{nome.replace(' ', '_')}.html",
    mime="text/html"
)
