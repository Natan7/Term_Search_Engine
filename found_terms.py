# import packages
import PyPDF2
import re
import os
import copy
import math


import io
from reportlab.pdfgen import canvas

page_width = math.floor(8.27*72)
page_height = math.floor(4.69*72)## 11.69*72 real size
## Read existing PDF

def search_and_registration(term_list, pages, pdf_writer, file_name):
   blank_page_flag = True
   for page in pages:
      text = page.extract_text().upper()
      for term in term_list:
         if(term.findall(text)):
            if blank_page_flag:
               ##pdf_writer.add_blank_page(page_width, page_height)
               packet = io.BytesIO()
               can = canvas.Canvas(packet, pagesize=[page_width, page_height])
               can.setFont("Courier", 16)
               can.drawString(20, 200, file_name)
               can.save()
               packet.seek(0)
               new_pdf = PyPDF2.PdfReader(packet)
               
               pdf_writer.add_page(new_pdf.pages[0])
               print("AKIIIIIIIIII")
               blank_page_flag = False
            pdf_writer.add_page(page)

   pdf_out = open('page_of_terms.pdf', 'wb')

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
   word_list = list(map(str.upper, word_list))

   for word in word_list:
      pattern_txt += "(\\b" + word + "\\b)"
   
   
   pattern_txt += "[:,]?"
   ##pattern_txt += "(?:.*?).(?:\n\n|\Z)"
   pattern = re.compile(pattern_txt, re.DOTALL)
   pattern_list.append(pattern)

print(pattern_list)

#### - DISCART - pattern = re.compile("(?:.*?)weighting(?:.*?)each(?:.*?).(?:\n\n|\Z)", re.DOTALL)
#### - DISCART - pattern = re.compile("(?:.*?)WEIGHTING(?:.?)EACH(?:.?)(?:.*?).(?:\n\n|\Z)", re.DOTALL)

# open the pdf files
#reader_list = []
files_names = copy.copy(os.listdir('Planos_Internaci_Nordeste'))
'''
for file_name in os.listdir('Planos_Internaci_Nordeste'):
   print(file_name)
   reader_list.append(PyPDF2.PdfReader(file_name))
'''


# pdf file output
pdf_writer = PyPDF2.PdfWriter("")
##pdf_writer.add_blank_page(page_width, page_height)

# extract text, search and write on pdf file
##reader = PyPDF2.PdfReader("research.pdf")
##search_and_registration(pattern, reader.pages, pdf_writer)

for file_name in files_names:
   print("=========================")
   print(file_name)
   reader = PyPDF2.PdfReader('Planos_Internaci_Nordeste/' + file_name)
   search_and_registration(pattern_list, reader.pages, pdf_writer, file_name)


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

# get number of pages
num_pages = len(pdf_writer.pages)
print()
print("--------------------")
print("Numero de páginas: " + str(num_pages))
print("--------------------")
