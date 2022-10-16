'''
Takes in a paystub pdf file. 
Writes a .txt copy of the pdf.
Extracts and writes the following data to .csv:

Date (first day of pay period)
Gross Pay
Income Tax (federal)
Medicare Tax
Social Security Tax
Other deductions, such as:
    insurance premiums
    401k contribution amounts
'''

import pandas as pd
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
from pathlib import Path

def main(delete_txts=True):

    # establish empty dataframe for storing data
    df = pd.DataFrame()

    # cycle through all pdf files in the directory
    for pdf_file in Path('pdfs').iterdir():
        # create a text file with the same name as the pdf
        txt_file = pdf_file.stem + '.txt'
        # dump all text from pdf into text file
        pdf_to_text(pdf_file, txt_file)

        # extract the pertinent data from the text file
        dct = {}
        with open(txt_file, 'r') as file:
            dct.update(get_date(file))
        with open(txt_file, 'r') as file:
            dct.update(get_gross_pay(file))
        with open(txt_file, 'r') as file:
            dct.update(get_other_values(file))
        # append to the dataframe
        df = df.append(dct, ignore_index=True)
        # write to csv
        df.to_csv('data/pay.csv', index=False)

        # get rid of text files
        if delete_txts:
            delete_txt_files()

def pdf_to_text(pdf_file, txt_file):
    i_f = open(pdf_file,'rb')
    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr,retData, laparams= LAParams())
    interpreter = PDFPageInterpreter(resMgr,TxtConverter)
    for page in PDFPage.get_pages(i_f):
        interpreter.process_page(page)
 
    text = retData.getvalue()
    with open(txt_file, 'w') as f:
        f.write(text)

def get_date(file):

    lines = file.readlines()
    # find the line that says "Pay Date"
    idx = lines.index('Pay Date:\n')
    # grab the date from two lines down 
    date = lines[idx+2].strip()

    return {'date': date}

def get_gross_pay(file):

    lines = file.readlines()
    # get first line that says 'Gross Pay'
    for i in range(len(lines)):
        if 'Gross Pay' in lines[i]:
            lines = lines[i:]
            # find the next line that says 'this period'
            for j in range(len(lines)):
                if 'this period' in lines[j]:
                    # get the gross pay number from the next line
                    gross_pay = lines[j+1]
                    break
            break
    # format the gross pay number
    gross_pay = float(gross_pay.strip().replace(' ', '')) / 100

    return {'gross_pay': gross_pay}

def get_other_values(file):

    # skip these lines which are irrelevant
    lines_to_skip = ['\n', 'Statutory\n', 'Federal\n', 'Net Pay\n', 
                     'Checking 1\n', 'Net Check\n']
    # to store labels
    list1 = []
    # to store values
    list2 = []

    lines = file.readlines()

    # find the first line containing the word 'Statutory'
    idx = lines.index('Statutory\n')
    # iterate through all lines after that
    lines = lines[idx:]
    for i in range(len(lines)):
        if lines[i] not in lines_to_skip:
            # get the labels
            if not lines[i].startswith('-'):
                if len(list2) == 0:
                    list1.append(lines[i])
            # get the values
            else:
                if len(list2) < len(list1):
                    list2.append(lines[i])

    # format labels
    list1 = [label.strip().lower().replace(' ', '_') for label in list1]
    # format values
    list2 = [abs(float(value.strip().replace(' ', '').replace('*',''))) / 100 for value in list2]

    # zip them into a dictionary
    return (dict(zip(list1, list2)))

def delete_txt_files():
    for path in Path('.').glob('*.txt'):
        path.unlink()

if __name__ == '__main__':
    main()