# import packages
import PyPDF2
import re
import os
import copy
import math
import fitz
import io
from reportlab.pdfgen import canvas
from datetime import datetime
import time

PAGE_WIDTH = math.floor(8.27*72)
PAGE_HEIGHT = math.floor(4.69*72)## 11.69*72 real size

def create_cover_page(file_name):
   packet = io.BytesIO()
   can = canvas.Canvas(packet, pagesize=[PAGE_WIDTH, PAGE_HEIGHT])
   can.setFont("Courier", 15)
   can.drawString(20, 180, file_name)
   can.save()
   packet.seek(0)
   return PyPDF2.PdfReader(packet)

def search_and_registration(term_list, doc, reader_doc, pdf_writer, file_name):
   blank_page_flag = True
   page_number = 0
   page_number_added = []
   for page in doc:
      text = page.getText().upper()
      for term in term_list:
         print(re.search(term, text))
         if(re.search(term, text)):
            if blank_page_flag:
               new_pdf = create_cover_page(file_name)

               pdf_writer.add_page(new_pdf.pages[0])
               blank_page_flag = False

            print(text)
            if page_number not in page_number_added:
               pdf_writer.add_page(reader_doc[page_number])
               page_number_added.append(page_number)

      page_number+=1
   
   #current_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
   current_time = time.strftime("%Y-%m-%d", time.localtime())
   file_output_name = "search_results_" + current_time + ".pdf"
   pdf_out = open(file_output_name, 'wb')
   pdf_writer.write(pdf_out)
   pdf_out.close()

terms_count = int(input("Informe quantos termos você irá pesquisar: "))
i=1
term_list=[]
while i<=terms_count:
   term_list.append(input("Informe o " + str(i) + "º termo para pesquisa: "))
   i+=1

#### - DISCART - pattern = re.compile(r'^weighting.+(?:\n.+)*', re.MULTILINE)
pattern_list = []
for term in term_list:
   ##pattern_txt = "(?:.*?)"
   pattern_txt = ""

   word_list = term.split(" ")
   '''
   word_list = list(map(str.upper, word_list))
   first_word_flag = True
   for word in word_list:
      if first_word_flag:
         pattern_txt += "(\b"
         pattern_txt += word
         first_word_flag = False
      else:
         pattern_txt += " " + word

   pattern_txt += "\b)[:,]?"
   '''
   print(term)
   word = term.upper()
   print(word)
   ##pattern_txt += "(" + word + "\\b)[:,]?"
   pattern_txt += r"\b" + word + r"\b"

   ##pattern_txt += "(?:.*?).(?:\n\n|\Z)"
   ##pattern = re.compile(pattern_txt, re.DOTALL)

   ##pattern_list.append(pattern)
   pattern_list.append(pattern_txt)

print(pattern_list)

#### - DISCART - pattern = re.compile("(?:.*?)weighting(?:.*?)each(?:.*?).(?:\n\n|\Z)", re.DOTALL)
#### - DISCART - pattern = re.compile("(?:.*?)WEIGHTING(?:.?)EACH(?:.?)(?:.*?).(?:\n\n|\Z)", re.DOTALL)

# open the pdf files
#reader_list = []
files_names = copy.copy(os.listdir('Planos_Internaci_Nordeste'))


# pdf file output
pdf_writer = PyPDF2.PdfWriter("")
##pdf_writer.add_blank_page(PAGE_WIDTH, PAGE_HEIGHT)

# extract text, search and write on pdf file
##reader = PyPDF2.PdfReader("research.pdf")
##search_and_registration(pattern, reader.pages, pdf_writer)

for file_name in files_names:
   print("=========================")
   print(file_name)
   doc = fitz.open('Planos_Internaci_Nordeste/' + file_name)
   reader = PyPDF2.PdfReader('Planos_Internaci_Nordeste/' + file_name)
   search_and_registration(pattern_list, doc, reader.pages, pdf_writer, file_name)
   ##reader = PyPDF2.PdfReader('Planos_Internaci_Nordeste/' + file_name)
   ##search_and_registration(pattern_list, reader.pages, pdf_writer, file_name)

      



''' DISCART
for page in reader.pages:
    text = page.extract_text().upper()
    if(pattern.findall(text)):
      print(pattern.findall(text))
      pdf_writer.add_page(page)

pdf_out = open('page_of_terms.pdf', 'wb')
pdf_writer.write(pdf_out)
pdf_out.close()
'''

#current_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
'''
current_time = time.strftime("%Y-%m-%d", time.localtime())
file_output_name = "search_results_" + current_time + ".pdf"
pdf_out = open(file_output_name, 'wb')
pdf_writer.write(pdf_out)
pdf_out.close()
'''

# get number of pages
num_pages = len(pdf_writer.pages)
print()
print("--------------------")
print("Numero de páginas: " + str(num_pages))
print("--------------------")
