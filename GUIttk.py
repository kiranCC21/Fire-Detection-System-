import numpy as np
import cv2
from time import time
from ultralytics import YOLO

import supervision as sv
from PIL import ImageTk,Image


from tkinter import *
from tkinter import filedialog as fd
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
from  FIRE_DETECTOR_2 import *
root = tb.Window(themename="solar")
lg=PhotoImage(file="fdslg.png")
root.wm_iconphoto(False,lg)

   
root.title("Fire Detection System ")
root.geometry('1500x450')


#root = ttk.Window(themename="darkly")
bg=tb.PhotoImage(file="fdslg.png")
bgl=tb.Label(root,image=bg)
bgl.place(x=0,y=0)
my_label=tb.Label(text="Fire Detection System",font=("Helvetica",20),bootstyle="Default")
my_label.pack(pady=50)
vid_path=""

def getFilePath():
    filetypes = (
 ('video files', '*.mp4'),
 ('image ffiles', '*.jpg')
 )   

    vid_path = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes,
    )

    showinfo(
        title='Selected File',
        message=vid_path,
    )
    FDS = FireDetection(vid_path)
    FDS()
open_button = ttk.Button(
    root,
    text='Browse the video file......',
    command=getFilePath,
bootstyle=(SUCCESS, OUTLINE))
open_button.pack(side=TOP, padx=5, pady=60)
#fd=FireDetection(vid_path)
#fd()
#run_detection(vid_path)
# run the application
root.mainloop()
