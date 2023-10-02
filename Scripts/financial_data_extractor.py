import os
import re
import pandas as pd
from pathlib import Path
folder_path = r""
output_path = r""

skipped_files = pd.DataFrame(columns=['file_name'])

# initializing substrings
sub1 = "FINANCIAL DATA"
sub2 = "PRESENTATION"
 
for foldername in os.listdir(folder_path):
    print("_"*100)
    output_folder = output_path + foldername + '/'
    print("Output path: " + output_folder)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    for filename in os.listdir(folder_path+foldername):
        print("File name: " + filename)
        file_path = folder_path+foldername + '/' + filename
        text_file_name = output_folder + filename
        try:
            test_str = open(file_path,"r").read()
        except UnicodeDecodeError:
            test_str = ''
            with open(file_path,"r",encoding='utf-8') as f:
                test_str = test_str + f.read()
            f.close()
        # getting index of substrings
        try:
            idx1 = test_str.index(sub1)
        except ValueError:
            print("Skipping file: " + filename)
            skipped_files = pd.concat([skipped_files, pd.DataFrame([filename], columns=['file_name'])])
            
        idx2 = test_str.index(sub2)
        res = ''
        # getting elements in between
        for idx in range(idx1 + len(sub1) + 1, idx2):
            res = res + test_str[idx]
        output_file = open(text_file_name,"wb")
        output_file.write(res.encode('utf-8'))
        output_file.close()
        