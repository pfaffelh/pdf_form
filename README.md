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

#### 1) Create excel file from filled pdf form(s)

Use
```
python3 fill_excel.py -o data_from_bewerbungen.xlsx -p path/*.pdf
```
to create a file `data_from_bewerbungen.xlsx` that contains data from all pdfs at the specified path `path/*.pdf`.
Alternatively list the pdf files you want to read:
```
python3 fill_excel.py -o data_from_bewerbungen.xlsx -p file1.pdf file2.pdf file3.pdf
```

#### 2) Create pdf file(s) from filled excel file

Use
```
python3 fill_pdf.py p6w_leer.pdf -f data_for_einstellungen.xlsx -o Ordner -s Name
```
to fill out the empty form `p6w_leer.pdf` with data from the excel file `data_for_einstellungen.xlsx`. The Option `-o` indicates the folder name `Ordner` where the pdf files will be created. The pdf files will be named after the field name given by the Option `-s`.