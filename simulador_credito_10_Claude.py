import streamlit as st

# Datos para cada línea de crédito
LINEAS_DE_CREDITO = {
    "LoansiFlex": {
        "descripcion": "Crédito de libre inversión para empleados, independientes, personas naturales y pensionados.",
        "monto_min": 1000000,
        "monto_max": 20000000,
        "plazo_min": 12,
        "plazo_max": 60,
        "tasa_mensual": 1.9715,  
        "tasa_anual_efectiva": 26.4,  
        "aval_porcentaje": 0.10,  
        "seguro_vida_base": 150000  
    },
    "Microflex": {
        "descripcion": "Crédito rotativo para personas en sectores informales, orientado a cubrir necesidades de liquidez rápida con pagos semanales.",
        "monto_min": 50000,
        "monto_max": 500000,
        "plazo_min": 4,
        "plazo_max": 8,
        "tasa_mensual": 2.0718,  
        "tasa_anual_efectiva": 27.9,  
        "aval_porcentaje": 0.12,  
    }
}

COSTOS_ASOCIADOS = {
    "Pagaré Digital": 2800,
    "Carta de Instrucción": 2800,
    "Custodia TVE": 5600,
    "Consulta Datacrédito": 11000
}

total_costos_asociados = sum(COSTOS_ASOCIADOS.values())

def calcular_seguro_vida(plazo, seguro_vida_base):
    años = plazo // 12
    return seguro_vida_base * años if años >= 1 else 0

st.markdown("""
    <style>
        .main {
            background-color: #f5f5f5;
            font-family: 'Arial', sans-serif;
        }
        h1 {
            color: #4A90E2;
            text-align: center;
            font-weight: bold;
        }
        .stButton button {
            background-color: #4A90E2;
            color: white;
            font-size: 24px;
            padding: 15px 25px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: fit-content;
            display: block;
            margin: 0 auto;
        }
        .stButton button:hover {
            background-color: #357ABD;
        }
        .result-box {
            border: 1px solid #4A90E2;
            padding: 15px;
            border-radius: 5px;
            background-color: #E6F7FF;
            text-align: center;
            width: fit-content;
            margin: 20px auto;
        }
        .whatsapp-box {
            text-align: center;
            margin-top: 20px;
        }
        .whatsapp-link {
            color: #4A90E2;
            font-weight: bold;
            font-size: 22px;
            text-decoration: none;
        }
        .whatsapp-link:hover {
            color: #357ABD;
        }
        .info-text {
            text-align: center;
            font-size: 14px;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>Simulador de Crédito Loansi</h1>", unsafe_allow_html=True)

st.markdown("<p style='font-weight: bold; font-size: 16px; margin-bottom: -10px;'>Selecciona la Línea de Crédito</p>", unsafe_allow_html=True)
tipo_credito = st.selectbox("", options=LINEAS_DE_CREDITO.keys())
detalles = LINEAS_DE_CREDITO[tipo_credito]

st.write(f"**Descripción**: {detalles['descripcion']}")

st.markdown("<p style='font-weight: bold; font-size: 16px; margin-bottom: -10px;'>Escribe el valor del crédito</p>", unsafe_allow_html=True)
st.write(f"<small>Ingresa un valor entre <b>{detalles['monto_min']:,} COP</b> y <b>{detalles['monto_max']:,} COP</b></small>", unsafe_allow_html=True)
monto = st.number_input(
    "", min_value=detalles["monto_min"], max_value=detalles["monto_max"], step=50000, format="%d", disabled=tipo_credito != "LoansiFlex"
)

aval = monto * detalles["aval_porcentaje"]

seguro_vida = calcular_seguro_vida(plazo=detalles["plazo_max"], seguro_vida_base=detalles.get("seguro_vida_base", 0)) if tipo_credito == "LoansiFlex" else 0

total_financiar = monto + aval + total_costos_asociados + seguro_vida

if tipo_credito == "LoansiFlex":
    plazo = st.slider("Plazo en Meses:", min_value=detalles["plazo_min"], max_value=detalles["plazo_max"], step=12)
    frecuencia_pago = "Mensual"
else:
    plazo = st.slider("Plazo en Semanas:", min_value=detalles["plazo_min"], max_value=detalles["plazo_max"], step=1)
    frecuencia_pago = "Semanal"

if st.button("Simular", key="simulate"):
    if tipo_credito == "LoansiFlex":
        cuota = (total_financiar * (detalles["tasa_mensual"] / 100)) / (1 - (1 + detalles["tasa_mensual"] / 100) ** -plazo)
    else:
        tasa_semanal = (1 + detalles["tasa_mensual"] / 100) ** (1/4) - 1
        cuota = (total_financiar * tasa_semanal) / (1 - (1 + tasa_semanal) ** -plazo)

    st.markdown(f"""
    <div class="result-box">
        <h2 style="color: #4A90E2; font-weight: bold;">Pagarás {plazo} cuotas por un valor aproximado de:</h2>
        <h2 style="color: #4A90E2; font-weight: bold;">COP {cuota:,.0f} {frecuencia_pago}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.button("Nueva Simulación", key="new_simulate", disabled=True)

    with st.expander("Ver Detalles del Crédito"):
        total_interes = cuota * plazo - total_financiar
        total_pagar = cuota * plazo
        st.write(f"**Monto Solicitado**: COP {monto:,.0f}")
        st.write(f"**Tasa de Interés Mensual**: {detalles['tasa_mensual']}%")
        st.write(f"**Interés Efectivo Anual (E.A.)**: {detalles['tasa_anual_efectiva']}%")
        st.write(f"**Frecuencia de Pago**: {frecuencia_pago}")
        st.write(f"**Número de Cuotas**: {plazo}")
        st.write(f"**Costo del Aval y Otros**: COP {total_costos_asociados + aval:,.0f}")
        if tipo_credito == "LoansiFlex":
            st.write(f"**Seguro de Vida**: COP {seguro_vida:,.0f}")
        st.write(f"**Total del Interés a Pagar**: COP {total_interes:,.0f}")
        st.write(f"**Total a Pagar**: COP {total_pagar:,.0f}")

    st.markdown("<h3 style='text-align: center;'>¿Interesado en solicitar este crédito?</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Para más información, comuníquese con nosotros por WhatsApp:</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'><a href='https://wa.me/XXXXXXXXXXX' target='_blank' class='whatsapp-link'>Hacer solicitud vía WhatsApp</a></p>", unsafe_allow_html=True)