import streamlit as st
import fill_excel
import Pdf_form
import os

st.write("##### pdf _form-retriever_")
st.write("Here, you can use data from one or several filled pdf-forms. The result is an Excel-file with the information from the pdf forms.")

with st.form("my-form-retriever", clear_on_submit=True):
    help = "Please choose filled pdf-forms. This will result in an Excel file with the stored data."
    uploaded_pdf_files = st.file_uploader("upload filled pdf-forms", type=["pdf"], accept_multiple_files=True, key="pdf_files", help=help, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    submitted = st.form_submit_button("Submit")
if submitted and uploaded_pdf_files != []:
    Pdf_form.clear_tmp_output()
    for file in uploaded_pdf_files:
        with open(os.path.join("tmp/",file.name),"wb") as f:
            f.write(file.getbuffer())
    df = fill_excel.df_from_pdfs(["tmp/" + x.name for x in uploaded_pdf_files])
    df.to_excel("tmp/data_from_pdfs.xls", index=False, engine="xlsxwriter")
    with open("tmp/data_from_pdfs.xls", "rb") as xls_file:
        st.download_button(label="Download xls file", data=xls_file, file_name='data_from_pdfs.xls')

