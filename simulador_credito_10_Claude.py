import streamlit as st

# Función para formatear números con separadores de miles
def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")

# Datos para cada línea de crédito (resto del código igual)
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

# Estilos (mismo código CSS que antes)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        .main {
            background-color: #ffffff;
            font-family: 'Inter', sans-serif;
        }
        
        h1 {
            color: #1a73e8;
            text-align: center;
            font-weight: 700;
            font-size: 2.2rem;
            margin-bottom: 2rem;
        }
        
        .stSelectbox {
            margin-top: -1rem;
        }
        
        .stSelectbox > div > div {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            font-weight: 600;
        }
        
        .number-input label {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.3rem;
        }
        
        .number-input input {
            font-size: 1.1rem;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 0.5rem;
            background-color: #f8f9fa;
        }
        
        .result-box {
            background-color: #f0f7ff;
            border: 1px solid #cce5ff;
            border-radius: 12px;
            padding: 1.2rem;
            margin: 1.5rem 0;
            text-align: center;
        }
        
        .result-amount {
            color: #1a73e8;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }
        
        .result-period {
            color: #5f6368;
            font-size: 1rem;
            font-weight: 500;
        }
        
        .expander-content {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 0.5rem;
        }
        
        .detail-item {
            display: flex;
            justify-content: space-between;
            margin: 0.5rem 0;
            padding: 0.5rem 0;
            border-bottom: 1px solid #e9ecef;
        }
        
        .whatsapp-section {
            text-align: center;
            margin-top: 2rem;
            padding: 1.5rem;
            background-color: #f8f9fa;
            border-radius: 12px;
        }
        
        .whatsapp-link {
            display: inline-block;
            background-color: #25D366;
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            text-decoration: none;
            font-size: 1.2rem;
            font-weight: 600;
            margin-top: 1rem;
            transition: background-color 0.3s ease;
        }
        
        .whatsapp-link:hover {
            background-color: #128C7E;
        }
        
        .slider-label {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>Simulador de Crédito Loansi</h1>", unsafe_allow_html=True)

# Selección de línea de crédito con estilo mejorado
st.markdown("<p style='font-weight: 600; font-size: 1rem; margin-bottom: 0.2rem;'>Selecciona la Línea de Crédito</p>", unsafe_allow_html=True)
tipo_credito = st.selectbox("", options=LINEAS_DE_CREDITO.keys(), index=0)
detalles = LINEAS_DE_CREDITO[tipo_credito]

st.markdown(f"<p style='color: #5f6368; font-size: 0.9rem; margin-top: 0.5rem;'>{detalles['descripcion']}</p>", unsafe_allow_html=True)

# Campo de entrada del monto con formato automático
st.markdown("<p style='font-weight: 600; font-size: 1rem; margin: 1rem 0 0.2rem;'>Escribe el valor del crédito</p>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #5f6368; font-size: 0.8rem; margin-bottom: 0.2rem;'>Ingresa un valor entre <b>$ {format_number(detalles['monto_min'])}</b> y <b>$ {format_number(detalles['monto_max'])}</b> COP</p>", unsafe_allow_html=True)

monto = st.number_input("", 
                       min_value=detalles["monto_min"],
                       max_value=detalles["monto_max"],
                       step=1000,
                       format="%d")

# Slider de plazo con estilo mejorado
if tipo_credito == "LoansiFlex":
    st.markdown("<p class='slider-label'>Plazo en Meses</p>", unsafe_allow_html=True)
    plazo = st.slider("", min_value=detalles["plazo_min"], max_value=detalles["plazo_max"], step=12)
    frecuencia_pago = "Mensual"
else:
    st.markdown("<p class='slider-label'>Plazo en Semanas</p>", unsafe_allow_html=True)
    plazo = st.slider("", min_value=detalles["plazo_min"], max_value=detalles["plazo_max"], step=1)
    frecuencia_pago = "Semanal"

# Cálculos
aval = monto * detalles["aval_porcentaje"]
seguro_vida = calcular_seguro_vida(plazo, detalles.get("seguro_vida_base", 0)) if tipo_credito == "LoansiFlex" else 0
total_financiar = monto + aval + total_costos_asociados + seguro_vida

# Cálculo de cuota y mostrar resultados
if tipo_credito == "LoansiFlex":
    cuota = (total_financiar * (detalles["tasa_mensual"] / 100)) / (1 - (1 + detalles["tasa_mensual"] / 100) ** -plazo)
else:
    tasa_semanal = (1 + detalles["tasa_mensual"] / 100) ** (1/4) - 1
    cuota = (total_financiar * tasa_semanal) / (1 - (1 + tasa_semanal) ** -plazo)

st.markdown(f"""
<div class="result-box">
    <p style='margin-bottom: 0.5rem;'>Pagarás {plazo} cuotas por un valor aproximado de:</p>
    <div class="result-amount">$ {format_number(cuota)} {frecuencia_pago}</div>
</div>
""", unsafe_allow_html=True)

# Detalles del crédito con orden mejorado
with st.expander("Ver Detalles del Crédito"):
    total_interes = cuota * plazo - total_financiar
    total_pagar = cuota * plazo
    
    detalles_orden = [
        ("Monto Solicitado", f"$ {format_number(monto)} COP"),
        ("Plazo", f"{plazo} {'meses' if tipo_credito == 'LoansiFlex' else 'semanas'}"),
        ("Frecuencia de Pago", frecuencia_pago),
        ("Tasa de Interés Mensual", f"{detalles['tasa_mensual']}%"),
        ("Tasa Efectiva Anual (E.A.)", f"{detalles['tasa_anual_efectiva']}%"),
        ("Costo del Aval", f"$ {format_number(aval)} COP"),
        ("Costos Asociados", f"$ {format_number(total_costos_asociados)} COP"),
    ]
    
    if tipo_credito == "LoansiFlex":
        detalles_orden.append(("Seguro de Vida", f"$ {format_number(seguro_vida)} COP"))
    
    detalles_orden.extend([
        ("Total Intereses", f"$ {format_number(total_interes)} COP"),
        ("Total a Pagar", f"$ {format_number(total_pagar)} COP")
    ])
    
    for titulo, valor in detalles_orden:
        st.markdown(f"""
        <div class="detail-item">
            <span style="font-weight: 500;">{titulo}</span>
            <span style="font-weight: 600;">{valor}</span>
        </div>
        """, unsafe_allow_html=True)

# Sección de WhatsApp mejorada
st.markdown("""
<div class="whatsapp-section">
    <h3 style='font-size: 1.3rem; font-weight: 600; color: #2c3e50;'>¿Interesado en solicitar este crédito?</h3>
    <p style='color: #5f6368; margin: 0.5rem 0;'>Para más información, comuníquese con nosotros por WhatsApp</p>
    <a href='https://wa.me/XXXXXXXXXXX' target='_blank' class="whatsapp-link">
        Hacer solicitud vía WhatsApp
    </a>
</div>
""", unsafe_allow_html=True)
