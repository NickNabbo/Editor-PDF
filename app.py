import streamlit as st
import fitz  # È il nome tecnico della libreria PyMuPDF
import io

st.set_page_config(page_title="Censura PDF", page_icon="🕵️‍♂️")
st.title("Oscura Testo nei PDF")
st.write("Cerca una parola nel documento e coprila con un rettangolo nero in modo permanente.")

uploaded_file = st.file_uploader("Carica il tuo PDF", type="pdf")
parola_da_cercare = st.text_input("Quale parola vuoi oscurare?")

if uploaded_file and parola_da_cercare:
    if st.button("Applica Modifiche"):
        # 1. Legge il file caricato
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        
        # 2. Scansiona le pagine
        for pagina in doc:
            # Trova le coordinate della parola
            aree_trovate = pagina.search_for(parola_da_cercare)
            for area in aree_trovate:
                # Disegna un rettangolo nero (0,0,0) sulle coordinate
                pagina.add_redact_annot(area, fill=(0, 0, 0))
            
            # Applica la censura alla pagina
            pagina.apply_redactions()
        
        # 3. Salva il nuovo documento in memoria
        pdf_bytes = doc.write()
        
        st.success("Elaborazione completata!")
        st.download_button(
            label="📥 Scarica PDF Modificato",
            data=pdf_bytes,
            file_name="pdf_oscurato.pdf",
            mime="application/pdf"
        )
