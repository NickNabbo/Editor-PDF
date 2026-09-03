import streamlit as st
from pypdf import PdfReader
from fpdf import FPDF

st.set_page_config(page_title="Editor PDF Libero", page_icon="📝")
st.title("Modifica il testo del tuo PDF")

# 1. Caricamento del file
uploaded_file = st.file_uploader("Carica il tuo file PDF", type="pdf")

if uploaded_file is not None:
    # 2. Estrazione del testo dal PDF
    reader = PdfReader(uploaded_file)
    testo_originale = ""
    for page in reader.pages:
        estratto = page.extract_text()
        if estratto:
            testo_originale += estratto + "\n"
    
    st.info("Testo estratto con successo! Modificalo nel riquadro sottostante.")
    
    # 3. L'Editor dove puoi modificare liberamente le parole
    testo_modificato = st.text_area("Testo del documento", value=testo_originale, height=400)

    # 4. Creazione e salvataggio del nuovo PDF
    if st.button("Genera il nuovo PDF aggiornato"):
        
        # --- NUOVA FASE: PULIZIA DEL TESTO ---
        # Sostituiamo i caratteri speciali tipografici con quelli standard
        testo_pulito = testo_modificato.replace('’', "'").replace('‘', "'")
        testo_pulito = testo_pulito.replace('“', '"').replace('”', '"')
        testo_pulito = testo_pulito.replace('–', '-').replace('—', '-')
        testo_pulito = testo_pulito.replace('•', '-')
        
        # Forziamo la codifica per ignorare eventuali altri simboli strani (es. emoji)
        # Sostituirà i caratteri non supportati con un "?" per evitare il crash
        testo_sicuro = testo_pulito.encode('windows-1252', 'replace').decode('windows-1252')
        # -------------------------------------

        # Usiamo FPDF per creare il nuovo documento
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", size=11)
        
        # Inseriamo il testo "sicuro"
        pdf.multi_cell(0, 5, text=testo_sicuro)
        
        st.success("Il tuo nuovo PDF è pronto!")
        
        # Pulsante di download
        st.download_button(
            label="📥 Scarica PDF Modificato",
            data=bytes(pdf.output()),
            file_name="nuovo_documento.pdf",
            mime="application/pdf"
        )
