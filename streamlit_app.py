import streamlit as st
import pandas as pd
import pickle

# ------------------------
# Cargar modelo
# ------------------------
model = pickle.load(open("modelo_wod.pkl", "rb"))

st.title("🏋️ Predictor Ranking CrossFit")

st.write("Ingrese resultados de los WOD")

# ------------------------
# Inputs
# ------------------------
W1T = st.number_input("W1T (segundos)", 0.0)
W2T = st.number_input("W2T (segundos)", 0.0)
W3T = st.number_input("W3T (segundos)", 0.0)
W4R = st.number_input("W4R (reps)", 0.0)
W5AR = st.number_input("W5AR (reps)", 0.0)
W5BL = st.number_input("W5BL (libras)", 0.0)

# ------------------------
# Botón predicción
# ------------------------
if st.button("Predecir posición"):

    data = pd.DataFrame([{
        'W1T': W1T,
        'W2T': W2T,
        'W3T': W3T,
        'W4R': W4R,
        'W5AR': W5AR,
        'W5BL': W5BL
    }])

    pred = model.predict(data)

    st.success(f"Posición estimada: {round(pred[0],2)}")
