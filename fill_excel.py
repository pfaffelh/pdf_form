import argparse, os, sys
from pathlib import Path
from pypdf import PdfReader
import pandas as pd

# Read pdf-forms from filelist and put field contents in an excel file
def df_from_pdfs(pdf_files):

    # Find field names of all fields in all files
    keys = ['input_filename']
    for file in pdf_files:
        if not Path(file).exists():
            print(file + " does not exist. Exiting...")
            sys.exit()
        reader = PdfReader(file)
        loc = reader.get_fields()
        keys = list(set(keys + list(loc)))
    
    # Create a list of dicts. Each dict contains input from one file
    data = []
    for file in pdf_files:
        # Write filenames in first column
        loc_dict = {'input_filename' : file}        
        reader = PdfReader(file)
        loc_data = reader.get_fields()
        for key in loc_data:
            try:
                loc_dict.update({key : loc_data[key]['/V']})
            except:
                print("Problems with field " + key + " in field " + file + ".")        

        data.append(loc_dict)
    df = pd.DataFrame.from_records(data)
    return df

if __name__ == "__main__":

    # excel_filename: the name of the path to excel file where the data should be stored
    # pdf_files: list of pdfs which contain the data

    parser = argparse.ArgumentParser(description='Write input from filles pdf-forms into an excel file.')
    parser.add_argument('-o', '--excel_filename', required = True,
                     help='The xls-file which is to be filled.')
    parser.add_argument('-p', '--pdf_files', required = True, nargs='+',
                     help='The list of pdf-files which store the information which is to be saved in the Excel file')
    parser.add_argument('-f', '--force', nargs='?', const='c',
                     default='d', help='Force overwriting existing files.')
    args = parser.parse_args()

    if Path(args.excel_filename).exists() and args.force=='d':
        print(args.excel_filename + " already exists. Exiting...")
        sys.exit()
    for file in args.pdf_files:
        if not Path(file).exists():
            print(file + " does not exist. Exiting...")
            sys.exit()

    # Write excel file
    df = df_from_pdfs(args.pdf_files)
    df.to_excel(args.excel_filename, index=False, engine="xlsxwriter")
    print("Written " + args.excel_filename + ".")
    
