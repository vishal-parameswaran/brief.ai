from PyPDF2 import PdfReader,PdfWriter
import re
import pandas as pd
import os


skipped_files = {
        'file_path': []
}

folder = r"C:\Users\yomaa\Documents\Github\University-of-Chicago\Capstone\Files\EB"
main_output_folder = r"C:\Users\yomaa\Documents\Github\University-of-Chicago\Capstone\splitFiles\EB\\"

for foldername in os.listdir(folder):
    print("_"*100)
    output_folder = main_output_folder + foldername
    print("Output path: " + output_folder)
    if not os.path.exists(output_folder):
            os.mkdir(output_folder)
    current_folder = folder + "\\"+foldername
    for filename in os.listdir(current_folder):
        file_path = current_folder +'\\'+filename
        skipped = False
        print("-"*100)
        print("File path: " + file_path)
        #Read PDF
        reader = PdfReader(file_path)
        last_page = (len(reader.pages))
        page = reader.pages[0]
        text = page.extract_text()
        print(text)
        text = re.split(r'(?<=[\d])[\n]+(?=[A-Z])(?!(Factiva))', text)
        print(text)
        text[0] = text[0].split("\n")[1]
        pdf_pages = {
            'name': [],
            'first_page': [] 
        }
        print(text)
        value = ""
        for i in range(0,len(text)):
            if (text[i] != '') and (not (text[i] is None)):
                print(text[i])
                value = re.split(r'\.\.+', text[i])
                print(value,len(value))
                if len(value)<2:
                    skipped=True
                    break
                name = value[0]
                name = name.replace('\n','')
                page = value[1]
                page = page.replace('\n','')
                try:
                    int(page)
                except:
                    skipped=True
                    break
                pdf_pages['name'].append(name)
                pdf_pages['first_page'].append(int(page))
        print(pdf_pages)
        print(skipped,value)
        if skipped:
            skipped_files['file_path'].append(file_path)
            continue
        pd_pages = pd.DataFrame(pdf_pages)
        pd_pages['last_page'] = pd_pages['first_page'].shift(-1)
        pd_pages.iloc[len(pd_pages)-1,2] = last_page + 1
        pd_pages['last_page'] = pd_pages['last_page'] - 1

        for i in range(len(pd_pages)):
            writer = PdfWriter()
            page_range = range(pd_pages.iloc[i,1], int(pd_pages.iloc[i,2]) + 1)
            for page_num, page in enumerate(reader.pages, 1):
                if page_num in page_range:
                    writer.add_page(page)
            if len(pd_pages.iloc[i,0])>100:
                file_name_temp =  pd_pages.iloc[i,0]
                file_name_temp = file_name_temp[0:70]
                file_name_temp = re.sub("[^0-9a-zA-Z]","",file_name_temp)
            else:
                file_name_temp =  pd_pages.iloc[i,0]
                file_name_temp = re.sub("[^0-9a-zA-Z]","",file_name_temp)
            file_name = output_folder + "/" + file_name_temp
            with open(f'{file_name}.pdf', 'wb') as out:
                writer.write(out)


skipped_files_pd = pd.DataFrame(skipped_files)
skipped_files_pd.to_csv(r"skipped_files_eb.csv",index=False)
