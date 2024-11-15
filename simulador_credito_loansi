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

def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")

def calcular_seguro_vida(plazo, seguro_vida_base):
    años = plazo // 12
    return seguro_vida_base * años if años >= 1 else 0

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        .main {
            background-color: #f5f7fa;
            font-family: 'Inter', sans-serif;
            color: #2d3748;
        }
        
        h1 {
            color: #2563eb;
            text-align: center;
            font-weight: 700;
            font-size: 2.2rem;
            margin-bottom: 2rem;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        
        .stSelectbox {
            margin-top: -1rem;
        }
        
        .stSelectbox > div > div {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            font-weight: 600;
            color: #1a202c;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .result-box {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.2rem;
            margin: 1.5rem 0;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .result-amount {
            color: #2563eb;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0.5rem 0;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        
        .whatsapp-link {
            display: inline-block;
            background-color: #22c55e;
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            text-decoration: none;
            font-size: 1.2rem;
            font-weight: 600;
            margin-top: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(34, 197, 94, 0.3);
        }
        
        .whatsapp-link:hover {
            background-color: #16a34a;
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(34, 197, 94, 0.4);
        }
        
        .slider-label {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }

        .input-currency {
            position: relative;
            display: flex;
            align-items: center;
        }

        .currency-symbol {
            position: absolute;
            left: 10px;
            color: #64748b;
            font-weight: 500;
        }

        input[type="text"] {
            padding-left: 25px !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>Simulador de Crédito Loansi</h1>", unsafe_allow_html=True)

st.markdown("<p style='font-weight: 600; font-size: 1rem; margin-bottom: 0.2rem;'>Selecciona la Línea de Crédito</p>", unsafe_allow_html=True)
tipo_credito = st.selectbox("", options=LINEAS_DE_CREDITO.keys(), index=0)
detalles = LINEAS_DE_CREDITO[tipo_credito]

st.markdown(f"<p style='color: #5f6368; font-size: 0.9rem; margin-top: 0.5rem;'>{detalles['descripcion']}</p>", unsafe_allow_html=True)

# Campo de entrada del monto con formato automático
st.markdown("<p style='font-weight: 600; font-size: 1rem; margin: 1rem 0 0.2rem;'>Escribe el valor del crédito</p>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #5f6368; font-size: 0.8rem; margin-bottom: 0.2rem;'>Ingresa un valor entre <b>$ {format_number(detalles['monto_min'])}</b> y <b>$ {format_number(detalles['monto_max'])}</b> COP</p>", unsafe_allow_html=True)

# Inicializar el estado si no existe
if 'monto_str' not in st.session_state:
    st.session_state.monto_str = format_number(detalles['monto_min'])

col1, col2 = st.columns([1,6])
with col1:
    st.markdown("<div style='text-align: right; padding-top: 5px; font-size: 1rem; font-weight: 500;'>$</div>", unsafe_allow_html=True)

with col2:
    monto_str = st.text_input("", value=st.session_state.monto_str, key='monto_input')
    try:
        monto = int(monto_str.replace(".", "").replace(",", ""))
        if monto < detalles["monto_min"]:
            st.warning(f"El valor mínimo es $ {format_number(detalles['monto_min'])}")
            monto = detalles["monto_min"]
        elif monto > detalles["monto_max"]:
            st.warning(f"El valor máximo es $ {format_number(detalles['monto_max'])}")
            monto = detalles["monto_max"]
    except ValueError:
        st.warning("Por favor ingresa un valor válido")
        monto = detalles["monto_min"]

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

st.markdown("""
<div class="whatsapp-section">
    <h3 style='font-size: 1.3rem; font-weight: 600; color: #2c3e50;'>¿Interesado en solicitar este crédito?</h3>
    <p style='color: #5f6368; margin: 0.5rem 0;'>Para más información, comuníquese con nosotros por WhatsApp</p>
    <a href='https://wa.me/XXXXXXXXXXX' target='_blank' class="whatsapp-link">
        Hacer solicitud vía WhatsApp
    </a>
</div>
""", unsafe_allow_html=True)

# Agregar JavaScript para formato automático
st.markdown("""
<script>
    function formatNumber(num) {
        return num.toString().replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }

    document.addEventListener('DOMContentLoaded', function() {
        const inputs = document.querySelectorAll('input[type="text"]');
        inputs.forEach(input => {
            input.addEventListener('input', function(e) {
                const value = this.value.replace(/\D/g, "");
                this.value = formatNumber(value);
            });
        });
    });
</script>
""", unsafe_allow_html=True)
