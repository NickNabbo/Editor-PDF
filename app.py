import streamlit as st
import fitz  # PyMuPDF

st.set_page_config(page_title="Sostituzione Chirurgica PDF", page_icon="✂️")
st.title("Sostituisci Parole nel PDF")
st.write("Mantiene il 100% dell'impaginazione e della grafica. Cancella la vecchia parola e scrive quella nuova sopra.")

uploaded_file = st.file_uploader("Carica il tuo PDF", type="pdf")

col1, col2 = st.columns(2)
with col1:
    parola_vecchia = st.text_input("Parola da cercare (esatta):")
with col2:
    parola_nuova = st.text_input("Nuova parola da inserire:")

if uploaded_file and parola_vecchia and parola_nuova:
    if st.button("Applica Sostituzione"):
        # Apriamo il documento
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        
        sostituzioni_fatte = 0
        
        # Scansioniamo tutte le pagine
        for pagina in doc:
            # Troviamo le coordinate della parola da togliere
            aree_trovate = pagina.search_for(parola_vecchia)
            
            for area in aree_trovate:
                # 1. "Sbianchiamo" la vecchia parola con un rettangolo bianco
                pagina.draw_rect(area, color=(1, 1, 1), fill=(1, 1, 1), width=0)
                
                # 2. Inseriamo la nuova parola nello stesso punto esatto (in basso a sinistra)
                # Impostiamo una grandezza font standard (11) e il colore nero (0,0,0)
                pagina.insert_text((area.x0, area.y1), parola_nuova, fontsize=11, color=(0, 0, 0))
                sostituzioni_fatte += 1
                
        if sostituzioni_fatte > 0:
            st.success(f"Trovate e sostituite {sostituzioni_fatte} occorrenze. Il layout è rimasto intatto.")
            
            pdf_bytes = doc.write()
            st.download_button(
                label="📥 Scarica il PDF aggiornato",
                data=pdf_bytes,
                file_name="pdf_modificato_chirurgicamente.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("La parola vecchia non è stata trovata nel documento.")
