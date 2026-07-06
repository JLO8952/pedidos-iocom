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
def get_image_base64():
    try:
        with open(path, "rb") as image_file:
            return "data:image/png;base64,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"
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
