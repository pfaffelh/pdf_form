import streamlit as st
import os
import logging

logging.basicConfig(level=logging.DEBUG, filename = "pdf_form.log", filemode="a", format = "%(asctime)s - %(levelname)s - pdf_form - %(message)s")

def clear_tmp_output():
    for folder in ["tmp/", "output/"]:
        for filename in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, filename)):
                os.remove(os.path.join(folder, filename))


st.write("### Connecting your pdf-forms to Excel")

st.markdown("""
            Pdf forms are often a useful alternative for retrieving and submitting data. We provide here three functions for automating work with pdf forms:
            * In the _form-retriever_, you provide several filled pdf-forms. (It is most useful if this is the same pdf form filled with different data.) You receive an xls-file where every field of the form represents one column and which is filled with the values of the pdf-forms.
            * In the _field-name-form-filler_, you provide an empty pdf-form, and get back a pdf-form where all text fields a re filled with the field names.
            * In the _form-filler_, you provide an empty pdf-form together with an Excel-file, where the column names coincide with the field names of the pdf-form. You receive several filled pdf-forms, filled with the data from the xls-file.
            """)

st.write("---")
