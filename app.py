import streamlit as st
import random
import time

# --- CONFIGURATIE ---
# Verander dit getal (de seed) om een compleet nieuwe trekking te genereren.
# Zolang dit getal hetzelfde blijft, is de uitslag voor iedereen gelijk.
TREKKING_SEED = 123456789 

# --- Constante Data ---
DEELNEMERS = ["Lex", "Sanne", "Sterre", "Dave", "Linde", "Nathan", "Jan", "Esther"]

CATEGORIEEN = {
    "Useless Hero": "Zoek het meest nutteloze product dat toch een goede review heeft.",
    "Life-changer": "Zoek een product dat zogenaamd je leven verandert.",
    "Copycat": "Koop iets dat duidelijk een namaakversie is van iets bekends.",
    "Temu Fashion": "Koop iets wat zogenaamd fashion is, maar je kan er beter niet in gezien worden."
}

# --- De 'Backend' Logica ---

@st.cache_data
def genereer_globale_trekking(seed_waarde):
    """
    Genereert de trekking op basis van een vaste seed.
    Hierdoor ligt de uitslag vast voor iedereen die de app bezoekt.
    """
    # We gebruiken een specifieke random generator met de gekozen seed
    rng = random.Random(seed_waarde)
    
    # 1. Maak de pool van taken (2x elke categorie)
    taken_pool = []
    for naam, omschrijving in CATEGORIEEN.items():
        taken_pool.append((naam, omschrijving))
        taken_pool.append((naam, omschrijving))
    
    # 2. Schud de taken deterministisch
    rng.shuffle(taken_pool)
    
    # Deelnemerslijst sorteren voor consistentie
    deelnemers_sorted = sorted(DEELNEMERS)
    
    # 3. Koppel ze aan elkaar
    toewijzingen = {}
    for i, deelnemer in enumerate(deelnemers_sorted):
        cat_naam, cat_desc = taken_pool[i]
        toewijzingen[deelnemer] = {
            "Categorie": cat_naam,
            "Opdracht": cat_desc
        }
        
    return toewijzingen

# --- Streamlit UI ---

st.set_page_config(page_title="Lootjestrekking", layout="centered", page_icon="🎁")

# Haal de vaste trekking op
uitkomst_dict = genereer_globale_trekking(TREKKING_SEED)

# Initialiseer sessie status voor 'inloggen'
if 'huidige_gebruiker' not in st.session_state:
    st.session_state.huidige_gebruiker = None
if 'toon_resultaat' not in st.session_state:
    st.session_state.toon_resultaat = False

# --- SCHERM 1: INLOGGEN ---
if st.session_state.huidige_gebruiker is None:
    st.title("🎁 Secret Lootjestrekking")
    st.markdown("Welkom bij de Temu Challenge! Selecteer je naam om te zien wie jij hebt getrokken.")
    st.markdown("---")
    
    geselecteerde_naam = st.selectbox(
        "Wie ben jij?",
        ["Kies je naam..."] + sorted(DEELNEMERS)
    )
    
    if st.button("Ga verder →", type="primary"):
        if geselecteerde_naam != "Kies je naam...":
            st.session_state.huidige_gebruiker = geselecteerde_naam
            st.rerun()
        else:
            st.error("Kies eerst een naam uit de lijst.")

# --- SCHERM 2: PERSOONLIJK RESULTAAT ---
else:
    user = st.session_state.huidige_gebruiker
    st.title(f"Hallo {user} 👋")
    
    if not st.session_state.toon_resultaat:
        st.info("Klik op de knop hieronder om je opdracht te onthullen.")
        
        if st.button("🔍 Onthul mijn lootje"):
            with st.spinner('Tromgeroffel...'):
                time.sleep(1.5)
                st.session_state.toon_resultaat = True
                st.rerun()
    
    else:
        # Het resultaat tonen
        mijn_lootje = uitkomst_dict[user]
        
        st.success("Je lootje is getrokken!")
        st.divider()
        
        st.markdown(f"<h2 style='text-align: center; color: #FF4B4B;'>{mijn_lootje['Categorie']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 18px;'><i>{mijn_lootje['Opdracht']}</i></p>", unsafe_allow_html=True)
        
        st.divider()
        st.warning("⚠️ Houd dit geheim! Sluit dit scherm of log uit als je klaar bent.")

    st.markdown("---")
    if st.button("← Uitloggen / Terug"):
        st.session_state.huidige_gebruiker = None
        st.session_state.toon_resultaat = False
        st.rerun()

# --- Footer ---
st.markdown("---")
st.caption(f"Lootjestrekking Temu Challenge| Seed ID: {TREKKING_SEED}")