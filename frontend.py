import streamlit as st
import requests

API_URL = "https://customer-churn-fase-ii.onrender.com/predict"

st.set_page_config(
    page_title="Customer Churn",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Customer Churn Prediction")
st.write(
    "Ingresa la información del cliente para estimar "
    "la posibilidad de cancelación del servicio."
)

with st.form("formulario_cliente"):

    st.subheader("Información del cliente")

    gender = st.selectbox("Género", ["Female", "Male"])
    senior = st.selectbox("¿Es adulto mayor?", ["YES", "NO"])
    partner = st.selectbox("¿Tiene pareja?", ["Yes", "No"])
    dependents = st.selectbox("¿Tiene dependientes?", ["Yes", "No"])

    tenure = st.number_input(
        "Antigüedad del cliente (meses)",
        min_value=0,
        max_value=100,
        value=12
    )

    st.subheader("Servicios contratados")

    phone = st.selectbox("Servicio telefónico", ["Yes", "No"])
    multiple_lines = st.selectbox(
        "Líneas múltiples",
        ["No", "Yes", "No phone service"]
    )

    internet = st.selectbox(
        "Servicio de internet",
        ["DSL", "Fiber optic", "No"]
    )

    online_security = st.selectbox(
        "Seguridad en línea",
        ["Yes", "No", "No internet service"]
    )

    online_backup = st.selectbox(
        "Respaldo en línea",
        ["Yes", "No", "No internet service"]
    )

    device_protection = st.selectbox(
        "Protección de dispositivos",
        ["Yes", "No", "No internet service"]
    )

    tech_support = st.selectbox(
        "Soporte técnico",
        ["Yes", "No", "No internet service"]
    )

    streaming_tv = st.selectbox(
        "Streaming TV",
        ["Yes", "No", "No internet service"]
    )

    streaming_movies = st.selectbox(
        "Streaming de películas",
        ["Yes", "No", "No internet service"]
    )

    st.subheader("Contrato y pagos")

    contract = st.selectbox(
        "Tipo de contrato",
        ["Month-to-month", "One year", "Two year"]
    )

    paperless = st.selectbox(
        "¿Facturación electrónica?",
        ["Yes", "No"]
    )

    payment = st.selectbox(
        "Método de pago",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

    monthly_charges = st.number_input(
        "Cargo mensual",
        min_value=0.0,
        value=50.0
    )

    total_charges = st.number_input(
        "Cargos totales",
        min_value=0.0,
        value=600.0
    )

    modelo = st.selectbox(
        "Modelo de predicción",
        ["logistic_regression", "random_forest"]
    )

    enviar = st.form_submit_button("Predecir churn")

if enviar:

    cliente = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple_lines,
        "InternetService": internet,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    try:
        respuesta = requests.post(
            API_URL,
            params={"modelo": modelo},
            json=cliente,
            timeout=30
        )

        respuesta.raise_for_status()
        resultado = respuesta.json()

        st.subheader("Resultado de la predicción")

        if resultado["prediccion"] == 1:
            st.error("⚠️ Posible churn")
        else:
            st.success("✅ Cliente permanece")

        st.metric(
            "Probabilidad de churn",
            f'{resultado["probabilidad_churn"]:.2%}'
        )

        st.metric(
            "Probabilidad de no churn",
            f'{resultado["probabilidad_no_churn"]:.2%}'
        )

        st.caption(f'Modelo utilizado: {resultado["modelo"]}')

    except requests.exceptions.RequestException as error:
        st.error(f"No fue posible conectar con la API: {error}")
