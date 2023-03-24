from tkinter.constants import S
from zipfile import ZipFile
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
from docx2pdf import convert


def unzip(file, dest):
    # ensures provided file is a zip file and then unzips it
    # accepts zip file path as file(str) and destination folder path as dest(str)

    try:
        with ZipFile(file, 'r') as zipped:
            zipped.extractall(dest)
    except Exception:
        print("Error with zip file")


def rename(directory):
    # renames each file in provided directory removing student number
    # accepts processing directory path as directory(str)
    
    for entry in os.listdir(directory):
        new_name = entry[9:]
        os.rename(f'{directory}/{entry}',f'{directory}/{new_name}')


def add_file(file, dest):
    # takes rubric file, makes a copy for each file in dest directory using the files name
    # accepts rubric file path as file(str) and deestination folder path as dest(str)
    
    period_index = file.find(".")
    ext = file[period_index:]
    
    for entry in os.listdir(dest):
        dash_index = entry.find("-")
        new_name = entry[:dash_index]
        #print(new_name)
        shutil.copyfile(file,f'{dest}/{new_name} - Rubric{ext}')


def zipped_btn():
    # gets zip file path from user
    # assigns zip file path to zip_file(str)

    root.zip_file = filedialog.askopenfilename(initialdir=".")

    # ensure that files selected is a zip file
    _, ext = os.path.splitext(root.zip_file)

    if root.zip_file != "":
        if ext == ".zip":
            zipped_lb.config(text=f"{os.path.basename(root.zip_file)[:15]}...")
            folder_btn.config(state=tk.NORMAL) # enables folder button
        else:
            zipped_lb.config(text = 'File selected is not zip file')
            root.zip_file = ""


def folder_btn():
    # get destination folder path from user
    # assigns folder path to root.destination(str)

    dir_path = filedialog.askdirectory(initialdir=".")

    _,new_folder = os.path.split(root.zip_file)
    root.destination = f"{dir_path}/{new_folder[:-4]}"

    # check that folder does not already exsist
    try:
        os.mkdir(root.destination)
    except Exception:
        messagebox.showerror("Error","Folder already exists")
        root.destination = ""

    # ensure that a folder was selected rather than clicking cancel
    if root.destination:
        _, directory = os.path.split(root.destination)
        parent_dir = dir_path[dir_path.rfind("/")+1:]
        folder_lb.config(text = f"..\{parent_dir}\{directory[:10]}...")
        rubric_btn.config(state=tk.NORMAL) # enables rubric button


def rubric_btn():
    # gets rubric file path from user
    # assigns rubric file path to root.rubric(str)

    root.rubric = filedialog.askopenfilename(initialdir=".")  

    # ensures that rubric file was selected rather than clicking cancel
    if root.rubric != "":
        criteria_lb.config(text = os.path.basename(root.rubric))
        go_btn.config(state=tk.NORMAL) # enables go button


def go_btn():
    # intiates the extraction, renaming and copying process
    
    # ensure all necessary information has been entered
    if root.zip_file != "" and root.destination != "" and root.rubric != "":
        # run process
        unzip(root.zip_file, root.destination)
        rename(root.destination)
        add_file(root.rubric, root.destination)
        convert(root.destination)
        go_lb.config(text = "Files Created")
        open_folder_btn.config(state=tk.NORMAL) # enables open folder button
    else:
        # error message
        go_lb.config(text = "Components missing")


def open_folder():
    # opens the destination folder path in File Explorer
    os.system(f"start {root.destination}")
    root.destroy()


# ----- MAIN PROGRAM -----

# --- User Interface ---
# -- Style Constants --
TITLE = ("Arial",30)
BODY = ("Arial",14)
MESSAGE = ("Arial",10)
BY_LINE = ("Arial",8)
MBBC_BLUE = "#00ACEC"
MBBC_DK_BLUE = "#004B84"

# -- Create Window --
root = tk.Tk()
root.title("Assessment Files Extractor")
root.configure(bg="white")

# create three frames
banner = tk.Frame(root,
    bg="white",
    pady=10,
    padx=10)
banner.pack()

body = tk.Frame(root,
    bg="white")
body.pack()

footer = tk.Frame(root,
    bg="white")
footer.pack()

# -- Create Elements --
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
    fg=MBBC_DK_BLUE,
    bg="white",
    padx=10,
    pady=10,
    anchor=tk.W)\
        .grid(sticky=tk.W,row=1,column=0)

