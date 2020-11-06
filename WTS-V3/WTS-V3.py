# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 16:14:56 2020

@author: Walden
"""

#%%Libraries 
import tkinter 
import cv2
import os
import os.path
import numpy as np
import serial
import PIL.Image
from PIL import Image, ImageTk
from ast import literal_eval
from scipy import misc, ndimage
from tkinter import PhotoImage, messagebox, ttk, Canvas, filedialog, Tk, Frame, BOTH
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import font
from tkinter.font import Font
from tkinter.simpledialog import askstring
from screeninfo import get_monitors
from tkinter import Button, Frame, INSERT, LEFT, RIGHT, Label
from tkinter import  Scrollbar, Text, Tk, TOP, X, Y, filedialog
from tkinter import *
import cv2
from screeninfo import get_monitors



#%%-------------GENERAL FUNCTIONS-------------
#%%Colors 
C_Primary = (21,21,21)
C_Light_Dark = (48,48,48)
C_White = (255,255,255)
C_Dark = (0,0,0)
C_Grey = (200,200,200)
C_Red = (255,0,0)
Font_CV = cv2.FONT_HERSHEY_SIMPLEX
Font_1 = 'Sans'

def Fun_Rgb(RGB):
    return "#%02x%02x%02x" % RGB  


#%%Fun Size
def Fun_Size(img, size):
    img = PIL.Image.open(img)
    size_1 = img.size
    width = int(size_1[0]*size)
    height = int(size_1[1]*size)
    img = img.resize((width, height))
    img = ImageTk.PhotoImage(img)
    return img

         
#%%Diectories
Dir_Images = 'Image/'
Dir_Projects = 'Projects/'
Dir_Videos = 'Videos/'
Dir_Project_Images = '/Images/'

#%%Windows size
aux_monitor = 0

try:
    for monitor in get_monitors():
        aux_monitor += 1
        if aux_monitor == 1:
            monitor_size = monitor
            aux_string_monitor = str(monitor_size)
            aux_cortar = aux_string_monitor.split('Monitor(')
            aux_cortar = aux_cortar[1].split(')')
            parameters_monitor = aux_cortar[0].split('width=')
            parameters_monitor = parameters_monitor[1].split(', height=')
            width_monitor = int(parameters_monitor[0])
            parameters_monitor = parameters_monitor[1].split(', width_mm=')
            height_monitor = int(parameters_monitor[0])
    
        if aux_monitor == 2:
            monitor_size = monitor
            aux_string_monitor = str(monitor_size)
            aux_cortar = aux_string_monitor.split('Monitor(')
            aux_cortar = aux_cortar[1].split(')')
            parameters_monitor = aux_cortar[0].split('width=')
            parameters_monitor = parameters_monitor[1].split(', height=')
            width_monitor = int(parameters_monitor[0])
            parameters_monitor = parameters_monitor[1].split(', width_mm=')
            height_monitor = int(parameters_monitor[0])
     
    aux_size = .65
    
except:
    width_monitor = 1280
    height_monitor = 800
    aux_size = .75
    
    
aux_width_monitor = width_monitor/15 
aux_height_monitor = height_monitor/15  


#%%Tool tip
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 20
        y = y + cy + self.widget.winfo_rooty() +20
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

#%%-------------PROGRAM FUNCTIONS------------- 
#%%Fun info
def info():
    messagebox.showinfo('WTS-V3','Program developed by Walden Modular Equipment')

def cutVideo():
    messagebox.showinfo(' ','In construction')

def newProjectAux():
    messagebox.showinfo(' ','In construction')
    

#%%-------------WIDGETS-------------
#%%Principal window
root = Tk()
root.title('Walden Tracking System v-3.0')
root.geometry(str(width_monitor)+'x'+str(height_monitor-100)+'+0+0') 
root.config(bg = Fun_Rgb(C_Primary))
root.isStopped = False

#%%Global variables   
global Lbl_Img_Original, List_Contenido, pathImageProject, textEnt, currentProject, openProjectVar

currentProject = 0                
Lbl_Img_Original = Label(root, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
List_Contenido = []
pathImageProject = ''
currentPicture = 0
openProjectVar = 0

#%%Toolbar and menu
toolbar = Frame(root)

img1 = PIL.Image.open(Dir_Images+'options.png')
useImg1 = ImageTk.PhotoImage(img1)
img2 = PIL.Image.open(Dir_Images+'cut_video.png')
useImg2 = ImageTk.PhotoImage(img2)
img3 = PIL.Image.open(Dir_Images+'new.png')
useImg3 = ImageTk.PhotoImage(img3)
img4 = PIL.Image.open(Dir_Images+'open.png')
useImg4 = ImageTk.PhotoImage(img4)
# img5 = PIL.Image.open(Dir_Images+'save.png')
# useImg5 = ImageTk.PhotoImage(img5)
# img6 = PIL.Image.open(Dir_Images+'new_observation.png')
# useImg6 = ImageTk.PhotoImage(img6)
# img7 = PIL.Image.open(Dir_Images+'open_observation.png')
# useImg7 = ImageTk.PhotoImage(img7)
# img8 = PIL.Image.open(Dir_Images+'data.png')
# useImg8 = ImageTk.PhotoImage(img8)
# img9 = PIL.Image.open(Dir_Images+'user.png')
# useImg9 = ImageTk.PhotoImage(img9)


iconTool_Options = Button(toolbar, image=useImg1, text="Options", width=20, command=info)
iconTool_Options.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconTool_Options, text = 'Contact information')

iconTool_CutVideo = Button(toolbar, image=useImg2, text="Cut Video", width=20, command=cutVideo)
iconTool_CutVideo.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconTool_CutVideo, text = 'Cut video')

iconNewProject = Button(toolbar, image=useImg3, text="New project", width=20, command=newProjectAux)
iconNewProject.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconNewProject, text = 'New project')

# openFile = Button(toolbar, image=useImg4, text="Open", width=20, command=openProject)
# openFile.pack(side=LEFT, padx=2, pady=2)
# CreateToolTip(openFile, text = 'Open project')

# saveButton = Button(toolbar, image=useImg5, text="Save", width=20, command=saveProject)
# saveButton.pack(side=LEFT, padx=2, pady=2)
# CreateToolTip(saveButton, text = 'Save project')

# iconNewObservation = Button(toolbar, image=useImg6, text="Observation", width=20, command= openProject)
# iconNewObservation.pack(side=LEFT, padx=2, pady=2)
# CreateToolTip(iconNewObservation, text = 'New observation')

# iconOpenObservation = Button(toolbar, image=useImg7, text="Observation", width=20, command= openObservation)
# iconOpenObservation.pack(side=LEFT, padx=2, pady=2)
# CreateToolTip(iconOpenObservation, text = 'Open observation')

# closeButton = Button(toolbar, image=useImg8, text="Data", width=20)#, command=close_WPI_Connection)
# closeButton.pack(side=LEFT, padx=2, pady=2)
# CreateToolTip(closeButton, text = 'Data analysis')

# checkInputButton = Button(toolbar, image=useImg9, text="User", width=20)#, command=check_Input_1)
# checkInputButton.pack(side=LEFT, padx=2, pady=2)
# CreateToolTip(checkInputButton, text = 'User information')



toolbar.pack(side=TOP, fill=X)

menubar = tkinter.Menu(root)
root.config(menu=menubar)

Menu_Opc1 = tkinter.Menu(root, bg=Fun_Rgb(C_White), fg=Fun_Rgb(C_Primary),
                             activebackground=Fun_Rgb(C_Grey), activeforeground=Fun_Rgb(C_Light_Dark),
                             tearoff=0)                         
menubar.add_cascade(label="File", menu=Menu_Opc1)
Menu_Opc1.add_command(label='Cut video', command=cutVideo) 
Menu_Opc1.add_command(label='New project', command = newProjectAux)
# Menu_Opc1.add_command(label='Open project', command = openProject)
# Menu_Opc1.add_command(label='Save project', command = saveProject)
# Menu_Opc1.add_command(label='New observation', command = openProject)
# Menu_Opc1.add_command(label='Open observation', command = openObservation)
Menu_Opc1.add_command(label='Data analysis')
Menu_Opc1.add_command(label='User information')
Menu_Opc1.add_command(label='License', command=info)  

#%%Notebooks
style = ttk.Style()
settings = {"TNotebook.Tab": {"configure": {"padding": [100, 10],
                                            "background": Fun_Rgb(C_White)
                                           },
                              "map": {"background": [("selected", Fun_Rgb(C_Primary)), 
                                                     ("active", Fun_Rgb(C_White))],
                                      
                                      "foreground": [("selected", Fun_Rgb(C_White)),
                                                     ("active", "#000000")]

                                     }
                              }
           }  


style.theme_create("mi_estilo", parent="alt", settings=settings)
style.theme_use("mi_estilo")

notebook = ttk.Notebook(root)
notebook.pack(fill = 'both', expand = 'yes')
pesCutVideo = tkinter.Frame(notebook, background = Fun_Rgb(C_Primary))
pesNewProject = tkinter.Frame(notebook, background = Fun_Rgb(C_Dark))
pesTracking = tkinter.Frame(notebook, background = Fun_Rgb(C_Dark))

notebook.add(pesCutVideo, text = '  Cut video', image=useImg4, compound=LEFT)
notebook.add(pesNewProject, text = 'New project')
notebook.add(pesTracking, text= 'Track')

#%%Canvas notebook Pestaña 1
canTittle = Canvas(pesCutVideo, width=int(width_monitor), height=int(aux_height_monitor*14), bg=Fun_Rgb(C_Primary))

canTittle.create_rectangle(int(aux_width_monitor*1.5), int(aux_height_monitor*1.5), int(aux_width_monitor*13.5), int(aux_width_monitor*2), fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=.1)
canTittle.place(x=0,y=0) 

#%%Labels and entries of notebook pesCutVideo         
lblTitle = Label(pesCutVideo, text="Label Tittle 1", bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblTitle.config(font = (Font_1,15))
lblTitle.place(x=aux_width_monitor*1.5, y=aux_height_monitor*1)

var1 = StringVar()

lblSubjects1 = Label(pesCutVideo, text="Label subtittle 1", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblSubjects1.config(font = (Font_1,12))
lblSubjects1.place(x=aux_width_monitor*1.75, y=aux_height_monitor*2)

entSub1 = Entry(pesCutVideo, textvariable = var1, bd =1)
entSub1.place(x=aux_width_monitor*1.75, y=aux_height_monitor*2.5)


#%%Canvas notebook pesNewProject
canNewProject = Canvas(pesNewProject, width=int(width_monitor), height=int(aux_height_monitor*14), bg=Fun_Rgb(C_Primary))

canNewProject.create_rectangle(int(aux_width_monitor*1), int(aux_height_monitor*1), int(aux_width_monitor*8), int(aux_height_monitor*9), fill=Fun_Rgb(C_Dark), outline=Fun_Rgb(C_White), width=.1)
canNewProject.place(x=0,y=0) 

#%%Buttons notebook pesNewProject
btnpesNewProject = tkinter.Button(pesNewProject,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,
    text = 'Button 1', command = info)
btnpesNewProject.config(font = ("Arial",20))
btnpesNewProject.place(x=aux_width_monitor*8.5, y=aux_height_monitor*1)

btnSubj1 = tkinter.Button(pesNewProject, bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = var1, command = info)
btnSubj1.config(font = ("Arial",13))
btnSubj1.place(x=aux_width_monitor*8.8, y=aux_height_monitor*3.5)

#%%Labels in pesPrincipal
lblImage = Label(canNewProject, text='Images', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblImage.config(font = (Font_1,15))
lblImage.place(x=aux_width_monitor*8.5, y=aux_height_monitor*.5)


#%%Sliders in canRegister
Slider_X1 = tkinter.Scale(canNewProject, 
    from_=0, to=1, resolution=0.01,
    orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*7,
    fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
    activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
    highlightbackground=Fun_Rgb(C_White),
    showvalue=1)
Slider_X1.config(font=(Font_1,11))
Slider_X1.place(x=int(aux_width_monitor*1), y=int(aux_height_monitor*.2))


#%%Text space in pesPrincipal
textEnt = Text(canNewProject, width = int(aux_width_monitor*1), height = int(aux_height_monitor*.15))
textEnt.config(font=("Arial",10))
textEnt.place(x=aux_width_monitor*1, y=aux_height_monitor*10)

#%%Mainloop
root.mainloop()



