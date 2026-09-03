import streamlit as st
from pdf2docx import Converter
import tempfile
import os

st.set_page_config(page_title="Convertitore PDF-Word", page_icon="🔄")
st.title("Converti per Modificare")
st.write("Questo strumento trasforma il tuo PDF in un file Word mantenendo grafica, immagini e layout. Potrai modificare il testo comodamente e poi risalvarlo in PDF.")

# Caricamento del file
uploaded_file = st.file_uploader("Carica il tuo file PDF", type="pdf")

if uploaded_file is not None:
    if st.button("Converti in formato Word"):
        with st.spinner("Conversione in corso... (mantenimento layout e immagini)"):
            
            # Salviamo il PDF caricato in un file temporaneo di sistema
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(uploaded_file.getvalue())
                pdf_path = temp_pdf.name
            
            # Prepariamo il percorso per il file Word in uscita
            docx_path = pdf_path.replace(".pdf", ".docx")
            
            try:
                # Eseguiamo la conversione complessa
                cv = Converter(pdf_path)
                cv.convert(docx_path)
                cv.close()
                
                # Rendiamo disponibile il download
                with open(docx_path, "rb") as docx_file:
                    st.success("Conversione completata con successo!")
                    st.download_button(
                        label="📥 Scarica il documento Word",
                        data=docx_file,
                        file_name="documento_modificabile.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            except Exception as e:
                st.error(f"Si è verificato un errore durante la conversione: {e}")
            finally:
                # Pulizia della memoria
                if os.path.exists(pdf_path): os.remove(pdf_path)
                if os.path.exists(docx_path): os.remove(docx_path)
