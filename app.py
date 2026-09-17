import sys
import subprocess

# Asegurar instalación de fpdf2 en tiempo de ejecución
try:
    from fpdf import FPDF
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf2"])
    from fpdf import FPDF

import streamlit as st
from datetime import datetime

# ------------------------------------------------------------------
# Configuración de página
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Sistema de Documentos Oficiales - Chubut",
    page_icon="🏛️",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-family: 'Verdana', sans-serif;
        color: #003366;
        text-align: center;
        margin-bottom: 20px;
    }
    .status-badge {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ffeeba;
        font-family: 'Verdana', sans-serif;
        font-size: 0.9em;
        margin-bottom: 20px;
    }
    .doc-preview-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 40px;
        border-radius: 4px;
        font-family: 'Verdana', sans-serif;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        min-height: 500px;
        position: relative;
    }
    .doc-top-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 20px;
    }
    .doc-header-code {
        font-weight: bold;
        font-size: 1.1em;
        color: #2c3e50;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .doc-date {
        text-align: right;
        font-size: 1.0em;
        margin-bottom: 10px;
    }
    .doc-ref {
        text-align: right;
        font-size: 0.95em;
        font-style: italic;
        color: #444;
        margin-bottom: 15px;
    }
    .doc-field-row {
        display: flex;
        justify-content: space-between;
        gap: 40px;
        margin-bottom: 15px;
        font-size: 0.95em;
    }
    .doc-motivo {
        font-weight: bold;
        margin-bottom: 15px;
    }
    .doc-body {
        text-align: justify;
        font-size: 1.0em;
        line-height: 1.6;
        margin-top: 25px;
        margin-bottom: 80px;
        white-space: pre-wrap;
    }
    .doc-footer {
        position: absolute;
        bottom: 20px;
        right: 40px;
        font-weight: bold;
        font-size: 1.0em;
        color: #444;
    }
    .doc-firma {
        margin-top: 60px;
        text-align: center;
        font-size: 0.95em;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏛️ Generador de Documentación Administrativa")
st.caption("Organismo: DPA-SsFyCP-MP | Gobierno del Chubut")

st.markdown("""
<div class="status-badge">
    🟡 <b>Formato configurado internamente — pendiente de validación oficial</b><br>
    <i>Tipografía oficial: Verdana (10–12pt) | Redacción basada en normativa vigente.</i>
</div>
""", unsafe_allow_html=True)

meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
         "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
now = datetime.now()
default_date_str = f"Rw, {now.day} de {meses[now.month - 1]} de {now.year}."

# ------------------------------------------------------------------
# Layout de dos columnas
# ------------------------------------------------------------------
col_input, col_preview = st.columns([1, 1])

with col_input:
    st.subheader("📋 Datos del Trámite")

    doc_type = st.selectbox(
        "Tipo de Documento",
        ["Nota", "Memorándum", "Pase"]
    )

    doc_num = st.text_input("Número Correlativo", value="001/2026")
    fecha_custom = st.text_input("Lugar y Fecha", value=default_date_str)

    # --- Campos condicionales según tipo de documento ---
    destinatario = ""
    referencia = ""
    producido_por = ""
    dirigido_a = ""
    motivo = ""
    firmante = ""
    dni = ""

    if doc_type == "Nota":
        st.markdown("**Campos propios de Nota** (externa / interdepartamental)")
        destinatario = st.text_area(
            "Destinatario / Organismo",
            value="Al Sr. Director Provincial de Administración\nS / D",
            height=80
        )
        referencia = st.text_input("Referencia (Expte. N° / Actuación)", value="Expte. N° 000-2026")
        asunto = st.text_input("Asunto", value="Solicitud de informe técnico")
        contenido_instruccion = st.text_area(
            "Contenido (solicitud o información a elevar)",
            value="Por medio de la presente, me dirijo a usted a fin de solicitar tenga bien disponer la "
                  "elaboración del informe técnico relativo a las actuaciones del expediente en trámite. "
                  "Sin otro particular, saludo a usted muy atentamente.",
            height=200
        )
        firmante = st.text_input("Firma - Nombre y Apellido", value="")
        dni = st.text_input("Firma - DNI", value="")

    elif doc_type == "Memorándum":
        st.markdown("**Campos propios de Memorándum** (exclusivamente interno)")
        producido_por = st.text_input("Producido por", value="Dirección de Promoción de Inversiones")
        dirigido_a = st.text_input("Dirigido a", value="")
        motivo = st.text_input("Motivo", value="")
        asunto = motivo
        contenido_instruccion = st.text_area(
            "Contenido (aviso, coordinación o directiva)",
            value="Se informa que a partir de la fecha...",
            height=200
        )

    else:  # Pase
        st.markdown("**Campos propios de Pase** (interno del expediente, sin referencia formal)")
        motivo = st.text_input("Motivo / Trámite a proseguir", value="")
        asunto = motivo
        contenido_instruccion = st.text_area(
            "Contenido (breve, normativo)",
            value="Pase a la oficina que corresponda a fin de proseguir el trámite.",
            height=150
        )

    st.button("🔄 Actualizar Vista Previa", use_container_width=True)

# ------------------------------------------------------------------
# Vista previa y exportación
# ------------------------------------------------------------------
with col_preview:
    st.subheader("📄 Vista Previa del Documento")

    header_code = f"{doc_type.upper()} N.º {doc_num} — DPA-SsFyCP-MP"

    # --- Armado del bloque HTML según tipo ---
    if doc_type == "Nota":
        campos_html = f"""
            <div class="doc-date">{fecha_custom}</div>
            <div class="doc-ref">Ref.: {referencia}</div>
            <div class="doc-header-code">{header_code}</div>
            <div style="font-weight:bold; margin-bottom: 15px;">ASUNTO: {asunto}</div>
            <div style="margin-bottom:15px; font-style:italic;">{destinatario.replace(chr(10), '<br>')}</div>
        """
        firma_html = f"""
            <div class="doc-firma">
                ____________________________<br>
                {firmante or '(Nombre y Apellido)'}<br>
                DNI: {dni or '(DNI)'}
            </div>
        """
    elif doc_type == "Memorándum":
        campos_html = f"""
            <div class="doc-date">{fecha_custom}</div>
            <div class="doc-header-code">{header_code}</div>
            <div class="doc-field-row">
                <div><b>Producido por:</b> {producido_por}</div>
                <div><b>Dirigido a:</b> {dirigido_a}</div>
            </div>
            <div class="doc-motivo">MOTIVO: {motivo}</div>
        """
        firma_html = ""
    else:  # Pase
        campos_html = f"""
            <div class="doc-date">{fecha_custom}</div>
            <div class="doc-header-code">{header_code}</div>
            <div class="doc-motivo">MOTIVO: {motivo}</div>
        """
        firma_html = ""

    st.markdown(f"""
    <div class="doc-preview-card">
        <div style="text-align: center; border-bottom: 2px solid #003366; padding-bottom: 10px; margin-bottom: 20px;">
            <h3 style="margin:0; color:#003366; font-family:'Verdana';">GOBIERNO DEL CHUBUT</h3>
            <small style="color:#666;">Ministerio de Producción — DPA-SsFyCP-MP</small>
        </div>
        {campos_html}
        <div class="doc-body">{contenido_instruccion}</div>
        {firma_html}
        <div class="doc-footer">L.I.A.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Generador de PDF
    # ------------------------------------------------------------------
    def clean_text(txt):
        if not txt:
            return ""
        txt = txt.replace("—", "-").replace("º", "°")
        return txt.encode('latin-1', 'replace').decode('latin-1')

    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 8, clean_text("GOBIERNO DEL CHUBUT"), ln=True, align="C")

        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 5, clean_text("Ministerio de Producción - DPA-SsFyCP-MP"), ln=True, align="C")
        pdf.line(10, 25, 200, 25)
        pdf.ln(10)

        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, clean_text(fecha_custom), ln=True, align="R")

        if doc_type == "Nota":
            pdf.set_font("Helvetica", "I", 10)
            pdf.cell(0, 6, clean_text(f"Ref.: {referencia}"), ln=True, align="R")
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, clean_text(header_code), ln=True, align="L")
            pdf.cell(0, 8, clean_text(f"ASUNTO: {asunto}"), ln=True, align="L")
            pdf.ln(3)
            pdf.set_font("Helvetica", "I", 10)
            pdf.multi_cell(0, 6, clean_text(destinatario))
            pdf.ln(5)
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 7, clean_text(contenido_instruccion), align="J")
            pdf.ln(15)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 6, clean_text("____________________________"), ln=True, align="C")
            pdf.cell(0, 6, clean_text(firmante or "(Nombre y Apellido)"), ln=True, align="C")
            pdf.cell(0, 6, clean_text(f"DNI: {dni or '(DNI)'}"), ln=True, align="C")

        elif doc_type == "Memorándum":
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, clean_text(header_code), ln=True, align="L")
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 7, clean_text(f"Producido por: {producido_por}"), ln=True, align="L")
            pdf.cell(0, 7, clean_text(f"Dirigido a: {dirigido_a}"), ln=True, align="L")
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 7, clean_text(f"MOTIVO: {motivo}"), ln=True, align="L")
            pdf.ln(5)
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 7, clean_text(contenido_instruccion), align="J")

        else:  # Pase
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, clean_text(header_code), ln=True, align="L")
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 7, clean_text(f"MOTIVO: {motivo}"), ln=True, align="L")
            pdf.ln(5)
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 7, clean_text(contenido_instruccion), align="J")

        pdf.set_y(-30)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 10, clean_text("L.I.A."), align="R", ln=True)

        return pdf.output()

    pdf_bytes = generate_pdf()

    st.download_button(
        label="📥 Descargar Documento en PDF",
        data=bytes(pdf_bytes),
        file_name=f"{doc_type}_{doc_num.replace('/', '-')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