zip_btn = tk.Button(body, 
    text="Choose File",
    font=BODY,
    fg=MBBC_DK_BLUE,
    bg=MBBC_BLUE,
    width=20,
    relief=tk.FLAT,
    command=zipped_btn)
zip_btn.grid(row=1, column=1)

zipped_lb = tk.Label(body, 
    text="Not Selected",
    font=MESSAGE,
    fg=MBBC_DK_BLUE,
    bg="white",
    width=20,
    padx=10,
    anchor=tk.W)
zipped_lb.grid(sticky=tk.W,row=1,column=2)

# desination folder picker
tk.Label(body,
    text="Destination Folder",
    font=BODY,
    fg=MBBC_DK_BLUE,
    bg="white",
    padx=10,
    pady=10,
    anchor = tk.W)\
        .grid(sticky=tk.W,row=2,column=0)

folder_btn = tk.Button(body,
    text="Select Folder",
    font=BODY,
    fg=MBBC_DK_BLUE,
    bg=MBBC_BLUE,
    width=20,
    relief=tk.FLAT,
    command=folder_btn, 
    state=tk.DISABLED)
folder_btn.grid(row=2,column=1)

folder_lb = tk.Label(body, 
    text="Not Selected",
    font=MESSAGE,
    fg=MBBC_DK_BLUE,
    bg="white",
    padx=10,
    width=20,
    anchor=tk.W)
folder_lb.grid(sticky=tk.W,row=2,column=2)

# rubric picker
tk.Label(body, 
    text="Rubric File",
    font=BODY,
    fg=MBBC_DK_BLUE,
    bg="white",
    padx=10,
    pady=10,
    anchor = tk.W)\
        .grid(sticky=tk.W, row=3,column=0)

rubric_btn = tk.Button(body, 
    text = "Choose Rubric File", 
    font=BODY,
    fg=MBBC_DK_BLUE,
    bg=MBBC_BLUE,
    width=20,
    relief=tk.FLAT,
    command=rubric_btn,
    state=tk.DISABLED)
rubric_btn.grid(row=3,column=1)

criteria_lb = tk.Label(body, 
    text="Not Selected",
    font=MESSAGE,
    fg=MBBC_DK_BLUE,
    bg="white",
    width=20,
    padx=10,
    anchor=tk.W)
criteria_lb.grid(sticky=tk.W,row=3,column=2)

# go button
'''
tk.Label(body, 
    text="",
    font=BODY,
    bg="white",
    padx=10,
    pady=10,
    anchor = tk.W)\
        .grid(sticky=tk.W,row=4,column=0)
'''
go_btn = tk.Button(body, 
    text="Go",
    font=BODY,
    fg=MBBC_DK_BLUE,
    bg=MBBC_BLUE,
    width=20,
    relief=tk.FLAT,
    command=go_btn,
    state=tk.DISABLED)
go_btn.grid(row=4,column=1)

go_lb = tk.Label(body, 
    text="",
    font=MESSAGE,
    fg=MBBC_DK_BLUE,
    bg="white",
    width=20,
    padx=10,
    anchor=tk.W)
go_lb.grid(row=4,column=2)

# open folder button
# this label is needed to maintain the gap 
# between the go and open folder buttons
tk.Label(body, 
    text="",
    font=BODY,
    padx=10,
    pady=10,
    bg="white",
    anchor = tk.W)\
        .grid(sticky=tk.W,row=5,column=0) 
        
open_folder_btn = tk.Button(body,
    text="Open Folder",
    font=BODY,
    fg=MBBC_DK_BLUE,
    bg=MBBC_BLUE,
    width=20,
    relief=tk.FLAT,
    command=open_folder,
    state=tk.DISABLED)
open_folder_btn.grid(row=5,column=1)

tk.Label(body, 
    text="Not for OneDrive folders",
    font=MESSAGE,
    fg=MBBC_DK_BLUE,
    bg="white",
    width=20,
    padx=10,
    anchor=tk.W)\
        .grid(sticky=tk.W,row=5,column=2)

# by line
tk.Label(footer,
    text="by Damien Murtagh",
    font=BY_LINE,
    bg="white",
    fg=MBBC_DK_BLUE,
    padx=10,
    pady=10).pack()

# ----- Global variables ----- 
root.zip_file = ""          # path of downloaded zip file
root.destination = ""       # path of folder which all files will be sent to
root.rubric = ""            # path of marking rubric file

# ----- Run Mainloop -----
root.mainloop()