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
    period_index = file.find(".")
    ext = file[period_index:]
    print(ext)
    for entry in os.listdir(dest):
        dash_index = entry.find("-")
        new_name = entry[:dash_index]
        #print(new_name)
        shutil.copyfile(file,f'{dest}/{new_name} - criteria{ext}')

def zipped_btn():
    root.zip_file = filedialog.askopenfilename(initialdir=".")

    file_name, ext = os.path.splitext(root.zip_file)
    
    if not root.zip_file == "":
        if ext == ".zip":
            zipped_lb.config(text = os.path.basename(root.zip_file))
        else:
            zipped_lb.config(text = 'File selected is not zip file')
            root.zip_file = ""

def folder_btn():
    root.destination = filedialog.askdirectory(initialdir=".")
    
    if not root.destination == "":
        path, directory = os.path.split(root.destination)
        folder_lb.config(text = f"..\{directory}")
    #print(root.destination)

def criteria_btn():
    root.criteria = filedialog.askopenfilename(initialdir=".")  

    if not root.criteria == "":
        criteria_lb.config(text = os.path.basename(root.zip_file))

def go_btn():
    if root.zip_file != "" and root.destination != "" and root.criteria != "":
        unzip(root.zip_file,root.destination)
        rename(root.destination)
        add_file(root.criteria, root.destination)
        go_lb.config(text = "Files Created")
    else:
        go_lb.config(text = "Components missing")


# ----- MAIN PROGRAM -----
# create window
root = tk.Tk()
root.geometry("600x400")
root.title("File Renamer")

# create elements
tk.Label(root,text="File Renamer").grid(row=0, column=0, columnspan=2)

# zipped file picker
tk.Label(root, text="Zipped file location").grid(row=1,column=0)
tk.Button(root, text="Choose File", command=zipped_btn).grid(row=1, column=1)
zipped_lb = tk.Label(root, text="Not Selected")
zipped_lb.grid(row=1,column=2)

# desination folder picker
tk.Label(root,text="Destination Folder").grid(row=2,column=0)
tk.Button(root,text="Select Folder", command=folder_btn).grid(row=2,column=1)
folder_lb = tk.Label(root, text="Not Selected")
folder_lb.grid(row=2,column=2)

# criteria sheet picker
tk.Label(root, text="Criteria Sheet").grid(row=3,column=0)
tk.Button(root, text = "Choose Criteria Sheet", command=criteria_btn)\
    .grid(row=3,column=1)
criteria_lb = tk.Label(root, text="Not Selected")
criteria_lb.grid(row=3,column=2)

# go button
tk.Button(root, text="Go",command=go_btn).grid(row=4,column=1)
go_lb = tk.Label(root, text="")
go_lb.grid(row=4,column=2)

# Global variables
root.zip_file = ""
root.destination = ""
root.criteria = ""



# run mainloop
root.mainloop()