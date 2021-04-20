from zipfile import ZipFile
import os

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

# ----- MAIN PROGRAM -----
zip_file = "11.FIA1___Creating_with_Code___Investigation_Final.zip"
destination = "student_files"
unzip(zip_file,destination)
rename(destination)