import streamlit as st
import random
import time

# --- CONFIGURATIE ---
# BELANGRIJK: Verander dit getal voor de DEFINITIEVE trekking!
# Zolang dit getal hetzelfde blijft, is de uitslag van de trekking ook exact hetzelfde,
# zelfs als de server herstart.
TREKKING_SEED = 123 

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
    Omdat de seed vaststaat, is de 'random' shuffle altijd deterministisch.
    Dit betekent: Zelfde seed = Zelfde uitslag. Altijd.
    """
    
    # We maken een specifieke random generator met de gekozen seed
    rng = random.Random(seed_waarde)
    
    # 1. Maak de pool van taken (2x elke categorie)
    taken_pool = []
    for naam, omschrijving in CATEGORIEEN.items():
        taken_pool.append((naam, omschrijving))
        taken_pool.append((naam, omschrijving))
    
    # 2. Schud de taken met onze vaste generator
    rng.shuffle(taken_pool)
    
    # We schudden ook de deelnemers (optioneel, maar leuk voor de variatie)
    # We gebruiken een kopie van de lijst om de originele constante niet te wijzigen
    deelnemers_shuffle = DEELNEMERS[:] 
    # We sorteren ze eerst om zeker te zijn dat de startpositie altijd gelijk is voor de shuffle
    deelnemers_shuffle.sort() 
    # rng.shuffle(deelnemers_shuffle) # Laten we de namen op alfabet laten en de taken shufflen, dat is overzichtelijker.
    
    # 3. Koppel ze aan elkaar in een dictionary
    toewijzingen = {}
    for i, deelnemer in enumerate(deelnemers_shuffle):
        cat_naam, cat_desc = taken_pool[i]
        toewijzingen[deelnemer] = {
            "Categorie": cat_naam,
            "Opdracht": cat_desc
        }
        
    return toewijzingen

# --- Streamlit UI ---

st.set_page_config(page_title="Lootjestrekking", layout="centered", page_icon="🎁")

st.title("🎁 Lootjestrekking")
st.markdown(f"""
Welkom bij de **Temu Challenge**! 
Iedereen trekt één lootje. De trekking is vastgelegd in het systeem.
""")

# Haal de trekking op basis van de SEED
uitkomst_dict = genereer_globale_trekking(TREKKING_SEED)

st.markdown("---")

# Stap 1: Wie ben jij?
st.subheader("Wie ben jij?")
geselecteerde_naam = st.selectbox(
    "Kies je naam uit de lijst:",
    ["Kies een naam..."] + sorted(DEELNEMERS)
)

# Sessie status om te bepalen of we het lootje moeten tonen
if "toon_lootje" not in st.session_state:
    st.session_state.toon_lootje = False
if "huidige_user" not in st.session_state:
    st.session_state.huidige_user = None

# Reset knop als er van naam gewisseld wordt
if st.session_state.huidige_user != geselecteerde_naam:
    st.session_state.toon_lootje = False
    st.session_state.huidige_user = geselecteerde_naam

# Stap 2: Trekken
if geselecteerde_naam != "Kies een naam...":
    st.info(f"Hallo **{geselecteerde_naam}**! Klik op de knop hieronder om jouw opdracht te onthullen.")
    
    if st.button("🔍 Onthul mijn lootje"):
        with st.spinner('Even in de hoge hoed graaien...'):
            time.sleep(1.0) 
            st.session_state.toon_lootje = True
            st.rerun()

    # Stap 3: Resultaat
    if st.session_state.toon_lootje:
        mijn_lootje = uitkomst_dict[geselecteerde_naam]
        
        st.divider()
        st.balloons()
        
        st.markdown(f"### 🎉 Jouw Categorie: **{mijn_lootje['Categorie']}**")
        st.success(f"**Opdracht:** {mijn_lootje['Opdracht']}")
        
        st.warning("⚠️ **Houd dit geheim!** Vernieuw de pagina of sluit de browser om je lootje weer te verbergen.")

# --- Footer ---
st.markdown("---")
st.caption(f"Trekking ID: #{TREKKING_SEED} (Controlegetal)")