import numpy as np
import math
import random
import streamlit as st

st.set_page_config(page_title="Générateur de mots FR", page_icon="🔤")

st.title("🔤 Générateur de mots en français (Bigrammes filtrés)")

with open("mots_fr.txt", "r", encoding="utf-8") as fichier:
    L = [ligne.strip().lower() for ligne in fichier if ligne.strip()]

k = st.slider("Nombre de transitions conservées par ligne (k)", 1, 26, 3)
mots_a_generer = st.number_input("Nombre de mots à générer", 1, 100, 10)
l = st.number_input("Longueur des mots", 2, 20, 8)

n = len(L)
M = np.zeros((26, 26), dtype=int)
H = np.zeros((26, 26), dtype=float)
start_counts = np.zeros(26, dtype=int)

for mot in L:
    if mot:
        first_letter = ord(mot[0]) - 97
        if 0 <= first_letter < 26:
            start_counts[first_letter] += 1
    for j in range(len(mot) - 1):
        a = ord(mot[j]) - 97
        b = ord(mot[j + 1]) - 97
        if 0 <= a < 26 and 0 <= b < 26:
            M[a][b] += 1

for i in range(26):
    s = sum(M[i])
    if s > 0:
        H[i] = M[i] / s

for i in range(26):
    if np.count_nonzero(H[i]) > k:
        top_k_idx = np.argsort(H[i])[-k:]
        mask = np.ones(26, dtype=bool)
        mask[top_k_idx] = False
        H[i][mask] = 0

start_probs = start_counts / np.sum(start_counts)
total = np.sum(H)
P = H / total
Hglob = -np.sum(P[P > 0] * np.log(P[P > 0]) / np.log(676))
Neffectif = 676 ** Hglob
nb_valides = np.sum(H > 0)

st.markdown(f"**Bigrammes retenus :** {nb_valides}")
st.markdown(f"**Entropie globale :** {Hglob:.3f}")
st.markdown(f"**Nombre effectif de bigrammes :** {math.ceil(Neffectif)}")

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
