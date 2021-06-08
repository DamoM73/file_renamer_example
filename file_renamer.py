from zipfile import ZipFile
import os
import shutil
import tkinter as tk
from tkinter import filedialog

def unzip(file, dest):
    # ensures provided file is a zip file and then unzips it

    try:
        with ZipFile(file, 'r') as zipped:
            zipped.extractall(dest)
    except:
        print("Error with zip file")

def rename(directory):
    # renames each file in provided directory removing student number
    for entry in os.listdir(directory):
        new_name = entry[9:]
        os.rename(f'{directory}/{entry}',f'{directory}/{new_name}')

def add_file(file, dest):
    # takes file, makes a copy for each file in dest directory using the files name
    period_index = file.find(".")
    ext = file[period_index:]
    
    for entry in os.listdir(dest):
        dash_index = entry.find("-")
        new_name = entry[:dash_index]
        #print(new_name)
        shutil.copyfile(file,f'{dest}/{new_name} - criteria{ext}')

def zipped_btn():
    # gets location of zip file from user
    root.zip_file = filedialog.askopenfilename(initialdir=".")

    # check if files selected is a zip file
    file_name, ext = os.path.splitext(root.zip_file)
       
    if not root.zip_file == "":
        if ext == ".zip":
            zipped_lb.config(text = os.path.basename(root.zip_file[:root.zip_file.find("__")]+"..."))
            folder_btn.config(state=tk.NORMAL)
        else:
            zipped_lb.config(text = 'File selected is not zip file')
            root.zip_file = ""

def folder_btn():
    # get destination folder from user
    selection = filedialog.askdirectory(initialdir=".")
    
    _,name = os.path.split(root.zip_file)
    root.destination =selection+"/"+name[:-4]
    os.mkdir(root.destination)

    # checks that a folder has been chosen
    if not root.destination == "":
        path, directory = os.path.split(root.destination)
        folder_lb.config(text = f"..\{directory}")
        criteria_btn.config(state=tk.NORMAL)

def criteria_btn():
    # gets criteria file location from user
    root.criteria = filedialog.askopenfilename(initialdir=".")  

    # checks that criteria file has been selected
    if not root.criteria == "":
        criteria_lb.config(text = os.path.basename(root.zip_file))
        go_btn.config(state=tk.NORMAL)

def go_btn():
    # intiates the extraction, renaming and copying process
    if root.zip_file != "" and root.destination != "" and root.criteria != "":
        unzip(root.zip_file,root.destination)
        rename(root.destination)
        add_file(root.criteria, root.destination)
        go_lb.config(text = "Files Created")
    else:
        go_lb.config(text = "Components missing")

# ----- CONSTANTS -----
TITLE = ("Arial",30)
BODY = ("Arial",14)
MESSAGE = ("Arial",10)


# ----- MAIN PROGRAM -----
# create window
root = tk.Tk()
#root.geometry("600x400")
root.title("File Renamer")

# create elements
tk.Label(root,
    text="File Renamer",
    font=TITLE)\
    .grid(row=0, column=0, columnspan=3)

# zipped file picker
tk.Label(root, 
    text="Zipped file location",
    font=BODY,
    width=20)\
        .grid(row=1,column=0)
zip_btn = tk.Button(root, 
    text="Choose File",
    width=20,
    font=BODY,
    command=zipped_btn)
zip_btn.grid(row=1, column=1)
zipped_lb = tk.Label(root, 
    text="Not Selected",
    width=20,
    font=MESSAGE)
zipped_lb.grid(row=1,column=2)

# desination folder picker
tk.Label(root,
    text="Destination Folder",
    font=BODY)\
        .grid(row=2,column=0)
folder_btn = tk.Button(root,
    text="Select Folder",
    width=20, 
    command=folder_btn,
    font=BODY, 
    state=tk.DISABLED)
folder_btn.grid(row=2,column=1)
folder_lb = tk.Label(root, 
    text="Not Selected",
    width=20,
    font=MESSAGE)
folder_lb.grid(row=2,column=2)

# criteria sheet picker
tk.Label(root, 
    text="Criteria Sheet",
    font=BODY)\
        .grid(row=3,column=0)
criteria_btn = tk.Button(root, 
    text = "Choose Criteria Sheet", 
    command=criteria_btn,
    width=20,
    font=BODY,
    state=tk.DISABLED)
criteria_btn.grid(row=3,column=1)
criteria_lb = tk.Label(root, 
    font=MESSAGE,
    width=20,
    text="Not Selected")
criteria_lb.grid(row=3,column=2)

# go button
go_btn = tk.Button(root, 
    text="Go",
    command=go_btn,
    width=20,
    font=BODY,
    state=tk.DISABLED)
go_btn.grid(row=4,column=1)
go_lb = tk.Label(root, 
    text="",
    font=MESSAGE,
    width=20)
go_lb.grid(row=5,column=0,columnspan=3)

# Global variables
root.zip_file = ""
root.destination = ""
root.criteria = ""

# run mainloop
root.mainloop()