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
            font-weight: bold;
            padding: 15px 25px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 0 10px;
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
        .button-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>Simulador de Crédito Loansi</h1>", unsafe_allow_html=True)

st.markdown("<p style='font-weight: bold; font-size: 16px; margin-bottom: -5px;'>Selecciona la Línea de Crédito</p>", unsafe_allow_html=True)
tipo_credito = st.selectbox("", options=LINEAS_DE_CREDITO.keys(), index=0)
detalles = LINEAS_DE_CREDITO[tipo_credito]

st.write(f"**Descripción**: {detalles['descripcion']}")

# Inicializar el estado de la sesión si no existe
if 'disabled' not in st.session_state:
    st.session_state.disabled = False

if 'mostrar_resultados' not in st.session_state:
    st.session_state.mostrar_resultados = False

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<p style='font-weight: bold; font-size: 16px; margin-bottom: -5px;'>Escribe el valor del crédito</p>", unsafe_allow_html=True)
    st.write(f"<small>Ingresa un valor entre <b>{detalles['monto_min']:,} COP</b> y <b>{detalles['monto_max']:,} COP</b></small>", unsafe_allow_html=True)
    monto = st.number_input("", 
                           min_value=detalles["monto_min"],
                           max_value=detalles["monto_max"],
                           step=50000,
                           format="%d",
                           disabled=st.session_state.disabled)

if tipo_credito == "LoansiFlex":
    plazo = st.slider("Plazo en Meses:", min_value=detalles["plazo_min"], max_value=detalles["plazo_max"], step=12)
    frecuencia_pago = "Mensual"
else:
    plazo = st.slider("Plazo en Semanas:", min_value=detalles["plazo_min"], max_value=detalles["plazo_max"], step=1)
    frecuencia_pago = "Semanal"

# Cálculos
aval = monto * detalles["aval_porcentaje"]
seguro_vida = calcular_seguro_vida(plazo, detalles.get("seguro_vida_base", 0)) if tipo_credito == "LoansiFlex" else 0
total_financiar = monto + aval + total_costos_asociados + seguro_vida

# Botones centrados
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Simular", key="simulate", disabled=st.session_state.disabled):
        st.session_state.disabled = True
        st.session_state.mostrar_resultados = True

with col2:
    if st.button("Nueva Simulación", key="new_simulate"):
        st.session_state.disabled = False
        st.session_state.mostrar_resultados = False
        st.experimental_rerun()

# Mostrar resultados
if st.session_state.mostrar_resultados:
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
