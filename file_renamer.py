from tkinter.constants import S
from zipfile import ZipFile
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image

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
        shutil.copyfile(file,f'{dest}/{new_name} - Rubric{ext}')

def zipped_btn():
    # gets location of zip file from user
    root.zip_file = filedialog.askopenfilename(initialdir=".")

    # check if files selected is a zip file
    file_name, ext = os.path.splitext(root.zip_file)
       
    if not root.zip_file == "":
        if ext == ".zip":
            zipped_lb.config(text = os.path.basename(root.zip_file)[:15]+"...")
            folder_btn.config(state=tk.NORMAL)
        else:
            zipped_lb.config(text = 'File selected is not zip file')
            root.zip_file = ""

def folder_btn():
    # get destination folder from user
    dir_path = filedialog.askdirectory(initialdir=".")
    
    _,new_folder = os.path.split(root.zip_file)
    root.destination = f"{dir_path}/{new_folder[:-4]}"
    try:
        os.mkdir(root.destination)
    except:
        messagebox.showerror("Error","Folder already exists")
        root.destination = ""

    # checks that a folder has been chosen
    if not root.destination == "":
        path, directory = os.path.split(root.destination)
        parent_dir = dir_path[dir_path.rfind("/")+1:]
        folder_lb.config(text = f"..\{parent_dir}\{directory[:10]}...")
        criteria_btn.config(state=tk.NORMAL)

def criteria_btn():
    # gets criteria file location from user
    root.criteria = filedialog.askopenfilename(initialdir=".")  

    # checks that criteria file has been selected
    if not root.criteria == "":
        criteria_lb.config(text = os.path.basename(root.criteria))
        go_btn.config(state=tk.NORMAL)

def go_btn():
    # intiates the extraction, renaming and copying process
    if root.zip_file != "" and root.destination != "" and root.criteria != "":
        unzip(root.zip_file,root.destination)
        rename(root.destination)
        add_file(root.criteria, root.destination)
        go_lb.config(text = "Files Created")
        open_folder_btn.config(state=tk.NORMAL)
    else:
        go_lb.config(text = "Components missing")

def open_folder():
    os.system(f"start {root.destination}")
    root.destroy()

# ----- MAIN PROGRAM -----

# ----- User Interface -----

# Style constants
TITLE = ("Arial",30)
BODY = ("Arial",14)
MESSAGE = ("Arial",10)
BY_LINE = ("Arial",8)
MBBC_BLUE = "#00ACEC"
MBBC_DK_BLUE = "#004B84"

# create window
root = tk.Tk()
#root.geometry("600x400")
root.title("Assessment Files Extractor")
root.configure(bg="white")

banner = tk.Frame(root,bg="white",pady=10,padx=10)
banner.pack()

body = tk.Frame(root,bg="white")
body.pack()

footer = tk.Frame(root,bg="white")
footer.pack()

# create elements

# banner
banner_file = Image.open("./assets/banner.png")
banner_img = ImageTk.PhotoImage(banner_file)
tk.Label(banner,
    bd=0,
    image=banner_img).pack()

# zipped file picker
tk.Label(body, 
    text="Zipped file location",
    font=BODY,
    padx=10,
    pady=10,
    fg=MBBC_DK_BLUE,
    bg="white")\
        .grid(sticky=tk.W,row=1,column=0)
zip_btn = tk.Button(body, 
    text="Choose File",
    width=20,
    font=BODY,
    relief=tk.FLAT,
    bg=MBBC_BLUE,
    fg=MBBC_DK_BLUE,
    command=zipped_btn)
zip_btn.grid(row=1, column=1)
zipped_lb = tk.Label(body, 
    text="Not Selected",
    width=20,
    font=MESSAGE,
    fg=MBBC_DK_BLUE,
    bg="white",
    padx=10,
    anchor=tk.W)
zipped_lb.grid(sticky=tk.W,row=1,column=2)

# desination folder picker
tk.Label(body,
    text="Destination Folder",
    font=BODY,
    padx=10,
    pady=10,
    fg=MBBC_DK_BLUE,
    bg="white")\
        .grid(sticky=tk.W,row=2,column=0)
folder_btn = tk.Button(body,
    text="Select Folder",
    width=20, 
    command=folder_btn,
    font=BODY,
    bg=MBBC_BLUE,
    fg=MBBC_DK_BLUE,
    relief=tk.FLAT, 
    state=tk.DISABLED)
folder_btn.grid(row=2,column=1)
folder_lb = tk.Label(body, 
    text="Not Selected",
    width=20,
    font=MESSAGE,
    fg=MBBC_DK_BLUE,
    bg="white",
    padx=10,
    anchor=tk.W)
folder_lb.grid(sticky=tk.W,row=2,column=2)

# criteria sheet picker
tk.Label(body, 
    text="Rubric File",
    font=BODY,
    padx=10,
    pady=10,
    fg=MBBC_DK_BLUE,
    bg="white")\
        .grid(sticky=tk.W, row=3,column=0)
criteria_btn = tk.Button(body, 
    text = "Choose Rubric File", 
    command=criteria_btn,
    width=20,
    font=BODY,
    bg=MBBC_BLUE,
    fg=MBBC_DK_BLUE,
    relief=tk.FLAT,
    state=tk.DISABLED)
criteria_btn.grid(row=3,column=1)
criteria_lb = tk.Label(body, 
    font=MESSAGE,
    width=20,
    fg=MBBC_DK_BLUE,
    text="Not Selected",
    bg="white",
    padx=10,
    anchor=tk.W)
criteria_lb.grid(sticky=tk.W,row=3,column=2)

# go button
tk.Label(body, 
    text="",
    font=BODY,
    padx=10,
    pady=10,
    bg="white")\
        .grid(sticky=tk.W,row=4,column=0)
go_btn = tk.Button(body, 
    text="Go",
    command=go_btn,
    width=20,
    font=BODY,
    bg=MBBC_BLUE,
    fg=MBBC_DK_BLUE,
    relief=tk.FLAT,
    state=tk.DISABLED)
go_btn.grid(row=4,column=1)
go_lb = tk.Label(body, 
    text="",
    font=MESSAGE,
    width=20,
    fg=MBBC_DK_BLUE,
    bg="white",
    padx=10,
    anchor=tk.W)
go_lb.grid(row=4,column=2)

# open folder button
tk.Label(body, 
    text="",
    font=BODY,
    padx=10,
    pady=10,
    bg="white")\
        .grid(sticky=tk.W,row=5,column=0)
open_folder_btn = tk.Button(body,
    text="Open Folder",
    command=open_folder,
    width=20,
    font=BODY,
    bg=MBBC_BLUE,
    fg=MBBC_DK_BLUE,
    relief=tk.FLAT,
    state=tk.DISABLED)
open_folder_btn.grid(row=5,column=1)

# by line
tk.Label(footer,
    text="by Damien Murtagh",
    font=BY_LINE,
    bg="white",
    fg=MBBC_DK_BLUE,
    padx=10,
    pady=10).pack()

# ----- Global variables ----- 
root.zip_file = ""
root.destination = ""
root.criteria = ""

# ----- Run Mainloop -----
root.mainloop()