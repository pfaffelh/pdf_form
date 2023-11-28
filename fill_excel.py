from pypdf import PdfReader
import xlsxwriter
import os

formular_pdf = "forms_to_xls/formular-absolventinnenfeier.pdf"
pdf_path = "forms_to_xls/volle_pdfs/"

workbook = xlsxwriter.Workbook("forms_to_xls/absolventinnenfeier.xlsx")
worksheet = workbook.add_worksheet()

# Finde Namen der Pdf Dateien raus
files = [f for f in os.listdir(pdf_path) if os.path.isfile(os.path.join(pdf_path, f))]

# Namen der Textfelder herausfinden
reader = PdfReader(formular_pdf)
all_fields = reader.get_fields()    
text_fields = reader.get_form_text_fields()

# Spaltennamen im xls anlegen
for col, zeilenname in enumerate(text_fields):
    worksheet.write(0, col, zeilenname)

# Schreibe Daten zeilenweise in xls
for row, file in enumerate(files, start=1):
    # Öffne jede Zeile das nächste Pdf
    reader = PdfReader(pdf_path + file)

    for col, value in enumerate(text_fields):
        # Zwischenstand
        # Lies im pdf aus, was im Feld mit dem Namen "value" steht
        worksheet.write(row, col, value)

# xls anlegen
workbook.close()