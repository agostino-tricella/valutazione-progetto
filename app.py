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

# MAPPA DEGLI ENTRY DEL FORM CON EMAIL INCLUSA
ENTRY_MAP = {
    "email": "entry.724133456",
    "data": "entry.756219816",
    "nome": "entry.673061402",
    "ruolo": "entry.1824122495",
    "valutatore": "entry.465627857",
    "media_what": "entry.483643984",
    "media_how": "entry.969822932",
    "x_pos": "entry.1057253397",
    "y_pos": "entry.814279471",
    "profilo": "entry.849542168",
    "dettagli": "entry.408649876",
    "commento": "entry.123456789"
}

# ==================== SIDEBAR: INPUT DATI ====================
st.sidebar.header("👤 Dati Dipendente e Valutatore")
email_valutatore = st.sidebar.text_input("Email Valutatore", "agostino.tricella@fontanagruppo.com")
nome = st.sidebar.text_input("Nome e Cognome Dipendente", "Mario Rossi")
ruolo = st.sidebar.text_input("Ruolo nel Progetto", "Developer / Analyst")
valutatore = st.sidebar.text_input("Valutatore (PM)", "Agostino Tricella")

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
    "Commenti e note sulla valutazione:",
    value="Punti di forza: ottima competenza tecnica e puntualità.\nAree di miglioramento: promuovere maggiore collaborazione durante le fasi critiche.",
    height=120
)

# ==================== CALCOLI ====================
media_what = round(float(np.mean([w1, w2, w3, w4, w5])), 2)
media_how = round(float(np.mean([h1, h2, h3, h4, h5])), 2)

x_pos = int(np.clip(round(media_what), 1, 5))
y_pos = int(np.clip(round(media_how), 1, 5))

# Mappa dei profili con terminologia HR Corporate
profili = {
    (5, 5): "Role Model", 
    (4, 5): "Top Performer", 
    (3, 5): "Talento Chiave", 
    (2, 5): "High Potential (HiPo)", 
    (1, 5): "Profilo in Sviluppo",
    
    (5, 4): "Top Performer", 
    (4, 4): "Future Leader", 
    (3, 4): "Core Performer", 
    (2, 4): "High Potential (HiPo)", 
    (1, 4): "Profilo in Sviluppo",
    
    (5, 3): "Pilastro Aziendale", 
    (4, 3): "Contributor Stabile", 
    (3, 3): "Core Performer", 
    (2, 3): "Emergente", 
    (1, 3): "Incarico sotto Standard",
    
    (5, 2): "Individual Contributor", 
    (4, 2): "Specialista Autonomo", 
    (3, 2): "Profilo da Allineare", 
    (2, 2): "Incarico sotto Standard", 
    (1, 2): "Action Plan (PIP)",
    
    (5, 1): "Individual Contributor", 
    (4, 1): "Specialista Autonomo", 
    (3, 1): "Rischio di Allineamento", 
    (2, 1): "Action Plan (PIP)", 
    (1, 1): "Action Plan (PIP)"
}

profilo_risultante = profili.get((x_pos, y_pos), "Non Definito")

# ==================== LAYOUT PRINCIPALE ====================
col1, col2, col3 = st.columns(3)
col1.metric("Punteggio Medio WHAT (X)", f"{media_what} / 5")
col2.metric("Punteggio Medio HOW (Y)", f"{media_how} / 5")
col3.metric("Profilo Mappato", profilo_risultante)

st.markdown("---")

# ==================== MATRICE GRAFICA INTERATTIVA (CON TERMINI HR) ====================
st.subheader("🗺️ Matrice Posizionamento 5x5")

x_labels = ['1 (Basso)', '2 (M. Basso)', '3 (Standard)', '4 (Alto)', '5 (Eccellente)']
y_labels = ['1 (Basso)', '2 (M. Basso)', '3 (Standard)', '4 (Alto)', '5 (Eccellente)']

grid_labels = [
    ["Action Plan (PIP)", "Action Plan (PIP)", "Rischio Allineamento", "Specialista Autonomo", "Individual Contributor"],
    ["Action Plan (PIP)", "Incarico sotto Standard", "Profilo da Allineare", "Specialista Autonomo", "Individual Contributor"],
    ["Incarico sotto Standard", "Emergente", "Core Performer", "Contributor Stabile", "Pilastro Aziendale"],
    ["Profilo in Sviluppo", "High Potential (HiPo)", "Core Performer", "Future Leader", "Top Performer"],
    ["Profilo in Sviluppo", "High Potential (HiPo)", "Talento Chiave", "Top Performer", "Role Model"]
]

