import streamlit as st
import fill_excel
import fill_pdf
import Pdf_form
import os

st.write("##### pdf _field-name-form-filler_")
st.write("Here, you can upload an empty pdf form, and retrieve a filled pdf form. The text fields are filled with the names of the fields.")
with st.form("my-empty-form-filler", clear_on_submit=True):
    help = "Please upload empty pdf-form."
    uploaded_pdf_form = st.file_uploader("upload empty pdf-form", type=["pdf"],
                                          accept_multiple_files=False, key="empty_pdf_form_to_fill", help=help, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    submitted = st.form_submit_button("Submit")
if submitted and uploaded_pdf_form is not None:
    Pdf_form.clear_tmp_output()
    with open("tmp/pdf_form.pdf","wb") as f:
        f.write(uploaded_pdf_form.getbuffer())
    fill_pdf.write_pdf_form_with_field_names("tmp/pdf_form.pdf", "tmp/filled_pdf_form.pdf")
    with open("tmp/filled_pdf_form.pdf", "rb") as pdf_file:
        st.download_button(label="Download filled pdf form", data=pdf_file, file_name='filled_pdf_form.pdf')
