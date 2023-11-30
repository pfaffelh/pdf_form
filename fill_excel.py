from pypdf import PdfReader
import xlsxwriter
import os

formular_pdf = "forms_to_xls/formular-absolventinnenfeier.pdf"
pdf_path = "forms_to_xls/volle_pdfs/"

workbook = xlsxwriter.Workbook("forms_to_xls/absolventinnenfeier.xlsx")
worksheet = workbook.add_worksheet()

# Finde Namen der Pdf Dateien
files = [f for f in os.listdir(pdf_path) if os.path.isfile(os.path.join(pdf_path, f))]

# Finde Namen der Textfelder
reader = PdfReader(formular_pdf)  
text_fields = reader.get_form_text_fields()

# Schreibe Spaltennamen in xls
for col, zeilenname in enumerate(text_fields):
    worksheet.write(0, col, zeilenname)

# Schreibe Daten zeilenweise in xls
for row, file in enumerate(files, start=1):

    # Öffne jede Zeile das nächste Pdf und lies den Inhalt aus
    reader = PdfReader(pdf_path + file)
    data = reader.get_form_text_fields()

    for col, value in enumerate(data):
        worksheet.write(row, col, data[value])

workbook.close()