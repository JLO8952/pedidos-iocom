import streamlit as st
import pandas as pd
from datetime import date
from xhtml2pdf import pisa
import io

# Configuración de la página
st.set_page_config(page_title="Pedidos IOCOM", page_icon="📝", layout="centered")

st.title("Generador de Pedidos - IOCOM")
st.markdown("**Orden de Pedido Interna - Taller de Ensamble**")

# Función para cargar el logo
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except:
        return ""

logo_base64 = get_image_base64("logo.png")

# Sección 1: Información General
with st.expander("Información del Pedido", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        departamento = st.text_input("Departamento Solicita", "TALLER DE ENSAMBLE")
        ciudad = st.text_input("Ciudad", "BOGOTA D.C.")
        entregado_a = st.text_input("Entregado a", "JOHN F. CORREA")
        cliente = st.text_input("Cliente", "IOCOM SAS")
        
    with col2:
        responsable = st.text_input("Responsable de la Solicitud", "JOHN F. CORREA")
        num_pedido = st.text_input("Número de Pedido", "A-000")
        fecha_solicitud = st.date_input("Fecha Solicitud", date.today())
        fecha_entrega = st.date_input("Fecha Entrega", date.today())
        num_contrato = st.text_input("N° Contrato", "N/A")

    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        recibo_personal = st.radio("Recibo Personalmente", ["SI", "NO"], horizontal=True)
        entregas_parciales = st.radio("Recibe entregas parciales", ["SI", "NO"], horizontal=True)
    with col4:
        correo_electronico = st.radio("Correo Electrónico", ["SI", "NO"], horizontal=True)

# Sección 2: Productos
st.subheader("Ítems a Solicitar")

if "datos_productos" not in st.session_state:
    st.session_state.datos_productos = pd.DataFrame({
        "CANTIDAD": [],
        "PRODUCTO": [],
        "STOCK": [],
        "OBSERVACIONES": []
    })

tabla_editada = st.data_editor(
    st.session_state.datos_productos, 
    num_rows="dynamic",
    use_container_width=True
)

observaciones_generales = st.text_area("Observaciones Generales de la Orden", height=80)

st.divider()

# Sección 3: Generación de PDF
if st.button("Generar PDF de Orden", type="primary"):
    
    # Lógica de las "X" en las casillas
    parcial_si = "X" if entregas_parciales == "SI" else ""
    parcial_no = "X" if entregas_parciales == "NO" else ""
    correo_si = "X" if correo_electronico == "SI" else ""
    correo_no = "X" if correo_electronico == "NO" else ""
    personal_si = "X" if recibo_personal == "SI" else ""
    personal_no = "X" if recibo_personal == "NO" else ""
    
    # Filas de la tabla
    filas_html = ""
    for index, row in tabla_editada.iterrows():
        filas_html += f"""
        <tr>
            <td width="5%" class="text-center">{index + 1}</td>
            <td width="12%" class="text-center">N/A</td>
            <td width="12%" class="text-center">{row['CANTIDAD']}</td>
            <td width="8%">{row['STOCK']}</td>
            <td width="33%">{row['PRODUCTO']}</td>
            <td width="15%">{row['OBSERVACIONES']}</td>
            <td width="15%"></td>
        </tr>
        """

    # PLANTILLA HTML CLONADA EXACTAMENTE A LA IMAGEN (HORIZONTAL)
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ 
                size: A4 landscape; /* Hoja horizontal obligatoria para las 10 columnas */
                margin: 10mm 12mm; 
            }}
            body {{ font-family: Helvetica, sans-serif; font-size: 8px; color: #000; }}
            table {{ border-collapse: collapse; margin-bottom: 0px; }}
            th, td {{ border: 1px solid #000; padding: 4px; vertical-align: middle; }}
            
            /* Color azul exacto de la plantilla corporativa */
            .bg-blue {{ background-color: #B4C6E7; font-weight: bold; text-align: center; }}
            
            .text-center {{ text-align: center; }}
            .text-left {{ text-align: left; }}
        </style>
    </head>
    <body>

        <table width="100%" border="1" cellpadding="3" cellspacing="0">
            <tr>
                <td rowspan="3" width="22%" class="text-center" style="border-right: 1px solid #000;">
                    <h1 style="margin: 0; font-size: 28px; color: #17365D; letter-spacing: 1px;">iocom</h1>
                    <span style="font-size: 7px; color: #17365D; font-style: italic;">Always Evolving</span>
                </td>
                <td rowspan="3" width="60%" class="bg-blue" style="font-size: 14px;">
                    ORDEN DE PEDIDO INTERNA
                </td>
                <td width="18%" class="text-center" style="font-size: 7px;">DOCUMENTO CONTROLADO</td>
            </tr>
            <tr><td class="text-center" style="font-size: 7px;">PÁGINA 1 DE 1</td></tr>
            <tr><td class="text-center" style="font-size: 7px;">VERSIÓN 004<br>08 DE NOVIEMBRE DE 2022</td></tr>
        </table>

        <table width="100%" border="1" cellpadding="3" cellspacing="0" style="margin-top: -1px;">
            <tr>
                <td width="17%" class="bg-blue text-left">DEPARTAMENTO SOLICITA</td>
                <td width="28%" class="text-center">{departamento}</td>
                <td width="18%" class="bg-blue" style="font-size: 7px;">NOMBRE DEL<br>RESPONSABLE DE LA<br>SOLICITUD</td>
                <td width="21%" class="text-center">{responsable}</td>
                <td width="10%" class="bg-blue">NÚMERO PEDIDO</td>
                <td width="6%" class="text-center font-bold">{num_pedido}</td>
            </tr>
        </table>

        <table width="100%" border="1" cellpadding="3" cellspacing="0" style="margin-top: -1px;">
            <tr>
                <td width="11%" class="bg-blue">CIUDAD</td>
                <td width="14%" class="text-center">{ciudad}</td>
                <td width="11%" class="bg-blue">N° CONTRATO</td>
                <td width="10%" class="text-center">{num_contrato}</td>
                <td width="14%" class="bg-blue">FECHA SOLICITUD</td>
                <td width="15%" class="text-center">{fecha_solicitud.strftime('%d/%m/%Y')}</td>
                <td width="13%" class="bg-blue">FECHA ENTREGA</td>
                <td width="12%" class="text-center">{fecha_entrega.strftime('%d/%m/%Y')}</td>
            </tr>
        </table>

        <table width="100%" border="1" cellpadding="3" cellspacing="0" style="margin-top: -1px;">
            <tr>
                <td width="18%" class="bg-blue text-left">ENTREGADO A:</td>
                <td width="42%" class="text-center">{entregado_a}</td>
                <td width="15%" class="bg-blue">DEPARTAMENTO</td>
                <td width="25%" class="text-center">{departamento}</td>
            </tr>
            <tr>
                <td width="18%" class="bg-blue text-left">CLIENTE</td>
                <td width="42%" class="text-center">{cliente}</td>
                <td width="15%" class="bg-blue">USUARIO FINAL</td>
                <td width="25%" class="text-center">{cliente}</td>
            </tr>
        </table>

        <table width="100%" border="1" cellpadding="3" cellspacing="0" style="margin-top: -1px;">
            <tr>
                <td width="20%" class="bg-blue text-left">CANAL DE RECIBO DE PEDIDO</td>
                <td width="15%" class="bg-blue">PERSONALMENTE</td>
                <td width="5%" class="bg-blue">SI</td>
                <td width="5%" class="text-center">{personal_si}</td>
                <td width="5%" class="bg-blue">NO</td>
                <td width="13%" class="text-center">{personal_no}</td>
                <td width="17%" class="bg-blue">CORREO<br>ELECTRÓNICO</td>
                <td width="5%" class="bg-blue">SI</td>
                <td width="5%" class="text-center">{correo_si}</td>
                <td width="10%" class="bg-blue">NO</td>
            </tr>
        </table>

        <table width="100%" border="1" cellpadding="3" cellspacing="0" style="margin-top: -1px;">
            <tr>
                <td width="20%" class="bg-blue text-left">RECIBE ENTREGAS PARCIALES</td>
                <td width="5%" class="bg-blue">SI</td>
                <td width="7%" class="text-center">{parcial_si}</td>
                <td width="8%" class="bg-blue">NO</td>
                <td width="20%" class="text-center">{parcial_no}</td>
                <td width="30%" class="bg-blue">RANGO DE TIEMPO PARA ENTREGA</td>
                <td width="10%" class="text-center">N/A</td>
            </tr>
            <tr>
                <td colspan="7" class="text-center" style="font-weight: bold; font-size: 7px; background-color: #ffffff;">
                    SI LA ENTREGA ES PARCIAL, POR FAVOR ESPECIFIQUE EL TIEMPO DE LA ENTREGA PARCIAL.
                </td>
            </tr>
        </table>

        <table width="100%" border="1" cellpadding="3" cellspacing="0" style="margin-top: 5px;">
            <thead>
                <tr class="bg-blue">
                    <th width="5%">No.<br>ITEM</th>
                    <th width="12%">REFERENCIA</th>
                    <th width="12%">CANTIDAD<br>SOLICITADA</th>
                    <th width="8%">STOCK</th>
                    <th width="33%">NOMBRE DEL PRODUCTO</th>
                    <th width="15%">OBSERVACIONES</th>
                    <th width="15%">COSTO </th>
                </tr>
            </thead>
            <tbody>
                {filas_html}
            </tbody>
        </table>

        <table width="100%" border="1" cellpadding="3" cellspacing="0" style="margin-top: 5px;">
            <tr>
                <td width="15%" class="bg-blue" style="vertical-align: middle;">OBSERVACIONES</td>
                <td width="85%" style="height: 40px; vertical-align: top; text-align: left;">{observaciones_generales}</td>
            </tr>
        </table>

        <table width="100%" border="0" cellpadding="0" cellspacing="0" style="margin-top: 25px;">
            <tr>
                <td width="31%">
                    <table width="100%" border="1" cellpadding="4" cellspacing="0">
                        <tr><td class="text-center" style="height: 20px; font-size: 7px; vertical-align: bottom; border-bottom: none;">{responsable} / JEFE TALLER</td></tr>
                        <tr><td class="text-center" style="font-weight: bold; font-size: 6px; border-top: 1px solid #000;">NOMBRE Y CARGO RESPONSABLE DE LA ORDEN DE PEDIDO</td></tr>
                    </table>
                </td>
                <td width="3%"></td>
                <td width="31%">
                    <table width="100%" border="1" cellpadding="4" cellspacing="0">
                        <tr><td class="text-center" style="height: 20px; font-size: 7px; vertical-align: bottom; border-bottom: none;">INGENIERO JULIO CARDENAS / GERENCIA</td></tr>
                        <tr><td class="text-center" style="font-weight: bold; font-size: 6px; border-top: 1px solid #000;">NOMBRE Y CARGO DE QUIEN RECIBE</td></tr>
                    </table>
                </td>
                <td width="3%"></td>
                <td width="32%">
                    <table width="100%" border="1" cellpadding="4" cellspacing="0">
                        <tr><td class="text-center" style="height: 20px; font-size: 7px; vertical-align: bottom; border-bottom: none;">INGENIERO JULIO CARDENAS / GERENCIA</td></tr>
                        <tr><td class="text-center" style="font-weight: bold; font-size: 6px; border-top: 1px solid #000;">NOMBRE Y CARGO DE RESPONSABLE DE APROBACIÓN</td></tr>
                    </table>
                </td>
            </tr>
        </table>

    </body>
    </html>
    """

    # Crear el PDF
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html_template.encode("UTF-8")), result)
    
    if not pdf.err:
        st.success("¡El documento calcado ha sido generado exitosamente!")
        st.download_button(
            label="Descargar Orden de Pedido",
            data=result.getvalue(),
            file_name=f"{num_pedido}.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Hubo un error al generar el PDF.")