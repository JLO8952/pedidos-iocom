import streamlit as st
import pandas as pd
from datetime import date
from xhtml2pdf import pisa
import io

# Configuración de página
st.set_page_config(page_title="Generador de Pedidos IOCOM", layout="centered")
st.title("Generador de Pedidos - IOCOM")

# --- BLOQUE DE DATOS DEL LOGO ---
# Copia la cadena larga de 'base64-image.de' y pégala aquí:
LOGO_BASE64 = "TU_LOGO_BASE64_AQUI"

# Formulario
with st.expander("Información del Pedido", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        dep = st.text_input("Departamento", "TALLER DE ENSAMBLE")
        ciudad = st.text_input("Ciudad", "BOGOTA D.C.")
        entregado = st.text_input("Entregado a", "JOHN F. CORREA")
        cliente = st.text_input("Cliente", "IOCOM SAS")
    with col2:
        resp = st.text_input("Responsable", "JOHN F. CORREA")
        pedido_num = st.text_input("Número Pedido", "A-052")
        f_sol = st.date_input("Fecha Solicitud")
        f_ent = st.date_input("Fecha Entrega")
        contrato = st.text_input("N° Contrato", "N/A")

    col3, col4 = st.columns(2)
    with col3:
        parcial = st.radio("Recibe entregas parciales", ["SI", "NO"])
    with col4:
        correo = st.radio("Correo Electrónico", ["SI", "NO"])

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["No.", "REF", "CANT", "STOCK", "PRODUCTO", "OBSERV", "COSTO"])
df_edit = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
notas = st.text_area("Observaciones Generales")

# Generación PDF
if st.button("Generar PDF Final"):
    filas_html = "".join([f"<tr><td>{r['No.']}</td><td>{r['REF']}</td><td>{r['CANT']}</td><td>{r['STOCK']}</td><td>{r['PRODUCTO']}</td><td>{r['OBSERV']}</td><td>{r['COSTO']}</td></tr>" for _, r in df_edit.iterrows()])
    
    html = f"""
    <html>
    <head><style>
        body {{ font-family: sans-serif; font-size: 7px; }}
        table {{ width: 100%; border-collapse: collapse; border: 1px solid #000; }}
        th, td {{ border: 1px solid #000; padding: 3px; text-align: center; }}
        .bg-blue {{ background-color: #D9E2F3; font-weight: bold; }}
    </style></head>
    <body>
        <table border="1">
            <tr>
                <td width="20%"><img src="{LOGO_BASE64}" width="50"></td>
                <td width="50%" class="bg-blue" style="font-size: 11px;">ORDEN DE PEDIDO INTERNA</td>
                <td width="30%">DOCUMENTO CONTROLADO<br>PÁGINA 1 DE 1<br>VERSIÓN 004 - 08 NOV 2022</td>
            </tr>
        </table>
        
        <table>
            <tr><td class="bg-blue">DEPARTAMENTO</td><td>{dep}</td><td class="bg-blue">RESPONSABLE</td><td>{resp}</td><td class="bg-blue">PEDIDO</td><td>{pedido_num}</td></tr>
            <tr><td class="bg-blue">CIUDAD</td><td>{ciudad}</td><td class="bg-blue">CONTRATO</td><td>{contrato}</td><td class="bg-blue">F. SOLICITUD</td><td>{f_sol}</td></tr>
        </table>
        
        <table style="margin-top:5px;">
            <tr class="bg-blue"><th>No.</th><th>REF</th><th>CANT</th><th>STOCK</th><th>PRODUCTO</th><th>OBSERV.</th><th>COSTO</th></tr>
            {filas_html}
        </table>
        
        <table style="margin-top:20px; border:none;">
            <tr>
                <td style="border:1px solid #000; height:30px;">{resp}<br>JEFE TALLER</td>
                <td style="border:1px solid #000; height:30px;">JULIO CARDENAS<br>RECIBE</td>
                <td style="border:1px solid #000; height:30px;">JULIO CARDENAS<br>APROBACIÓN</td>
            </tr>
        </table>
    </body>
    </html>
    """
    result = io.BytesIO()
    pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    st.download_button("Descargar PDF", data=result.getvalue(), file_name="Pedido_Final.pdf", mime="application/pdf")
