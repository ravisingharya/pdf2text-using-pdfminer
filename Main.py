from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt
import sqlite3

#converts pdf, returns its text content as a string
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
        
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text 
   
def convertMultiple(pdfDir, txtDir, dbDir):
    if pdfDir == "": pdfDir = os.getcwd() + "\\"
    for pdf in os.listdir(pdfDir): 
        fileExtension = pdf.split(".")[-1]
        if fileExtension == "pdf":
            pdfFilename = pdfDir + pdf 
            text = convert(pdfFilename) 
            textFilename = txtDir + pdf + ".txt"
            textFile = open(textFilename, "w") 
            textFile.write(text) 
            dbfilename = dbDir + "PDF DB" + ".db"
            conn = sqlite3.connect(dbfilename)
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS PDF2TEXT (PDF_Name TEXT, Extracted_Text TEXT)')
            conn.commit()
            c.execute("INSERT INTO PDF2TEXT VALUES(?,?)",
                      (pdf, text))
            conn.commit()

pdfDir = "INPUT_PDF/"
txtDir = "CONVERTED_TEXT/"
dbDir = "CONVERTED_DB/"
convertMultiple(pdfDir, txtDir, dbDir)
