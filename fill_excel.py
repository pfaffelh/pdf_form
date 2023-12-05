from pypdf import PdfReader
import xlsxwriter
import os
import sys

def write_excel(excel_file, pdf_path, pdf_files):
    workbook = xlsxwriter.Workbook(excel_file)
    worksheet = workbook.add_worksheet()

    # Finde Namen der Textfelder
    reader = PdfReader(os.path.join(pdf_path, pdf_files[0]))
    text_fields = reader.get_form_text_fields()

    # Schreibe Spaltennamen in xls
    for col, zeilenname in enumerate(text_fields):
        worksheet.write(0, col, zeilenname)

    # Schreibe Daten zeilenweise in xls
    for row, file in enumerate(pdf_files, start=1):

        # Öffne jede Zeile das nächste Pdf und lies den Inhalt aus
        reader = PdfReader(os.path.join(pdf_path, file)) 
        data = reader.get_form_text_fields()

        for col, value in enumerate(data):
            worksheet.write(row, col, data[value])

    workbook.close()


if __name__ == "__main__":

    # Optionen:
    # -o
    # Es gibt einen separaten Ordner, in dem alle Pdfs dem gleichen Formular entstammen
    # und bearbeitet werden sollen
    #
    # -p
    # Es geht nur um vereinzelte Pdfs, die im gleichen Ordner liegen wie das Python Skript.
    # Ihre Namen müssen hinter dem -p mitgegeben werden, egal viele.

    instructions = f"""
    Benutzung: python {sys.argv[0]} <excel_filename> -o <path_to_folder>
    Alternative: python {sys.argv[0]} <excel_filename> -p <pdf_file_1> <pdf_file_2> ...
    """

    # Shell Argumente parsen
    if len(sys.argv) < 4:
        print(instructions)
        sys.exit()

    excel_file = sys.argv[1]

    if sys.argv[2] == "-o":
        pdf_path = sys.argv[3]
        pdf_files = [f for f in os.listdir(pdf_path) if os.path.isfile(os.path.join(pdf_path, f))]
    elif sys.argv[2] == "-p":
        pdf_path = ""
        pdf_files = sys.argv[3:]
    else:
        print(instructions)
        sys.exit()

    # Schreibe xls
    write_excel(excel_file, pdf_path, pdf_files)
    print("Datei '%s' geschrieben." % excel_file)