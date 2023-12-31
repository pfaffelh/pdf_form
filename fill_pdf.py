import argparse, sys, os
import pandas as pd
from pathlib import Path
from pypdf import PdfReader, PdfWriter
import logging

# Fill in field names in an empty pdf form
def write_pdf_form_with_field_names(filename_pdf_empty, filename_pdf_filled):
    logging.info("Enter write_pdf_form_with_field_names(" + filename_pdf_empty + ", " + filename_pdf_filled + ")")
    reader = PdfReader(filename_pdf_empty)
    writer = PdfWriter()
    text_fields = reader.get_form_text_fields()

    writer.append(reader)
    for i in range(len(reader.pages)):
        for key in text_fields:
            writer.update_page_form_field_values(
                writer.pages[i], {key: key}
            )    
    with open(filename_pdf_filled, "wb") as output_stream:
        writer.write(output_stream)
    logging.info("File " + filename_pdf_filled + " written." )

# Check if a field in a pdf form is a Checkbox
def is_check_box(value):
    return "/_States_" in value

# Fill in pdf form with data from an excel file
# output will be stored in pdf_path, and named by name_by-column of the excel file
def write_pdfs(pdf_form, excel_file, pdf_path, name_by = None):
    logging.info("Enter write_pdfs(" + pdf_form + ", " + excel_file + ", " + pdf_path + ", " + str(name_by) + ")")
    # Read xls in a data frame
    path_to_excel = Path(excel_file)
    if not path_to_excel.exists():
        text = excel_file + " does not exist. Exiting..."
        logging.error(text)
        raise FileNotFoundError(text)
    df = pd.read_excel(excel_file)
    # fill missing values by an empty string
    df.fillna("", inplace=True)  

    # Read empty form
    if not Path(pdf_form).exists():
        text = pdf_form + " does not exist. Exiting..."
        logging.error(text)
        raise FileNotFoundError(text)
    reader = PdfReader(pdf_form)
    fields = reader.get_fields()    

    # Reduce fields to the column names of the xls-file
    keys = list(set(list(df.columns)).intersection(set(fields.keys())))
    fields = {key:value for key,value in fields.items() if key in keys}

    # Check Output-Pfad
    if not Path(pdf_path).is_dir():
        text = pdf_path + " is not a directory. Exiting..."
        logging.error(pdf_path + " is not a directory. Exiting...")
        raise NotADirectoryError(text)

    logging.info("Write pdfs in " + pdf_path)

    # Write one file for each row in the excel file.
    # Use column name_by for filenames.
    if (not name_by == None) and (not name_by in df.columns):
        text = name_by + " is not a column name in " + excel_file + ". Exiting..."
        logging.error(text)
        raise Exception(text)
    for index, row in df.iterrows():
        writer = PdfWriter()
        writer.append(reader)
        for i in range(len(reader.pages)):
            for key, field in fields.items():
                if is_check_box(fields[key]):
                    states = field["/_States_"]
                    if not str(row[key]).lower() in {"", "/off", "nein", "off", "false", "0"}:
                        state = [s for s in states if s != "/Off"][0]
                        try:
                            writer.update_page_form_field_values(writer.pages[i], {key: state}, auto_regenerate=False)
                        except:
                            logging.warning("Problems with field " + key)
                else:
                    try:
                        writer.update_page_form_field_values(writer.pages[i], {key: row[key]})
                    except:
                        logging.warning("Problems with text field " + key + ", value " + row[key])

        if name_by == None:
            filename = (pdf_path + "/" + str(index + 1) + ".pdf")
        else:
            filename = (pdf_path + "/" + row[name_by] + ".pdf")
        if Path(filename).exists() and args.force=='d':
            logging.warning(filename + " already exists. Continuing...")
        else:
            with open(filename, "wb") as output_stream:
                writer.write(output_stream)
                logging.info(filename + " written.")

if __name__ == "__main__":

    # pdf_form : path to form which needs to be filled
    # excel_filename: path to excel file for data
    # path_to_folder: path to output folder for filled pdfs
    # name_by: None, or the field of the form for filenames

    logging.basicConfig(level=logging.DEBUG, format = "%(asctime)s - %(levelname)s - %(message)s")

    # Get arguments from command line, creating the help at the same time.
    parser = argparse.ArgumentParser(description='Fill in pdf forms from an xls-file.')
    parser.add_argument('pdf_form',
                     help='The empty pdf form.')
    parser.add_argument('-i', '--excel_filename', required = True,
                     help='The input Excel file for the data used to fill out the forms. Column names must match keys for the fields.  If no xls-file is given, only field names are filled into the form.')
    parser.add_argument('-o', '--output', required = True,
                     help='The output folder for the filled pdfs.')
    parser.add_argument('-s', '--name_by', default = None,
                     help='Filled pdf files will be named after field name_by.')
    parser.add_argument('-f', '--force', nargs='?', const='c',
                     default='d', help='Force overwriting existing files.')
    args = parser.parse_args()

    # check output path
    path_to_output = Path(args.output)
    if not path_to_output.exists():
        text = args.output + " is not a directory. Exiting..."
        logging.error(text)
        raise NotADirectoryError(text)

    if args.excel_filename == None:
        write_pdf_form_with_field_names(args.pdf_form, args.output + "/" + "filled_form.pdf")
    else:
        write_pdfs(args.pdf_form, args.excel_filename, args.output, args.name_by)



