import streamlit as st
import pandas as pd
import pickle
import sqlite3
import datetime
from auth import login


# ------------------------
# CONFIG APP
# ------------------------
st.set_page_config(page_title="WODStats", page_icon="🏋️", layout="wide")


# ------------------------
# LOGIN
# ------------------------
name, auth_status, username, authenticator = login()

if auth_status is False:
    st.error("Usuario o contraseña incorrecto")
    st.stop()

if auth_status is None:
    st.warning("Ingrese sus credenciales")
    st.stop()

authenticator.logout("Logout", "sidebar")
st.sidebar.success(f"Bienvenido {name}")


# ------------------------
# MODELOS DISPONIBLES
# ------------------------
MODELOS = {
    "Strongfit 2026 Amateur Hombre": "models/modelo_wod.pkl"
    # puedes agregar más después
}


# ------------------------
# FUNCIONES DB
# ------------------------
def save_prediction(user, comp, data, pred):

    conn = sqlite3.connect("logs.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions(
            user TEXT,
            competition TEXT,
            W1T REAL,
            W2T REAL,
            W3T REAL,
            W4R REAL,
            W5AR REAL,
            W5BL REAL,
            prediction REAL,
            date TEXT
        )
    """)

    c.execute("""
        INSERT INTO predictions VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (
        user,
        comp,
        data["W1T"],
        data["W2T"],
        data["W3T"],
        data["W4R"],
        data["W5AR"],
        data["W5BL"],
        pred,
        str(datetime.datetime.now())
    ))

    conn.commit()
    conn.close()


def load_history(user):

    conn = sqlite3.connect("logs.db")

    df = pd.read_sql(
        f"SELECT * FROM predictions WHERE user='{user}'",
        conn
    )

    conn.close()

    return df


# ------------------------
# TÍTULO
# ------------------------
st.title("🏋️ WODStats Predictor Ranking")


# ------------------------
# SELECCIÓN COMPETENCIA
# ------------------------
competencia = st.selectbox(
    "Seleccionar competencia",
    list(MODELOS.keys())
)

model = pickle.load(open(MODELOS[competencia], "rb"))


st.markdown(f"### Competencia seleccionada: {competencia}")


# ------------------------
# INPUTS
# ------------------------
st.subheader("Ingresar resultados")

col1, col2 = st.columns(2)

with col1:
    W1T = st.number_input("W1T (segundos)", 0.0)
    W2T = st.number_input("W2T (segundos)", 0.0)
    W3T = st.number_input("W3T (segundos)", 0.0)

with col2:
    W4R = st.number_input("W4R (reps)", 0.0)
    W5AR = st.number_input("W5AR (reps)", 0.0)
    W5BL = st.number_input("W5BL (libras)", 0.0)


# ------------------------
# PREDICCIÓN
# ------------------------
if st.button("Predecir posición"):

    columnas = ['W1T','W2T','W3T','W4R','W5AR','W5BL']

    data = pd.DataFrame([[W1T,W2T,W3T,W4R,W5AR,W5BL]],
                        columns=columnas)

    data = data.fillna(0)
    data = data.astype(float)

    pred = model.predict(data)

    st.success(f"🏆 Posición estimada: {round(pred[0],2)}")

    # Guardar registro
    save_prediction(username, competencia, data.iloc[0], pred[0])


# ------------------------
# HISTORIAL
# ------------------------
st.divider()
st.subheader("📊 Historial de predicciones")

if st.checkbox("Ver historial"):

    hist = load_history(username)

    if len(hist) > 0:
        st.dataframe(hist, use_container_width=True)
    else:
        st.info("No hay registros aún")
