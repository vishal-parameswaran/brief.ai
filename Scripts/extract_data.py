import pandas as pd
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import os
import re

folder_path = r""
output_path = r""
disclaimer_regex = re.compile(r"\[Thomson Financial reserves")

for foldername in os.listdir(folder_path):
    print("_"*100)
    output_folder = output_path + foldername + '/'
    print("Output path: " + output_folder)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    for filename in os.listdir(folder_path+foldername):
        file_path = folder_path+foldername + '/' + filename
        text_file_name = output_folder + filename.replace("pdf","txt")
        reader = extract_pages(file_path)
        final_text = ""
        for page_layout in reader:
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    final_text += element.get_text()

        text_split = re.split(disclaimer_regex,final_text)
        output_file = open(text_file_name,"wb")
        output_file.write(text_split[0].encode('utf-8'))
        output_file.close()
        