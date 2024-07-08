import streamlit as st
import pandas as pd
from pypdf import PdfReader, PdfWriter
import os

# Dies ist ein dictionary mit key = name im Eingabeformular, value = name im Ausgabeformular
felder = {"filename": "filename",
          "name": "Nachname", 
          "vorname": "Vorname", 
          "strasse": "Adresse",
          "ort": "Ort", 
          "plz": "PLZ",
          "email": "Email",
          "gebdat": "Geburtsdatum", 
}

def clear_data():
    st.session_state.data = []

def setup_session_state():
    if "data" not in st.session_state:
        clear_data()

def clear_tmp_output():
    for folder in ["tmp/", "output/"]:
        for filename in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, filename)):
                os.remove(os.path.join(folder, filename))

def data_from_pdfs(files):
    data = []
    for file in files:
        # Write filenames in first column
        loc_dict = {'filename' : file.name}  
        reader = PdfReader(file)
        try:
            loc_data = reader.get_fields()
            for key in loc_data:
                loc_dict.update({key : loc_data[key]['/V']})
            data.append(loc_dict)
        except:
            st.write(f"Probleme mit Datei {file.name}.")
    return data

# Check if a field in a pdf form is a Checkbox
def is_check_box(value):
    return "/_States_" in value

# Fill in pdf formfile with data from a dict d
# output filenames are input filenames with P166
def write_pdf(d, formfile, pdf_path):
    reader = PdfReader(formfile)
    fields = reader.get_fields()    

    # Reduce keys to the intersection of keys in data and fields in the formfile
    keys = set(d.keys()).intersection(set(fields.keys()))
    fields = {key:value for key,value in fields.items() if key in keys}

    # Check Output-Pfad
    # Write one file for each row in the excel file.
    # Use column name_by for filenames.
    writer = PdfWriter()
    writer.append(reader)
    for i in range(len(reader.pages)):
        for key, field in fields.items():
            if is_check_box(fields[key]):
                states = field["/_States_"]
                if not str(d[key]).lower() in {"", "/off", "nein", "off", "false", "0"}:
                    state = [s for s in states if s != "/Off"][0]
                    try:
                        writer.update_page_form_field_values(writer.pages[i], {key: state}, auto_regenerate=False)
                    except:
                        st.write("Problems with field " + key)
            else:
                try:
                    writer.update_page_form_field_values(writer.pages[i], {key: d[key]})
                except:
                    st.write("Problems with text field " + key + ", value " + d[key])

    try:
        output_filename = f"{str.split(d['filename'], '.')[0]}_P166.pdf"
    except:
        output_filename = ".pdf"
    filename = (pdf_path + "/" + output_filename)
    with open(filename, "wb") as output_stream:
            writer.write(output_stream)
    
    filename = (f"{d['filename']}_P166.pdf")
    with open(filename, "wb") as output_stream:
        writer.write(output_stream)
    return output_stream

setup_session_state()
st.set_page_config(page_title="Hilfe beim Ausfüllen des P166", page_icon=None, layout="wide", menu_items=None)
st.header("Hilfe beim Ausfüllen des P166")
st.write("Hier werden Bewerbungsformulare für Tutorate eingelesen, und einige Felder des P166 automatisch befüllt.")

with st.form("my-form-retriever", clear_on_submit=True):
    help = "Hier bitte die ausgefüllten pdf-Formulare der Tutoratsbewerbungen hochladen. Am besten gleichzeitig mehrere Formulare hochladen."
    uploaded_files = st.file_uploader("Upload ausgefüllter Bewerbungen", type=["pdf"], accept_multiple_files=True, key="pdf_files", help=help, on_change=None, args=None, kwargs=None)
    submitted = st.form_submit_button("Submit")

if submitted:
    data = data_from_pdfs(uploaded_files)
    st.session_state.data = st.session_state.data + [ { felder[key]: d[key] for key in felder.keys()} for d in data]
if st.session_state.data != []:
    df = pd.DataFrame(st.session_state.data)
    df_new = st.data_editor(df, use_container_width = True, num_rows = "fixed")
    st.session_state.data = df_new.to_dict('records')
    clear_tmp_output()
    for d in st.session_state.data:
        write_pdf(d, 'static/P166_03_2024.pdf', 'output')

    os.system("cd output; tar czvf ../tmp/data.tgz *")
    col1, col2 = st.columns([1, 1])
    with col1:
        with open("tmp/data.tgz", "rb") as tgz_file:
            st.download_button(label="Download Formulare P166 mit ein paar ausgefüllten Zellen", data=tgz_file, file_name='data.tgz')
    with col2: 
        st.button("Alle Zellen löschen", on_click = clear_data)
