from zipfile import ZipFile
import os
import shutil

def unzip(file, dest):
    try:
        with ZipFile(file, 'r') as zipped:
            zipped.extractall(dest)
    except:
        print("Error with zip file")

def rename(directory):
    for entry in os.listdir(directory):
        new_name = entry[9:]
        os.rename(f'{directory}/{entry}',f'{directory}/{new_name}')

def add_file(file, dest):
    for entry in os.listdir(dest):
        dash_index = entry.find("-")
        new_name = entry[:dash_index]
        print(new_name)
        shutil.copyfile(file,f'{dest}/{new_name} - criteria.docx')

# ----- MAIN PROGRAM -----
# Global variables
zip_file = "11.FIA1___Creating_with_Code___Investigation_Final.zip"
destination = "student_files"
criteria = "criteria.docx"

# Function calls
unzip(zip_file,destination)
rename(destination)
add_file(criteria, destination)