from zipfile import ZipFile
import os
import shutil
import tkinter as tk
from tkinter import filedialog

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
        #print(new_name)
        shutil.copyfile(file,f'{dest}/{new_name} - criteria.docx')

def zipped_btn():
    root.zip_file = filedialog.askopenfile(initialdir=".").name
    #print(root.zip_file)

def folder_btn():
    root.destination = filedialog.askdirectory(initialdir=".")
    #print(root.destination)

def criteria_btn():
    root.criteria = filedialog.askopenfilename(initialdir=".")
    print(root.criteria)

def go_btn():
    unzip(root.zip_file,root.destination)
    rename(root.destination)
    add_file(root.criteria, root.destination)

# ----- MAIN PROGRAM -----
# create window
root = tk.Tk()
root.geometry("600x400")
root.title("File Renamer")

# create elements
tk.Label(root,text="File Renamer").grid(row=0, column=0, columnspan=2)

# zipped folder picker
tk.Label(root, text="Zipped file location").grid(row=1,column=0)
tk.Button(root, text="Choose Folder", command=zipped_btn).grid(row=1, column=1)

# desination folder picker
tk.Label(root,text="Destination Folder").grid(row=2,column=0)
tk.Button(root,text="Select Folder", command=folder_btn).grid(row=2,column=1)

# criteria sheet picker
tk.Label(root, text="Criteria Sheet").grid(row=3,column=0)
tk.Button(root, text = "Choose Criteria Sheet", command=criteria_btn).grid(row=3,column=1)

# go button
tk.Button(root, text="Go",command=go_btn).grid(row=4,column=1)

# Global variables
root.zip_file = ""
root.destination = ""
root.criteria = ""



# run mainloop
root.mainloop()