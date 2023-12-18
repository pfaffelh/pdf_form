import streamlit as st
import fill_pdf
import Pdf_form
import os

st.write("##### pdf _form-filler_")
st.write("Here, you can use data from an Excel-file in order to fill in pdf-forms. You must upload both, the Excel-file and an empty pdf-form.")

with st.form("my-form-filler", clear_on_submit=True):
    help = "Please upload empty pdf-form."
    uploaded_pdf_form = st.file_uploader("upload empty pdf-form", type=["pdf"],
                                          accept_multiple_files=False, key="empty_pdf_form", help=help, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    help = "Please upload xls or xlsx with data for the empty form."
    uploaded_xls = st.file_uploader("upload xls with data", type=["xls", "xlsx"], 
                                    accept_multiple_files=False, key="Excel file with data", help=help, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")    
    name_by = st.text_input("By which column from the Excel file should the pdfs be named?")
    submitted = st.form_submit_button("Submit")
if submitted and uploaded_pdf_form is not None and uploaded_xls is not None:
    Pdf_form.clear_tmp_output()
    with open("tmp/pdf_form.pdf","wb") as f:
        f.write(uploaded_pdf_form.getbuffer())
    with open("tmp/data.xls","wb") as f:
        f.write(uploaded_xls.getbuffer())
    if name_by != "":
        fill_pdf.write_pdfs("tmp/pdf_form.pdf", "tmp/data.xls", "output/", name_by)    
    else:
        fill_pdf.write_pdfs("tmp/pdf_form.pdf", "tmp/data.xls", "output/")    
    os.system("tar czvf tmp/data.tgz output/*")

    with open("tmp/data.tgz", "rb") as tgz_file:
        st.download_button(label="Download pdf files", data=tgz_file, file_name='data.tgz')

