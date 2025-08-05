import numpy as np
import random
import math
import streamlit as st

st.set_page_config(page_title="Générateur de mots FR", page_icon="🔤")

st.title("🔤 Générateur de mots en français (Bigrammes filtrés, k=6)")

# Chargement direct des matrices pré-calculées
H = np.load("H.npy")
start_probs = np.load("debut.npy")

mots_a_generer = st.number_input("Nombre de mots à générer", 1, 100, 10)
l = st.number_input("Longueur des mots", 2, 20, 8)

# Calcul stats
total = np.sum(H)
P = H / total
Hglob = -np.sum(P[P > 0] * np.log(P[P > 0]) / np.log(676))
Neffectif = 676 ** Hglob
nb_valides = np.sum(H > 0)

st.markdown(f"**Bigrammes retenus :** {nb_valides}")
st.markdown(f"**Entropie globale :** {Hglob:.3f}")
st.markdown(f"**Nombre effectif de bigrammes :** {math.ceil(Neffectif)}")

# Génération mots
mots = []
for _ in range(mots_a_generer):
    mot = ""
    current = random.choices(range(26), weights=start_probs, k=1)[0]
    mot += chr(current + 97)
    for _ in range(l - 1):
        probs = H[current]
        if np.sum(probs) == 0:
            break
        next_letter = random.choices(range(26), weights=probs, k=1)[0]
        mot += chr(next_letter + 97)
        current = next_letter
    mots.append(mot)

st.subheader("Mots générés")
st.write(", ".join(mots))
