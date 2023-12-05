from pypdf import PdfReader, PdfWriter
import pandas as pd
import sys
import os

def write_pdfs(pdf_form, excel_file, pdf_path, name_by):

    # Lies leeres Formular
    reader = PdfReader(pdf_form)
    text_fields = reader.get_form_text_fields()

    # Lies ausgefülltes xls in einen dataframe ein
    df = pd.read_excel(excel_file)
    df.fillna("", inplace=True)  # fülle missing values mit leerem String

    for index, row in df.iterrows():
        writer = PdfWriter()
        writer.append(reader)
        for i in range(len(reader.pages)):
            for field in text_fields:
                try:
                    writer.update_page_form_field_values(writer.pages[i], {field: row[field]})
                except:
                    print("Problems with field " + field)
            # set_need_appearances_writer
            # write "output" to pypdf-output.pdf
        filename = row[name_by] + ".pdf"
        with open(os.path.join(pdf_path, filename), "wb") as output_stream:
            writer.write(output_stream)
        print("Datei " + filename + " geschrieben.")

if __name__ == "__main__":

    # pdf_form : Pfad zum Formular, das ausgefüllt werden soll
    # excel_filename: Pfad zur ausgefüllten Excel Datei
    # path_to_folder: Pfad zum Ordner, in dem die ausgefüllten Pdfs gespeichert werden sollen
    # name_by: Feld des Formulars, nach dem die Pdf Dateien benannt werden sollen

    instructions = f"""
    Benutzung: python {sys.argv[0]} <pdf_form> <excel_filename> <path_to_folder> <name_by>
    """

    # Shell Argumente parsen
    if len(sys.argv) < 5:
        print(instructions)
        sys.exit()

    pdf_form = sys.argv[1]
    excel_file = sys.argv[2]  # hier liegts
    pdf_path = sys.argv[3]  # hier solls rein
    name_by = sys.argv[4]

    # Schreibe pdfs
    write_pdfs(pdf_form, excel_file, pdf_path, name_by)