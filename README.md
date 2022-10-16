*Assuming your pay statment pdfs are structured the same way mine are*, this program will extract basic data from those pdfs and write them to a .csv file. 

### Getting Started
1. Have reasonably current installations of
    - Python
    - pandas
    - pathlib
    - pdfminer
1. download/fork/clone this repo
1. place paystub pdfs in the `pdfs` directory.
1. In a terminal, run `python extract_data.py`
1. VOILA! You should now see a csv file inside the `data` directory entitled `pay.csv`.

Credit to the author of this post for the `pdf_to_text` function using the `pdfminer` library:
https://www.pythonpool.com/python-pdf-parser/