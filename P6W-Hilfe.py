import streamlit as st
import pandas as pd
from pypdf import PdfReader, PdfWriter
from io import BytesIO

#felder = { "Name": f"{name}, {vorname}", "Geburtsdt" : ort }


def data_from_pdfs(files):
    # Find field names of all fields in all files
    keys = ['filename']
    for file in files:
        reader = PdfReader(file)
        loc = reader.get_fields()
        keys = list(set(keys + list(loc)))
    # Create a list of dicts. Each dict contains input from one file
    data = []
    for file in files:
        # Write filenames in first column
        loc_dict = {'filename' : file.name}  
        reader = PdfReader(file)
        loc_data = reader.get_fields()
        for key in loc_data:
            try:
                loc_dict.update({key : loc_data[key]['/V']})
            except:
                st.write(f"Problems with field {key} in file {file}.")        

        data.append(loc_dict)
    return data


# Check if a field in a pdf form is a Checkbox
def is_check_box(value):
    return "/_States_" in value

# Fill in pdf formfile with data from a dict
def write_pdfs(data, formfile):
    reader = PdfReader(formfile)
    fields = reader.get_fields()    

    # Reduce keys to the intersection of keys in data and fields in the formfile
    keys = data.keys().intersection(set(fields.keys()))
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
                if not str(data[key]).lower() in {"", "/off", "nein", "off", "false", "0"}:
                    state = [s for s in states if s != "/Off"][0]
                    try:
                        writer.update_page_form_field_values(writer.pages[i], {key: state}, auto_regenerate=False)
                    except:
                        st.write("Problems with field " + key)
            else:
                try:
                    writer.update_page_form_field_values(writer.pages[i], {key: data[key]})
                except:
                    st.write("Problems with text field " + key + ", value " + data[key])

    with BytesIO() as bytes_stream:
        writer.write(bytes_stream)

    filename = (pdf_path + "/" + row[name_by] + ".pdf")
    with open(filename, "wb") as output_stream:
        writer.write(output_stream)





st.header("Hilfe beim Ausfüllen des P6w")
st.write("Hier werden Bewerbungsformulare für Tutorate eingelesen, und einige Felder des P6w automatisch befüllt.")

with st.form("my-form-retriever", clear_on_submit=True):
    help = "Hier bitte die ausgefüllten pdf-Formulare der Tutoratsbewerbungen hochladen. Bitte gleichzeitig mehrere Formulare hochladen."
    uploaded_files = st.file_uploader("Upload ausgefüllter Bewerbungen", type=["pdf"], accept_multiple_files=True, key="pdf_files", help=help, on_change=None, args=None, kwargs=None)
    submitted = st.form_submit_button("Submit")

if submitted and uploaded_files != []:
    data = data_from_pdfs(uploaded_files)
    data = [ { key: value for key, value in d.items() if key in ["filename", "name", "vorname", "ort"]} for d in data]
    for d in data:
        d["weiterbeschaeftigung"] = True
df = pd.DataFrame.from_records(data)
df_new = st.data_editor(df, use_container_width = True, num_rows = "fixed")
data = df_new.to_dict('records')
st.write(data)