color_values = [
    [0, 0, 1, 2, 2],
    [0, 1, 2, 2, 2],
    [1, 2, 3, 4, 5],
    [2, 3, 3, 5, 5],
    [2, 3, 4, 5, 6]
]

fig = go.Figure()

fig.add_trace(go.Heatmap(
    z=color_values,
    x=x_labels,
    y=y_labels,
    colorscale='RdYlGn',  # Sfumatura Rosso -> Giallo -> Verde
    showscale=False,
    hoverinfo='none'
))

for y_idx in range(5):
    for x_idx in range(5):
        fig.add_annotation(
            x=x_labels[x_idx],
            y=y_labels[y_idx],
            text=f"<b>{grid_labels[y_idx][x_idx]}</b>",
            showarrow=False,
            font=dict(size=11, color="black")
        )

# Indicatore dinamico in evidenza
fig.add_trace(go.Scatter(
    x=[x_labels[x_pos - 1]],
    y=[y_labels[y_pos - 1]],
    mode='markers+text',
    marker=dict(size=36, color='black', symbol='x-thin', line=dict(width=6, color='black')),
    text=[f"<b>📍 {nome}</b>"],
    textposition="top center",
    name="In Valutazione"
))

fig.update_layout(
    xaxis_title="<b>WHAT: Obiettivi Concreti (Asse X)</b>",
    yaxis_title="<b>HOW: Comportamenti / Soft Skills (Asse Y)</b>",
    height=530,
    margin=dict(l=40, r=40, t=40, b=40)
)

st.plotly_chart(fig, use_container_width=True, key=f"matrice_{x_pos}_{y_pos}")

st.markdown("---")
st.subheader("📝 Commenti e Note di Valutazione")
st.info(commento if commento.strip() else "Nessun commento inserito.")

st.markdown("---")

# ==================== COSTROZIONE URL PRECOMPILATO ====================
st.subheader("💾 Salvataggio nel Foglio Google")

data_ora = datetime.now().strftime("%Y-%m-%d %H:%M")
dettagli_voti = f"W:[{w1},{w2},{w3},{w4},{w5}] | H:[{h1},{h2},{h3},{h4},{h5}]"

params = {
    ENTRY_MAP["email"]: email_valutatore,
    ENTRY_MAP["data"]: data_ora,
    ENTRY_MAP["nome"]: nome,
    ENTRY_MAP["ruolo"]: ruolo,
    ENTRY_MAP["valutatore"]: valutatore,
    ENTRY_MAP["media_what"]: str(media_what),
    ENTRY_MAP["media_how"]: str(media_how),
    ENTRY_MAP["x_pos"]: str(x_pos),
    ENTRY_MAP["y_pos"]: str(y_pos),
    ENTRY_MAP["profilo"]: profilo_risultante,
    ENTRY_MAP["dettagli"]: dettagli_voti,
    ENTRY_MAP["commento"]: commento
}

url_precompilato = f"{FORM_BASE_URL}?{urllib.parse.urlencode(params)}"

st.markdown(
    f"""
    <a href="{url_precompilato}" target="_blank">
        <button style="
            background-color: #28A745;
            color: white;
            padding: 14px 28px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        ">
            🚀 Salva Valutazione nel Foglio Google (Precompilato)
        </button>
    </a>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ==================== DOWNLOAD DIRECT CSV ====================
df_dettagli = pd.DataFrame([{
    "Email": email_valutatore,
    "Data": data_ora,
    "Nome": nome,
    "Ruolo": ruolo,
    "Valutatore": valutatore,
    "Media_WHAT": media_what,
    "Media_HOW": media_how,
    "X_Pos": x_pos,
    "Y_Pos": y_pos,
    "Profilo": profilo_risultante,
    "Dettagli_Voti": dettagli_voti,
    "Commento": commento
}])

st.download_button(
    label="📥 Scarica Scheda Singola in CSV",
    data=df_dettagli.to_csv(index=False).encode('utf-8'),
    file_name=f"Valutazione_{nome.replace(' ', '_')}.csv",
    mime="text/csv"
)
