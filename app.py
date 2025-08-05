import numpy as np
import random
import math
import streamlit as st

st.set_page_config(page_title="Générateur de mots FR", page_icon="🔤")
st.title("🔤 Générateur de mots en français (Bigrammes filtrés, k=6)")

H = np.load("H.npy")
D = np.load("debut.npy")

m = st.number_input("Nombre de mots à générer", 1, 100, 4)
l = st.number_input("Longueur des mots", 2, 20, 6)

t = np.sum(H)
P = H / t
Hg = -np.sum(P[P > 0] * np.log(P[P > 0]) / np.log(676))
Ne = 676 ** Hg
nb = np.sum(H > 0)

st.markdown(f"**Bigrammes retenus :** {nb}")
st.markdown(f"**Entropie globale :** {Hg:.3f}")
st.markdown(f"**Nombre effectif de bigrammes :** {math.ceil(Ne)}")

res = []
for _ in range(m):
    mot = ""
    cur = random.choices(range(26), weights=D, k=1)[0]
    mot += chr(cur + 97)
    for _ in range(l - 1):
        pr = H[cur]
        if np.sum(pr) == 0:
            break
        nxt = random.choices(range(26), weights=pr, k=1)[0]
        mot += chr(nxt + 97)
        cur = nxt
    res.append(mot)

st.subheader("Mots générés")
st.write(", ".join(res))
