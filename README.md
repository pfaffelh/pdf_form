### General

You just downloaded a small [repository](https://github.com/pfaffelh/pdf_form)  using
```
git clone https://github.com/pfaffelh/pdf_form
```
You probably need to call
```
pip install -r requirements.txt
```
in order to install some packages. You now have two new commands, which come with a small help:
```
python3 fill_excel.py -h
python3 fill_pdf.py -h
```
The first takes filled pdf forms and puts the data to an excel file. 
The second takes an excel file and fills an empty pdf form.

### Workflow:

#### 1) Use filled pdf forms for an excel file

We retrieve data from a pdf-form (example: `formular_bewerbungen_leer.pdf`). All data is stored in directory "input".
Using 
```
python3 fill_excel.py -o data_from_bewerbungen.xls -p input/*
```
we write a file `data_from_bewerbungen.xls`, which contains all data from the pdfs.

#### 2) Fill new pdf form with data

In order to use this data for yet another pdf_form (`p6w_leer.pdf` here), we first fill in this form for creating a template. This is `p6w_vorlage.pdf`. Once we have this template, use
```
python3 fill_excel.py -o data_for_einstellungen.xls -p p6w_vorlage.pdf
```
in order to obtain an excel-file with the corresponding field names. This Excel file can now be updated using data from `data_from_bewerbungen.xls`. (It is allowed to delete columns from this file.) Once this is done, use 
```
python3 fill_pdf.py p6w_leer.pdf -f data_for_einstellungen.xls -s Name
```
in order to fill the empty form, one file for each row in `data_for_einstellungen.xls`. Here, `-s Name` leads to filenames which are indicated by the column Name in `data_for_einstellungen.xls`.

