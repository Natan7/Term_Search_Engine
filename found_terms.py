# import packages
import re
import os
import io
import copy
import math
import fitz
import time
import PyPDF2
from reportlab.pdfgen import canvas

# constants
PAGE_WIDTH = math.floor(8.27*72)
PAGE_HEIGHT = math.floor(4.69*72)## 11.69*72 real size

# methods
def generate_pattern(term_list):
   for term in term_list:
      pattern_txt = r"\b" + term.upper() + r"\b"
      pattern_list.append(pattern_txt)
   return pattern_list

def create_cover_page(file_name):
   packet = io.BytesIO()
   can = canvas.Canvas(packet, pagesize=[PAGE_WIDTH, PAGE_HEIGHT])
   can.setFont("Courier", 15)
   can.drawString(20, 180, file_name)
   can.save()
   packet.seek(0)
   return PyPDF2.PdfReader(packet)

''' extract text, search and write on pdf file '''
def search_and_registration(term_list, doc, reader_doc, pdf_writer, file_name):
   blank_page_flag = True
   page_number = 0
   page_number_added = []
   for page in doc:
      text = page.getText().upper()
      for term in term_list:
         if(re.search(term, text)):
            if blank_page_flag:
               cover_page = create_cover_page(file_name)
               pdf_writer.add_page(cover_page.pages[0])
               blank_page_flag = False

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

############################################################################
# main
############################################################################
term_list=[]
print("Lendo input de termos...")
with open('input_terms.txt') as file:
    term_list = [line.rstrip() for line in file]
print("Termos utilizados para esta busca: ")
print(*term_list, sep = "\n")

pattern_list = []
pattern_list = generate_pattern(term_list)
print(pattern_list)

''' get pdf files names '''
files_names = copy.copy(os.listdir('Planos_Internaci_Nordeste'))

''' create pdf file output '''
pdf_writer = PyPDF2.PdfWriter("")

''' search terms per file '''
for file_name in files_names:
   print("======")
   print(file_name)
   print("======")
   doc = fitz.open('Planos_Internaci_Nordeste/' + file_name)
   reader = PyPDF2.PdfReader('Planos_Internaci_Nordeste/' + file_name)
   search_and_registration(pattern_list, doc, reader.pages, pdf_writer, file_name)

''' results '''
num_pages = len(pdf_writer.pages)
print()
print("--------------------")
print("Numero de páginas: " + str(num_pages))
print("--------------------")