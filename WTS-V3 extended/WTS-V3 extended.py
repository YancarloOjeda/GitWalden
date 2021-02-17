# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 16:14:56 2020

@author: Walden Modular Equipment (YO and LA)
"""

#%%Libraries 
import tkinter 
import cv2
import os
import os.path
import numpy as np
import serial
import PIL.Image
import scipy
import statistics
import math
from PIL import Image, ImageTk
from ast import literal_eval
from scipy import misc, ndimage
from tkinter import PhotoImage, messagebox, ttk, Canvas, filedialog, Tk, Frame, BOTH
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import font
from tkinter.font import Font
from tkinter.simpledialog import askstring
from screeninfo import get_monitors
from tkinter import Button, Frame, INSERT, LEFT, RIGHT, Label, Checkbutton
from tkinter import  Scrollbar, Text, Tk, TOP, X, Y, filedialog
from tkinter import *
import cv2
from screeninfo import get_monitors
import time
import pytube
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import imageio

#%%-------------GENERAL FUNCTIONS-------------
#%%Settings
fileSettings = open('settings.txt', 'r')
arrSettings = fileSettings.read().split('\n')
fileSettings.close()

theme = int(arrSettings[0])
showTextImage = int(arrSettings[1])
themeAux = theme
showTextImageAux = showTextImage
#%%Colors 
if theme == 1:
    C_Primary = (21,21,21)
    C_Light_Dark = (48,48,48)
    C_White = (255,255,255)
    C_Dark = (0,0,0)
    C_Grey = (200,200,200)
    C_Red = (255,0,0)
    Font_CV = cv2.FONT_HERSHEY_SIMPLEX
    Font_1 = 'Sans'
elif theme == 0:
    C_Primary = (200,200,200)
    C_Light_Dark = (148,148,148)
    C_White = (0,0,0)
    C_Dark = (255,255,255)
    C_Grey = (100,100,100)
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
Dir_ConfigFiles = 'Config/'
Dir_Videos = 'Videos/'
Dir_Project_Images = '/Images/'
Dir_Datos = 'Data/'

if os.path.exists(Dir_ConfigFiles):
    os.path.exists(Dir_ConfigFiles)
else:
    os.mkdir(Dir_ConfigFiles)

if os.path.exists(Dir_Datos):
    os.path.exists(Dir_Datos)
else:
    os.mkdir(Dir_Datos)
    
if os.path.exists(Dir_Videos):
    os.path.exists(Dir_Videos)
else:
    os.mkdir(Dir_Videos)
#%%Global variables
global var1, Seleccion_Camara, Seleccion_Resolucion, Dev_WebCam_Resolution, Seleccion_Track
global arr_Color_Cuadro, arr_Color_Cuadro1, arr_Color_Cuadro2 
arr_Color_Cuadro = np.zeros(4)
arr_Color_Cuadro1 = np.zeros(4)
arr_Color_Cuadro2 = np.zeros(4)
Seleccion_Camara = 0 
Seleccion_Resolucion = 1
Dev_WebCam_Resolution=(480,320)
Seleccion_Track = 0
global number_subject, Mat_RGB 
Mat_RGB = np.zeros((16,6))
number_subject = 0
global auxColors, auxColorCircleCanvas, auxColorR, auxColorG, auxColorB
auxColors = 0
auxColorR = 255
auxColorG = 255
auxColorB = 255
auxColorCircleCanvas = 0 
global Lbl_Img_Original, List_Contenido, pathImageProject, textEnt, currentProject, openProjectVar, lblVideo
currentProject = 0                
List_Contenido = []
pathImageProject = ''
currentPicture = 0
openProjectVar = 0
global pathDirectoryTrack
pathDirectoryTrack = ''
#%%Windows size
auxEvaluar = 0
try:
    for monitor in get_monitors():
        if auxEvaluar == 0:
            monitor_size = monitor
            aux_string_monitor = str(monitor_size)
            aux_cortar = aux_string_monitor.split('Monitor(')
            aux_cortar = aux_cortar[1].split(')')
            parameters_monitor = aux_cortar[0].split('width=')
            parameters_monitor = parameters_monitor[1].split(', height=')
            width_monitor = int(parameters_monitor[0])
            parameters_monitor = parameters_monitor[1].split(', width_mm=')
            height_monitor = int(parameters_monitor[0])
            # print(width_monitor, height_monitor)
            auxEvaluar += 1
            aux_size = 1.9
except:
    width_monitor = 1280
    height_monitor = 800
    aux_size = .75
    
aux_width_monitor = width_monitor/15 
aux_height_monitor = height_monitor/15
# print(width_monitor, height_monitor)
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
                      font=("tahoma", "12", "normal"))
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
#%%Fun ordenarAlfabeticamente
def ordenarAlfabeticamente(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
#%%Fun Fun_Get_RGB
def Fun_Get_RGB():
    global Dir_Videos
    Main_Dir_Image = filedialog.askopenfilename(initialdir = Dir_Videos,
                                                title = "Select Image",
                                                filetypes = (("jpg files","*.jpg"),
                                                              ("all files","*.*"))) 
    Get_Image = mpimg.imread(Main_Dir_Image)
    plt.imshow(Get_Image)
    plt.show() 
#%%Fun printSettings
def printSettings(x):
    global winSettings, themeAux, showTextImageAux
    fileSettings = open('settings.txt', 'r')
    arrSettings = fileSettings.read().split('\n')
    fileSettings.close()
    
    theme = int(arrSettings[0])
    showTextImage = int(arrSettings[1])
    
    if x == 1:
        if theme == 0:
            themeAux = 1
        else:
            themeAux = 0
    elif x == 2:
        if showTextImage == 0:
            showTextImageAux = 1
        else:
            showTextImageAux = 0      
            
    if x == 3:
        fileSettings = open('settings.txt', 'w')
        fileSettings.write(str(themeAux) + '\n')
        fileSettings.write(str(showTextImageAux) +'\n')
        fileSettings.close()    
        destroyAllWindows = messagebox.askyesno("Restart WTS","Would you like to restart now?")
        winSettings.destroy()                    
        if destroyAllWindows == True:
            root.destroy()
#%%Fun openSettings
def openSettings():
    global winSettings
    winSettings = Tk()
    winSettings.title('Walden Tracking System v-3.0')
    winSettings.geometry(str(int(aux_width_monitor*8))+'x'+str(int(aux_height_monitor*8))+'+'+
              str(int(aux_width_monitor*3.5))+'+'+str(int(aux_height_monitor*3.5))) 
    winSettings.iconbitmap(Dir_Images+"Icon.ico")
    winSettings.resizable(0,0)
    winSettings.config(bg = Fun_Rgb(C_Light_Dark))
    winSettings.isStopped = False
    
    varAux = IntVar()
    varAux2 = IntVar()
    
    lblDownloads = tkinter.Label(winSettings, text="Select default parameters", 
                                 background=Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White), borderwidth=1,
                                 font = ("Arial",18, "normal"))
    lblDownloads.place(x=aux_width_monitor * .2, y=aux_height_monitor*.5)
    
    R1 = Radiobutton(winSettings, bg=Fun_Rgb(C_Light_Dark), activebackground=Fun_Rgb(C_Primary), indicatoron=0, bd = 0,
        text="Dark theme", variable=varAux, value=1, command=lambda: printSettings(1))
    R1.config(font=('Arial', 12))
    R1.place(x=aux_width_monitor*.3, y=aux_height_monitor*1.2)
    
    R2 = Radiobutton(winSettings, bg=Fun_Rgb(C_Light_Dark), activebackground=Fun_Rgb(C_Primary), indicatoron=0, bd = 0,
        text="Show time in videos", variable=varAux2, value=2, command=lambda: printSettings(2))
    R2.config(font=('Arial', 12))
    R2.place(x=aux_width_monitor*.3, y=aux_height_monitor*1.9)
    
    
    btnNext = tkinter.Button(winSettings,  bd=0, fg = Fun_Rgb(C_White),
                bg = Fun_Rgb(C_Primary), activebackground=Fun_Rgb(C_Light_Dark),
                highlightbackground=Fun_Rgb(C_Grey),
                text = 'Finish', command = lambda: printSettings(3))
    btnNext.config(font = ("Arial",15))
    btnNext.place(x=aux_width_monitor*7, y=aux_height_monitor*7)
#%%-------------GENERAL FUNCTIONS------------- 
#%%Fun info
def info():
    messagebox.showinfo('WTS-V3','Software developed by Walden Modular Equipment')

def newProjectAux():
    messagebox.showinfo('WTS-V3','In construction')
#%%Fun_Image_Rezice  
def Fun_Image_Rezice(img):
    # Var_Tamaño_Lbl_X = int(((height_monitor/2)*1.99)-(aux_width_monitor*1.4))
    # Var_Tamaño_Lbl_Y = int(((height_monitor/2)*1.37)-(aux_width_monitor*1.3))
    Var_Tamaño_Lbl_X = int(aux_width_monitor*7)-2
    Var_Tamaño_Lbl_Y = int(aux_height_monitor*8)-2
    
    Img_Original = img
    if int(Img_Original.size[0])>=Var_Tamaño_Lbl_X:
        Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))))
        if int(Img_Original_2.size[1]) >= Var_Tamaño_Lbl_Y:
            Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y))
    elif int(Img_Original.size[1])>=Var_Tamaño_Lbl_Y:
        Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y))
        if int(Img_Original_2.size[0]) >= Var_Tamaño_Lbl_X:
            Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))))
    else:
        Img_Original_2 = Img_Original
        #La siguiente linea reajusta la imagen al tamaño del canvas 
        # Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,Var_Tamaño_Lbl_Y))
        
    return(Img_Original_2)
#%%Fun imageRezicePesNewProject
def imageRezicePesNewProject(img):
    # Var_Tamaño_Lbl_X = int(aux_width_monitor*3.25)-2
    # Var_Tamaño_Lbl_Y = int(aux_height_monitor*4.7)-2
    Var_Tamaño_Lbl_X = int(aux_width_monitor*7)-2
    Var_Tamaño_Lbl_Y = int(aux_height_monitor*8)-2
    
    print(Var_Tamaño_Lbl_X, Var_Tamaño_Lbl_Y)
    Img_Original = img 
    print(Img_Original.size[0], Img_Original.size[1])
    
    if int(Img_Original.size[0])>=Var_Tamaño_Lbl_X:
        Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))))
        if int(Img_Original_2.size[1]) >= Var_Tamaño_Lbl_Y:
            Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y))
    elif int(Img_Original.size[1])>=Var_Tamaño_Lbl_Y:
        Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y))
        if int(Img_Original_2.size[0]) >= Var_Tamaño_Lbl_X:
            Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))))
    else:
        Img_Original_2 = Img_Original
        #La siguiente linea reajusta la imagen al tamaño del canvas 
        # Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,Var_Tamaño_Lbl_Y))
   
        
    return(Img_Original_2)    
#%%Fun changeCamera
def Fun_Change_Camera():
    global Seleccion_Camara
    Seleccion_Camara += 1
    lblNumberCamera = Label(pesCutVideo, text=str(Seleccion_Camara), bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
    lblNumberCamera.config(font = (Font_1,20))
    lblNumberCamera.place(x=aux_width_monitor*12, y=aux_height_monitor*6.2)
    if Seleccion_Camara == 5:
        Seleccion_Camara =  -1           
#%%FunSetResolution (radiobuttons)
def FunSetResolution():
    global Seleccion_Resolucion, Dev_WebCam_Resolution
    Seleccion_Resolucion = opcion.get()
    Dev_WebCam_Resolution = Seleccion_Resolucion
    
    if Dev_WebCam_Resolution == 1:
        Dev_WebCam_Resolution=(480,320)
    elif Dev_WebCam_Resolution == 2:
        Dev_WebCam_Resolution=(600,480)
    elif Dev_WebCam_Resolution == 3:
        Dev_WebCam_Resolution=(800,600)
    elif Dev_WebCam_Resolution == 4:
        Dev_WebCam_Resolution=(1280,800) 
#%%FunSetResolution
def FunSetResolutionParameter(Seleccion_Resolucion, Seleccion_Camara):
    # global Seleccion_Resolucion, Dev_WebCam_Resolution, Seleccion_Camara
    Dev_WebCam_Resolution = Seleccion_Resolucion
    
    Dev_WebCam_Read = cv2.VideoCapture(Seleccion_Camara)
    if Dev_WebCam_Resolution == 1:
        Dev_WebCam_Resolution=(320,200)
    elif Dev_WebCam_Resolution == 2:
        Dev_WebCam_Resolution=(480,320)
    elif Dev_WebCam_Resolution == 3:
        Dev_WebCam_Resolution=(600,480)
    elif Dev_WebCam_Resolution == 4:
        Dev_WebCam_Resolution=(800,600)
    elif Dev_WebCam_Resolution == 5:
        Dev_WebCam_Resolution=(1280,800)   
    Dev_WebCam_Read.set(3,Dev_WebCam_Resolution[0])
    Dev_WebCam_Read.set(4,Dev_WebCam_Resolution[1])
    
    
    # if Dev_WebCam_Resolution == 1:
    #     Dev_WebCam_Resolution=(480,320)
    # elif Dev_WebCam_Resolution == 2:
    #     Dev_WebCam_Resolution=(600,480)
    # elif Dev_WebCam_Resolution == 3:
    #     Dev_WebCam_Resolution=(800,600)
    # elif Dev_WebCam_Resolution == 4:
    #     Dev_WebCam_Resolution=(1280,800) 
        
    return Dev_WebCam_Read
#%%-------------VIDEO AND IMAGES FUNCTIONS------------- 
#%%Fun openImage 
def openImage():
    global Lbl_Img_Original, List_Contenido, pathImageProject, currentPicture, Dir_Project_Img
    
    pathVideo = filedialog.askdirectory(initialdir = Dir_Videos,
                                            title = "Select Image Project")
    
    Dir_Project_Img = pathVideo + Dir_Project_Images
    
    textImageProject = pathVideo.split(Dir_Videos)
    textImageProject = textImageProject[1]
    
    if len(textImageProject) >= 30:
        lblImageProject = Label(pesCutVideo, text='Project: '+textImageProject[:30] + '...', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))     
    else:
        lblImageProject = Label(pesCutVideo, text='Project: '+textImageProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
    
    lblImageProject.config(font = (Font_1,15))
    lblImageProject.place(x=aux_width_monitor*8.5, y=aux_height_monitor*9.2)
    CreateToolTip(lblImageProject, text = textImageProject)
    
    setImage()
#%%Fun Set image
def setImage():
    global Lbl_Img_Original, List_Contenido, pathImageProject, currentPicture, Dir_Project_Img, lblNumberImage
    
    currentPicture = 0
    
    List_Contenido = ordenarAlfabeticamente(os.listdir(Dir_Project_Img))
    
    img = Dir_Project_Img+str(List_Contenido[currentPicture])
    
    lblNumberImage.place_forget()
    
    lblNumberImage = Label(pesCutVideo, text='Image '+str(currentPicture+1)+ ' of '+str(len(List_Contenido)) +'   ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
    lblNumberImage.config(font = (Font_1,15))
    lblNumberImage.place(x=aux_width_monitor*1, y=aux_height_monitor*9.1)
       
    Lbl_Img_Original.place_forget()
    Img_Original = PIL.Image.open(img)
    Img_Original_2 = Fun_Image_Rezice(Img_Original)
    
    Photo_Img_Original = ImageTk.PhotoImage(Img_Original_2)
    Lbl_Img_Original = tkinter.Label(pesCutVideo, image=Photo_Img_Original, bg = Fun_Rgb(C_Primary), bd = 0)
    Lbl_Img_Original.image = Photo_Img_Original
    Lbl_Img_Original.place(x = (aux_width_monitor*1)+1, y = (aux_height_monitor*1)+1)
    
    return List_Contenido, pathImageProject    
#%%Fun Cut video
def cutVideo():
    global var1, rateVideo, pathVideo, Dir_Project_Img
    
    if pathVideo =='':
        mensaje1 = messagebox.showerror(message= "You have to select a video to cut", title="Warning")
    else:
        try:
            entRate = int(var1.get())
            Captura_Video = cv2.VideoCapture(pathVideo)    
            Rate_Video = round(Captura_Video.get(5)) 
            # videoDuration = (Captura_Video.get(cv2.CAP_PROP_FRAME_COUNT)+1)/Rate_Video
            miliseconds = 1000/Rate_Video
            rateVideo.set("Frames per second in the video: " + str(Rate_Video))
            
            if entRate > int(Rate_Video):
                messagebox.showerror("Error", "Frames per second must not exceed original video frames")
            else:
                Aux_Ent_Frame = round(Rate_Video/entRate)
                Aux_Contador = 1
                
                while(Captura_Video.isOpened()):
                    Id_Frame = Captura_Video.get(1) 
                    ret, Frame = Captura_Video.read()
                    if (Aux_Contador == Aux_Ent_Frame):
                        Ruta_Frame = Dir_Project_Img + "/" +  str(int(round((Id_Frame +1) *miliseconds))) + ".jpg"
                        
                        try:
                            cv2.imwrite(Ruta_Frame, Frame)
                        except:
                            break
                        
                        Aux_Contador = 1
                        if (ret != True):
                            break
                    else:
                        Aux_Contador += 1
                        if (ret != True):
                            break
                    
                Captura_Video.release()
               
                messagebox.showinfo("Finalized", "Video has been cut")
                setImage()
            
        except ValueError:
            mensaje1 = messagebox.showerror(message= "You have to select a number of frames per second", title="Warning")     
#%%Fun Select video  
def SelectVideo():
    global Dir_Project, var1, rateVideo, pathVideo, Dir_Project_Img
    
    try:
        pathVideo = filedialog.askopenfilename(initialdir = Dir_Videos,
                                            title = "Select Video",
                                            filetypes = (("all files","*.*"),
                                            ("mp4 files","*.mp4")))
        
        Captura_Video = cv2.VideoCapture(pathVideo)    
        Rate_Video = round(Captura_Video.get(5))
        videoDuration = (Captura_Video.get(cv2.CAP_PROP_FRAME_COUNT)+1)/Rate_Video
        miliseconds = 1000/Rate_Video
        rate = StringVar()
        rateVideo.set("Frames per second in the video: " + str(Rate_Video) + " select f/s")
        
        try:
            pathNewProject = filedialog.asksaveasfilename(initialdir = Dir_Videos,
                                    title = "Save image project",
                                    filetypes = (("all files","*.*"),
                                    ("jpeg files","*.jpg")))
            
            Dir_Project_Img = pathNewProject + Dir_Project_Images   
            if os.path.exists(pathNewProject):
                os.path.exists(pathNewProject)
                os.mkdir(Dir_Project_Img)
            else:
                os.mkdir(pathNewProject)
                os.mkdir(Dir_Project_Img)
                 
        except:
            mensaje1 = messagebox.showerror(message= "You dont't have a current project. Open a new project", title="Warning")
        
    except:
        mensaje1 = messagebox.showerror(message= "You dont't have a current project. Open a new project", title="Warning")    
#%%Fun changeImage
def changeImage(x):
    global currentPicture, Lbl_Img_Original, text, Dir_Project_Img, lblNumberImage
    
    currentPicture += x
    
    if currentPicture >= len(List_Contenido):
        currentPicture = len(List_Contenido) - 1
    if currentPicture <= 0:
        currentPicture = 0
    
    img = Dir_Project_Img+str(List_Contenido[currentPicture])
    milisecond = img.split(Dir_Project_Img)[1]
    lblNumberImage.place_forget()
    
    lblNumberImage = Label(pesCutVideo, text='Image '+str(currentPicture+1)+ 
                           ' of '+str(len(List_Contenido)) + ' (' + str(milisecond) + ')', 
                           bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
    lblNumberImage.config(font = (Font_1,15))
    lblNumberImage.place(x=aux_width_monitor*1, y=aux_height_monitor*9.1)
        
    Lbl_Img_Original.place_forget()
    Img_Original= PIL.Image.open(img)
    Img_Original_2 = Fun_Image_Rezice(Img_Original)
           
    Photo_Img_Original = ImageTk.PhotoImage(Img_Original_2)
    Lbl_Img_Original = tkinter.Label(pesCutVideo, image=Photo_Img_Original, bg = Fun_Rgb(C_Primary), bd = 0)
    Lbl_Img_Original.image = Photo_Img_Original
    Lbl_Img_Original.place(x = (aux_width_monitor*1)+1, y = (aux_height_monitor*1)+1)
#%%Fun Take Video
def Fun_Take_Video():
    global Name_Video, Seleccion_Camara, Dev_WebCam_Resolution
    
    Dev_WebCam_Read = cv2.VideoCapture(Seleccion_Camara)
    Dev_WebCam_Read.set(3,Dev_WebCam_Resolution[0])
    Dev_WebCam_Read.set(4,Dev_WebCam_Resolution[1])
    
    Name_Video = videoName.get()
    if Name_Video == '':
        messagebox.showerror("Error", "Video name not assigned")   
    else:
        Arr_TiempoReal = np.zeros(4)
        seconds = 0
        minutes = 0
        hours = 0
        
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        out = cv2.VideoWriter(Dir_Videos + Name_Video + '.mp4',fourcc, 30.0, (640,480))
        
        while(True):
            Arr_TiempoReal[0]=time.time() 
            ret, Img_WebCam = Dev_WebCam_Read.read()
            if showTextImage == 1:
                cv2.putText(Img_WebCam, 'Time: ' + str(hours) +' h: ' + str(minutes) +
                            ' m: ' + str(round(seconds, 2)) + ' s', (5, 35), Font_CV, 1, (255, 255, 255))
                  
            if ret==True:
                out.write(Img_WebCam)
                cv2.imshow('Press Esc to abort',Img_WebCam)
                cv2.moveWindow('Press Esc to abort', int(aux_width_monitor*1), int(aux_height_monitor*3.2))
                
                key = cv2.waitKey(1)
                if key == 27:#esc
                    break
                if key == 32:#space
                    cv2.waitKey(-1)
                
            else:
                break
            
            Arr_TiempoReal[1]=time.time()
            Arr_TiempoReal[2]=Arr_TiempoReal[1]-Arr_TiempoReal[0] 
            Arr_TiempoReal[3]+= Arr_TiempoReal[2]
            seconds = Arr_TiempoReal[3]
        
            if seconds >= 60:
                seconds = 0
                minutes += 1
                Arr_TiempoReal[3] = 0
                
                if minutes >= 60:
                    hours += 1
                    minutes = 0
                
        Dev_WebCam_Read.release()
        out.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Finalized", "Video has been saved")
#%%Fun_Test_Video
def Fun_Test_Video():
    global Seleccion_Camara, Dev_WebCam_Resolution
    
    Dev_WebCam_Read = cv2.VideoCapture(Seleccion_Camara)
    Dev_WebCam_Read.set(3,Dev_WebCam_Resolution[0])
    Dev_WebCam_Read.set(4,Dev_WebCam_Resolution[1])

    Arr_TiempoReal = np.zeros(4)
    seconds = 0
    minutes = 0
    hours = 0
    while(True):
        Arr_TiempoReal[0]=time.time() 
        ret, Img_WebCam = Dev_WebCam_Read.read()
        if showTextImage == 1:
            cv2.putText(Img_WebCam, 'Time: ' + str(hours) +' h: ' + str(minutes) +
                        ' m: ' + str(round(seconds, 2)) + ' s', (5, 35), Font_CV, 1, (255, 255, 255))
                  
        if ret==True:
            cv2.imshow('Press Esc to abort',Img_WebCam)
            cv2.moveWindow('Press Esc to abort', int(aux_width_monitor*1), int(aux_height_monitor*3.2))
            
            key = cv2.waitKey(1)
            if key == 27:
                break
            if key == 32:#space
                cv2.waitKey(-1)
        else:
            break
        
        Arr_TiempoReal[1]=time.time()
        Arr_TiempoReal[2]=Arr_TiempoReal[1]-Arr_TiempoReal[0] 
        Arr_TiempoReal[3]+= Arr_TiempoReal[2]
        seconds = Arr_TiempoReal[3]
        if seconds >= 60:
            seconds = 0
            minutes += 1
            Arr_TiempoReal[3] = 0
            
            if minutes >= 60:
                hours += 1
                minutes = 0
             
    Dev_WebCam_Read.release()
    cv2.destroyAllWindows()  
#%%Fun_Download_Video
def Fun_Download_Video():
    url = entVideoURL.get()
    try:
        youtube = pytube.YouTube(url)
        video = youtube.streams.first()
        video.download(Dir_Videos)
        messagebox.showinfo("Finalized", "Video has been saved")
        openVideo()
    except:
        messagebox.showerror("Error", "Video not found")          
#%%Fun openVideo  
def openVideo():
    global Dir_Project_Img, lblVideo, lblFrames, lblTotalFrames, lblDuration, lblName 
    lblVideo.place_forget()
    
    pathVideo = filedialog.askopenfilename(initialdir = Dir_Videos,
                                            title = "Select Video",
                                            filetypes = (("all files","*.*"),
                                            ("mp4 files","*.mp4")))
    
    Dir_Project_Img = pathVideo + Dir_Project_Images
    
    textImageProject = pathVideo.split(Dir_Videos)
    textImageProject = textImageProject[1]
    
    if len(textImageProject) >= 30:
        lblVideoProject = Label(pesCutVideo, text='Project: '+textImageProject[:30] + '...', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))     
    else:
        lblVideoProject = Label(pesCutVideo, text='Project: '+textImageProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
    
    lblVideoProject.config(font = (Font_1,15))
    lblVideoProject.place(x=aux_width_monitor*8.5, y=aux_height_monitor*11.3)
    CreateToolTip(lblVideoProject, text = textImageProject)
    
    Dev_WebCam_Read = cv2.VideoCapture(pathVideo)
    
    lblFrames.place_forget()
    lblTotalFrames.place_forget()
    lblDuration.place_forget()
    lblName.place_forget()
    
    fps = Dev_WebCam_Read.get(cv2.CAP_PROP_FPS)
    frame_count = int(Dev_WebCam_Read.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    minu = int(duration/60)
    seco = duration%60
    
    lblFrames = Label(pesCutVideo, text='Frames per second: '+ str(round(fps)), bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
    lblFrames.config(font = (Font_1,15))
    lblFrames.place(x=aux_width_monitor*4.6, y = aux_height_monitor*9.8)
    
    lblTotalFrames = Label(pesCutVideo, text='Total frames: '+ str(frame_count), bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
    lblTotalFrames.config(font = (Font_1,15))
    lblTotalFrames.place(x=aux_width_monitor*4.6, y = aux_height_monitor*10.3)
    
    lblDuration = Label(pesCutVideo, text='Duration: ' + str(minu) + ' m :' + str(round(seco)) + ' s', bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
    lblDuration.config(font = (Font_1,15))
    lblDuration.place(x=aux_width_monitor*4.6, y = aux_height_monitor*10.8)
    
    lblName = Label(pesCutVideo, text='Name: ' + textImageProject[:25] + '...', bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
    lblName.config(font = (Font_1,15))
    lblName.place(x=aux_width_monitor*4.6, y = aux_height_monitor*11.3)
    CreateToolTip(lblName, text = textImageProject)
    
    while(True):
        ret, Img_WebCam = Dev_WebCam_Read.read()
        if ret==True:
            cv2.imshow('Press Esc to abort',Img_WebCam)
            cv2.moveWindow('Press Esc to abort', int(aux_width_monitor*1), int(aux_height_monitor*3.2))
            
            time.sleep(0.02)
            key = cv2.waitKey(1)
            if key == 27:
                break
            if key == 32:#space
                cv2.waitKey(-1)
        else:
            break
    
    Dev_WebCam_Read.release()
    cv2.destroyAllWindows()       
#%%-------------NEW PROJECT FUNCTIONS-------------
#%%Fun Color_CuadroRGB
def Fun_Color_CuadroR(Valor):
    global arr_Color_Cuadro, arr_Color_Cuadro1, arr_Color_Cuadro2
    arr_Color_Cuadro[0] = int(Valor)
    Fun_Color_Cuadro()
def Fun_Color_CuadroG(Valor):
    global arr_Color_Cuadro, arr_Color_Cuadro1, arr_Color_Cuadro2
    arr_Color_Cuadro[1] = int(Valor)
    Fun_Color_Cuadro()
def Fun_Color_CuadroB(Valor):
    global arr_Color_Cuadro, arr_Color_Cuadro1, arr_Color_Cuadro2
    arr_Color_Cuadro[2] = int(Valor)   
    Fun_Color_Cuadro()
def Fun_Color_Des(Valor):
    global arr_Color_Cuadro, arr_Color_Cuadro1, arr_Color_Cuadro2
    arr_Color_Cuadro[3] = int(Valor)    
    Fun_Color_Cuadro()
    
def Fun_Color_Cuadro():
    arr_Color_Cuadro1[0] = arr_Color_Cuadro[0] - arr_Color_Cuadro[3] 
    arr_Color_Cuadro1[1] = arr_Color_Cuadro[1] - arr_Color_Cuadro[3] 
    arr_Color_Cuadro1[2] = arr_Color_Cuadro[2] - arr_Color_Cuadro[3] 
    arr_Color_Cuadro2[0] = arr_Color_Cuadro[0] + arr_Color_Cuadro[3] 
    arr_Color_Cuadro2[1] = arr_Color_Cuadro[1] + arr_Color_Cuadro[3] 
    arr_Color_Cuadro2[2] = arr_Color_Cuadro[2] + arr_Color_Cuadro[3] 
    arr_Color_Cuadro1[(arr_Color_Cuadro1<=0)] = 0
    arr_Color_Cuadro2[(arr_Color_Cuadro2>=255)] = 255
    
    Rgb_Can.itemconfig(Cuadro_Rgb1, fill=Fun_Rgb((int(arr_Color_Cuadro[0]),int(arr_Color_Cuadro[1]),int(arr_Color_Cuadro[2]))))
    Rgb_Can.itemconfig(Cuadro_Rgb2, fill=Fun_Rgb((int(arr_Color_Cuadro1[0]),int(arr_Color_Cuadro1[1]),int(arr_Color_Cuadro1[2]))))
    Rgb_Can.itemconfig(Cuadro_Rgb3, fill=Fun_Rgb((int(arr_Color_Cuadro2[0]),int(arr_Color_Cuadro2[1]),int(arr_Color_Cuadro2[2]))))
#%%Fun changeColorAndFilter
def changeColorAndFilter(Img_WebCam, Mat_RGB, Img_Filtro):
    Mat_WebCam_RGB = np.zeros((Img_WebCam.shape))
    Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,0]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[0]+Mat_RGB[3])))[0]),
                   (np.where((Img_WebCam[:,:,0]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[0]+Mat_RGB[3])))[1]),0] = 1
    Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[0]),
                   (np.where((Img_WebCam[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[1]),1] = 1
    Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,2]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[2]+Mat_RGB[3])))[0]),
                   (np.where((Img_WebCam[:,:,2]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[2]+Mat_RGB[3])))[1]),2] = 1          
    Img_WebCam = Mat_WebCam_RGB   
                
    if Img_Filtro==1:
        Img_WebCam = ndimage.gaussian_filter(Img_WebCam, sigma=3)
    elif Img_Filtro==2:
        Img_WebCam = ndimage.gaussian_filter(Img_WebCam, sigma=5)
    elif Img_Filtro==3:
        Img_WebCam =ndimage.uniform_filter(Img_WebCam, size=2)
    elif Img_Filtro==4:
        Img_WebCam =ndimage.uniform_filter(Img_WebCam, size=11)
    elif Img_Filtro==5:
        Img_WebCam = Img_WebCam
    np.place(Img_WebCam[:,:,:], Img_WebCam[:,:,:]>=Mat_RGB[4], 1)
    np.place(Img_WebCam[:,:,:], Img_WebCam[:,:,:]<Mat_RGB[4], 0)
    
    return(Img_WebCam)

#%%Fun newVideoProject
def newVideoProject():
    global Seleccion_Track, Ruta_Imagen, Dialog_Video_File_Aux, Ruta_Proyecto, Ruta_Video, Carpeta_Imagenes, Ruta_Carpeta_Imagenes, Nombre_Archivo, Lbl_Img_Original, Img_Original_2
    global Img_Original       
    
    Seleccion_Track = 1
    
    Ruta_Imagen = filedialog.askopenfilename(initialdir=Dir_Videos,
                                             title="Select Image",
                                             filetypes=(("jpg files","*.jpg"),
                                             ("all files","*.*")))
    
    Dialog_Video_File_Aux = Ruta_Imagen.replace(Ruta_Imagen.split('/')[(np.size(Ruta_Imagen.split('/')))-1], 'Aux_Image.jpg')
    Ruta_Proyecto = Dir_Videos
    Len_Ruta_Proyecto = len(Ruta_Proyecto)
    posicionCarpeta = (Ruta_Imagen[Len_Ruta_Proyecto:].find('/'))
    Ruta_Video = Ruta_Imagen[:Len_Ruta_Proyecto+posicionCarpeta]
    Carpeta_Imagenes ='/Images/'
    Ruta_Carpeta_Imagenes = Ruta_Video + Carpeta_Imagenes
    Nombre_Archivo = Ruta_Imagen.split('/')[(np.size(Ruta_Imagen.split('/')))-3]

    Lbl_Img_Original.place_forget()
    Img_Original= PIL.Image.open(Ruta_Imagen)
    Img_Original_2 = imageRezicePesNewProject(Img_Original)
           
    Photo_Img_Original = ImageTk.PhotoImage(Img_Original_2)
    Lbl_Img_Original = tkinter.Label(pesNewProject, image=Photo_Img_Original, bg = Fun_Rgb(C_Primary), bd = 0)
    Lbl_Img_Original.image = Photo_Img_Original
    Lbl_Img_Original.place(x = (aux_width_monitor*1), y = (aux_height_monitor*1)+1)
    
    updateSeleccionTrackVideo()
#%%Fun getValuesSliders
def getValuesSliders(value):
    global Dialog_Video_File_Aux, Lbl_Img_Original, Dialog_Video_File_Aux_2, Img_Original
    global Ruta_Imagen, Seleccion_Track
    global LblXAxis, LblYAxis
    
    X1 = Slider_X1.get()
    X2 = Slider_X2.get()
    Y1 = Slider_Y1.get()
    Y2 = Slider_Y2.get()
    Rotar = Slider_Grados_Rotar.get()
    
    textEntryX = Etr_Tamano_Caja.get()
    textEntryY = Etr2_Tamano_Caja.get()
    
    LblXAxis.place_forget()
    LblXAxis = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                             text = textEntryX)
    LblXAxis.config(font = (Font_1,12))
    LblXAxis.place(x=aux_width_monitor*5.5, y=aux_height_monitor*11.3)
    
    LblYAxis.place_forget()
    LblYAxis = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                             text = textEntryY)
    LblYAxis.config(font = (Font_1,12))
    LblYAxis.place(x=aux_width_monitor*6.7, y=aux_height_monitor*11.3)
    
    Lbl_Img_Original.place_forget()
    
    Var_R = Slider_Rojo.get()
    Var_G = Slider_Verde.get()
    Var_B = Slider_Azul.get()
    Var_Des = Slider_Desviacion.get()
    Var_Umbral = float(Entr_Umbral.get())
    Mat_RGB = ([Var_R, Var_G, Var_B, Var_Des, Var_Umbral])
    Img_Filtro = Var_Filtro.get()
    
    def Fun_Color_CuadroR():
        global arr_Color_Cuadro, arr_Color_Cuadro1, arr_Color_Cuadro2
        arr_Color_Cuadro[0] = int(Var_R)
        Fun_Color_Cuadro()
    def Fun_Color_CuadroG():
        global arr_Color_Cuadro, arr_Color_Cuadro1, arr_Color_Cuadro2
        arr_Color_Cuadro[1] = int(Var_G)
        Fun_Color_Cuadro()
    def Fun_Color_CuadroB():
        global arr_Color_Cuadro, arr_Color_Cuadro1, arr_Color_Cuadro2
        arr_Color_Cuadro[2] = int(Var_B)   
        Fun_Color_Cuadro()
    def Fun_Color_Des():
        global arr_Color_Cuadro, arr_Color_Cuadro1, arr_Color_Cuadro2
        arr_Color_Cuadro[3] = int(Var_Des)    
        Fun_Color_Cuadro()
    
    Fun_Color_CuadroR()
    Fun_Color_CuadroG()
    Fun_Color_CuadroB()
    Fun_Color_Des()
        
    try:
        Img_Original = imageio.imread(Ruta_Imagen)
        Img_Original = Img_Original[round(Img_Original.shape[0]*Y1):round(Img_Original.shape[0]*Y2),
                                    round(Img_Original.shape[1]*X1):round(Img_Original.shape[1]*X2)]
    
        imageio.imsave(Dialog_Video_File_Aux, Img_Original)
        Img_Aux = PIL.Image.open(Dialog_Video_File_Aux).rotate(Rotar)
        
        Img_Aux.save(Dialog_Video_File_Aux)
        
        Dialog_Video_File_Aux_2 = Dialog_Video_File_Aux.replace('Aux_Image', 'Aux_Imagee')
        Img_Cortable = imageio.imread(Dialog_Video_File_Aux)
        Img_Cortable_Aux = Img_Cortable[:, :]
        imageio.imsave(Dialog_Video_File_Aux_2, Img_Cortable_Aux)
        Img_WebCam = np.copy(Img_Cortable_Aux)
        
        Img_WebCam = changeColorAndFilter(Img_WebCam, Mat_RGB, Img_Filtro)
    
        imageio.imsave(Dialog_Video_File_Aux_2, Img_WebCam)
        Img_Cortable_Aux = PIL.Image.open(Dialog_Video_File_Aux_2)
        
        Img_Original_2 = imageRezicePesNewProject(Img_Cortable_Aux)
        
        #Guardar_Axuliar_2
        Img_Cortable_Aux.save(Dialog_Video_File_Aux_2)   
        
        #Mostrar Imagen
        Pho_Img_Cortable_Aux = ImageTk.PhotoImage(Img_Original_2)
        Lbl_Img_Original = tkinter.Label(pesNewProject, image=Pho_Img_Cortable_Aux, bg = Fun_Rgb(C_Primary), bd = 0)
        Lbl_Img_Original.image = Pho_Img_Cortable_Aux 
        Lbl_Img_Original.place(x = (aux_width_monitor*1), y = (aux_height_monitor*1)+1)
    except:
        pass
   
    if value == 'Restart':
        try:
            Lbl_Img_Original.place_forget()
            Img_Original = imageio.imread(Ruta_Imagen)
            Img_Original = Img_Original[round(Img_Original.shape[0]*Y1):round(Img_Original.shape[0]*Y2),
                                        round(Img_Original.shape[1]*X1):round(Img_Original.shape[1]*X2)]
        
            imageio.imsave(Dialog_Video_File_Aux, Img_Original)
            Img_Aux = PIL.Image.open(Dialog_Video_File_Aux).rotate(Rotar)
            
            Img_Original_2 = imageRezicePesNewProject(Img_Aux)       
            Img_Aux.save(Dialog_Video_File_Aux)
            
            Photo_Img_Aux = ImageTk.PhotoImage(Img_Original_2)
            Lbl_Img_Original = tkinter.Label(pesNewProject, image=Photo_Img_Aux, bg = Fun_Rgb(C_Primary), bd = 0)
            Lbl_Img_Original.image = Photo_Img_Aux 
            Lbl_Img_Original.place(x = (aux_width_monitor*1), y = (aux_height_monitor*1)+1)   
        except:
            pass
#%%Fun_Next_Subject
def Fun_Next_Subject(): 
    global number_subject, Mat_RGB, Seleccion_Track
      
    if Seleccion_Track == 0:
        messagebox.showinfo("Error", "Select a traking option")
    
    Var_R = int(Slider_Rojo.get())
    Var_G = int(Slider_Verde.get())
    Var_B = int(Slider_Azul.get())
    Var_Des = int(Slider_Desviacion.get())
    Var_Umbral = float(Entr_Umbral.get())
    Img_Filtro = Var_Filtro.get()
    Mat_RGB2 = ([Var_R, Var_G, Var_B, Var_Des, Var_Umbral, Img_Filtro])
    
    global Lbl_Img_Original, Lbl_Img_Original_Aux
    Lbl_Img_Original.place_forget()
    
    #Direccion_nueva Imagen
    global Dialog_Video_File_Aux_2
    Dialog_Video_File_Aux_2 = Dialog_Video_File_Aux.replace('Aux_Image', 'Aux_Imagee')
    
    #Guardar Imagenes
    Img_Cortable = imageio.imread(Dialog_Video_File_Aux)
    Img_Cortable_Aux = Img_Cortable[:, :]
    imageio.imsave(Dialog_Video_File_Aux_2, Img_Cortable_Aux)
    
    Img_Aux = PIL.Image.open(Dialog_Video_File_Aux)
    Img_Original_2 = imageRezicePesNewProject(Img_Aux)  
    
    #Mostrar Imagen
    Photo_Img_Aux = ImageTk.PhotoImage(Img_Original_2)
    Lbl_Img_Original = tkinter.Label(pesNewProject, image=Photo_Img_Aux, bg = Fun_Rgb(C_Primary), bd = 0)
    Lbl_Img_Original.image = Photo_Img_Aux 
    Lbl_Img_Original.place(x = (aux_width_monitor*1), y = (aux_height_monitor*1)+1) 
    
    Mat_RGB[number_subject][:]= Mat_RGB2
    number_subject += 1 
    
    Slider_Rojo.set(0)
    Slider_Verde.set(0)
    Slider_Azul.set(0)
    Slider_Desviacion.set(0)
    Entr_Umbral.set(.5)
    Var_Filtro.set(0)   
          
#%%Fun saveParameters
def saveParameters():
    global Mat_RGB, number_subject, Dialog_Video_File_Aux_2, Dialog_Video_File_Aux, Ruta_Imagen, Seleccion_Track
    global Dialog_Video_File_Aux, Ruta_Proyecto, Ruta_Video, Carpeta_Imagenes, Ruta_Carpeta_Imagenes, Nombre_Archivo
    
    configFileName = entConfigFile.get()
    
    if Seleccion_Track == 0:
        messagebox.showinfo("Error", "Select a traking option")
    
    if configFileName == '':
        messagebox.showinfo("Info", "Config file name is not assigned")
    
    if Seleccion_Track == 1 or Seleccion_Track == 2:
        plt.rcParams['image.cmap'] = 'gray'
        plt.show()
        X1 = Slider_X1.get()
        X2 = Slider_X2.get()
        Y1 = Slider_Y1.get()
        Y2 = Slider_Y2.get()
        Rotar = Slider_Grados_Rotar.get()
        textEntryX = Etr_Tamano_Caja.get()
        textEntryY = Etr2_Tamano_Caja.get()
        Img_Filtro = Var_Filtro.get()
        Track_MinSize = float(Entr_Valor_Minimo_Animal.get())
        Img_Original = imageio.imread(Dialog_Video_File_Aux)
        Img_Original = Img_Original[round(Img_Original.shape[0]*Y1):round(Img_Original.shape[0]*Y2),
                                    round(Img_Original.shape[1]*X1):round(Img_Original.shape[1]*X2)]
        Img_Original = PIL.Image.open(Dialog_Video_File_Aux).rotate(Rotar)
        Img_WebCam = np.copy(Img_Original)
        try:
            os.remove(Dialog_Video_File_Aux)
            os.remove(Dialog_Video_File_Aux_2)
        except:
            pass
        
        if number_subject == 0:
            Var_R = Slider_Rojo.get()
            Var_G = Slider_Verde.get()
            Var_B = Slider_Azul.get()
            Var_Des = Slider_Desviacion.get()
            Var_Umbral = float(Entr_Umbral.get())
            Mat_RGB = ([Var_R, Var_G, Var_B, Var_Des, Var_Umbral])
        
            #Guardar txt
            Arr_Variables = [str(Seleccion_Camara), str(Seleccion_Resolucion),
                             str(X1), str(X2), str(Y1), str(Y2), str(Rotar), 
                             str(textEntryX), str(textEntryY),  
                             str(Var_R), str(Var_G), str(Var_B),
                             str(Var_Des), str(Var_Umbral), str(Img_Filtro), 
                             str(Track_MinSize), 
                             str(Img_WebCam.shape[1]),str(Img_WebCam.shape[0]), str(number_subject), 
                             str(Seleccion_Track)] 
            
            Archivo_Variables = open(Dir_ConfigFiles + '/' + configFileName +'.txt','w')
            for i in Arr_Variables:
                Archivo_Variables.write(i +'\n')
            Archivo_Variables.close()
                
            messagebox.showinfo("Finalized", "Parameters has been saved")
            
        else:
            Var_R = Slider_Rojo.get()
            Var_G = Slider_Verde.get()
            Var_B = Slider_Azul.get()
            Var_Des = Slider_Desviacion.get()
            Var_Umbral = float(Entr_Umbral.get())
            Img_Filtro = Var_Filtro.get()
            Mat_RGB2 = ([Var_R, Var_G, Var_B, Var_Des, Var_Umbral, Img_Filtro])
    
            Mat_RGB[number_subject][:]= Mat_RGB2
            
            c = 0
            for q in range(len(Mat_RGB)):
                suma = np.sum(Mat_RGB[c][:], axis=0)
                if (suma == 0):
                    Mat_RGB = np.delete(Mat_RGB[:,:], c, axis=0)
                    c = c
                else:
                    c+=1
            
            #Guardar txt
            Arr_R = np.zeros(c)
            Arr_G = np.zeros(c)
            Arr_B = np.zeros(c)
            Arr_Des = np.zeros(c)
            Arr_Umbral = np.zeros(c)
            Arr_Filtro = np.zeros(c)
            
            for aux in range(len(Mat_RGB)):
                Arr_R[aux] = int(Mat_RGB[aux][0])
                Arr_G[aux] = int(Mat_RGB[aux][1])
                Arr_B[aux] = int(Mat_RGB[aux][2])
                Arr_Des[aux] = int(Mat_RGB[aux][3])
                Arr_Umbral[aux] = float(Mat_RGB[aux][4])
                Arr_Filtro[aux] = int(Mat_RGB[aux][5])    
                
            Arr_Variables = [str(Seleccion_Camara), str(Seleccion_Resolucion),
                             str(X1), str(X2), str(Y1), str(Y2), str(Rotar), 
                             str(textEntryX), str(textEntryY), 
                             str(Track_MinSize), 
                             str(Img_WebCam.shape[1]),str(Img_WebCam.shape[0]), 
                             str(number_subject+1), str(Seleccion_Track)]  
            
            Archivo_Variables = open(Dir_ConfigFiles + '/' + configFileName +'.txt','w')
            cont_Grabar = 0
            for j in Arr_Variables:
                Archivo_Variables.write(j +'\n')
                cont_Grabar += 1
                if cont_Grabar == 10:
                    for i in range(len(Arr_R)):
                        Archivo_Variables.write(str(Arr_R[i]) +';')
                    Archivo_Variables.write('\n')
                    for i in range(len(Arr_G)):
                        Archivo_Variables.write(str(Arr_G[i]) +';')
                    Archivo_Variables.write('\n')
                    for i in range(len(Arr_B)):
                        Archivo_Variables.write(str(Arr_B[i]) +';')
                    Archivo_Variables.write('\n')
                    for i in range(len(Arr_Des)):
                        Archivo_Variables.write(str(Arr_Des[i]) +';')
                    Archivo_Variables.write('\n')
                    for i in range(len(Arr_Umbral)):
                        Archivo_Variables.write(str(Arr_Umbral[i]) +';')
                    Archivo_Variables.write('\n')
                    for i in range(len(Arr_Filtro)):
                        Archivo_Variables.write(str(Arr_Filtro[i]) +';')
                    Archivo_Variables.write('\n')
            
            Archivo_Variables.close() 
            messagebox.showinfo("Finalized", "Parameters have been saved")
#%%-------------TRACKING FUNCTIONS-------------
#%%Fun putCircleCanvas
def putCircleCanvas(canShowDataXY, x, y, r, Mat_RGB):
    global auxColors, auxColorCircleCanvas, auxColorR, auxColorG, auxColorB
    auxColorCircleCanvas += 1
    # print(Mat_RGB)
    # colorRGB = (auxColorR, auxColorG, auxColorB)
    try:
        colorRGB = (Mat_RGB[0], Mat_RGB[1], Mat_RGB[2])
        colorCircleCanvas = Fun_Rgb(colorRGB)
    except:
        colorRGB = (int(Mat_RGB[0]), int(Mat_RGB[1]), int(Mat_RGB[2]))
        colorCircleCanvas = Fun_Rgb(colorRGB)
    
    id = canShowDataXY.create_oval(x-r,y-r,x+r,y+r, fill=colorCircleCanvas)
    # canShowDataXY.create_text(x + r*2, y +r*2,fill="darkblue",font="Times 12 bold",
    #                     text=str(auxColorCircleCanvas))

    canShowDataXY.update()    
    return id
#%%Fun clearCanvas
def clearCanvas():
    canShowDataXY.delete("all")
#%%Fun openConfigFile
def openConfigFile():
    global lblConfigFile, pathConfigFile
    pathConfigFile = filedialog.askopenfilename(initialdir=Dir_ConfigFiles,
                                              title="Select Config file",
                                              filetypes=(("txt files","*.txt"),
                                              ("all files","*.*")))
    
    fileName = pathConfigFile.split('/')
    auxlen = len(fileName)
    fileName = fileName[auxlen-1]
    lblConfigFile.place_forget()
    lblConfigFile = Label(pesTracking, text='Config: '+str(fileName), bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
    lblConfigFile.config(font = (Font_1,15))
    lblConfigFile.place(x=aux_width_monitor*1.2, y=aux_height_monitor*10.1)
    return pathConfigFile 
#%%Fun openProjectDirectoryToTrack
def openProjectDirectoryToTrack():
    global pathDirectoryTrack, lblProjectFile 
    pathDirectoryTrack = filedialog.askdirectory(initialdir = Dir_Videos,
                                            title = "Select project")
    directoryName = pathDirectoryTrack.split('/')
    auxlen = len(directoryName)
    directoryName = directoryName[auxlen-1]
    lblProjectFile.place_forget()
    lblProjectFile = Label(pesTracking, text='Project: ' + str(directoryName), bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
    lblProjectFile.config(font = (Font_1,15))
    lblProjectFile.place(x=aux_width_monitor*1.2, y=aux_height_monitor*11.1)
    return pathDirectoryTrack
#%%Fun_Distancia
def Fun_Distancia(x1,x2,y1,y2,DistanciaRelativa):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)*DistanciaRelativa
#%%Fun TrackProject
def TrackProject():
    global pathConfigFile, pathDirectoryTrack
    global radBtnSaveVideo, entTime
    global Mat_Datos_X, Mat_Datos_Y, Mat_Datos_D, Mat_RGB 
#%%------Get parameters---------
    try:
        pathConfigFile
        fileConfig = open(pathConfigFile, 'r')
        arrConfig = fileConfig.read().split('\n')
        fileConfig.close()
        
        Seleccion_Camara = int(arrConfig[0])
        Seleccion_Resolucion = int(arrConfig[1])
        X1 = float(arrConfig[2])
        X2 = float(arrConfig[3]) 
        Y1 = float(arrConfig[4])
        Y2 = float(arrConfig[5])
        Rotar = float(arrConfig[6])
        textEntryX = float(arrConfig[7]) 
        textEntryY = float(arrConfig[8]) 
        Track_MinSize = float(arrConfig[9]) 
        Img_WebCam1 = int(arrConfig[16])
        Img_WebCam0 = int(arrConfig[17])
        number_subject = int(arrConfig[18])
        Seleccion_Track = int(arrConfig[19])
        
        if number_subject == 0:
            Var_R = int(arrConfig[10])
            Var_G = int(arrConfig[11]) 
            Var_B = int(arrConfig[12])
            Var_Des = int(arrConfig[13]) 
            Var_Umbral = float(arrConfig[14])
            Img_Filtro = int(arrConfig[15]) 
            Mat_RGB = ([Var_R, Var_G, Var_B, Var_Des, Var_Umbral])
           
        if number_subject > 0: 
            Mat_Datos_X = np.zeros((9999999,16))
            Mat_Datos_Y = np.zeros((9999999,16))
            Mat_Datos_D = np.zeros((9999999,16))
    
            Mat_RGB = np.zeros((number_subject, 5))
            Img_Filtro = np.zeros((number_subject, 1))
            aux_1 = 0
            f = 0
            for i in arrConfig:
                b = i
                aux_1 += 1
                if aux_1 == 11:
                    list_aux = b
                    c = list_aux.split(';')
                    c = c[:-1]
                    for e in c:
                        Mat_RGB[f][0] = e
                        f += 1
                    f = 0
                if aux_1 == 12:
                    list_aux = b
                    c = list_aux.split(';')
                    c = c[:-1]
                    for e in c:
                        Mat_RGB[f][1] = e
                        f += 1
                    f = 0   
                if aux_1 == 13:
                    list_aux = b
                    c = list_aux.split(';')
                    c = c[:-1]
                    for e in c:
                        Mat_RGB[f][2] = e
                        f += 1
                    f = 0
                if aux_1 == 14:
                    list_aux = b
                    c = list_aux.split(';')
                    c = c[:-1]
                    for e in c:
                        Mat_RGB[f][3] = e
                        f += 1
                    f = 0
                if aux_1 == 15:
                    list_aux = b
                    c = list_aux.split(';')
                    c = c[:-1]
                    for e in c:
                        Mat_RGB[f][4] = e
                        f += 1
                    f = 0
                if aux_1 == 16:
                    list_aux = b
                    c = list_aux.split(';')
                    c = c[:-1]
                    for e in c:
                        Img_Filtro[f][0] = e
                        f += 1
                    f = 0
                
                
                
        timeSession = entTime.get()
        subject = entSubject.get()
        session = entSession.get()
        group = entGroup.get()
        sessionName = entSessionName.get()
        saveVideo = Var_SaveVideo.get()
        showPreview = Var_ShowPreview.get()
        
        if saveVideo != 1:
            saveVideo = 0
        
        Int_Contador = 1
        Int_Datos_Consecuencia = 0
        Int_Contador_Distancia = 0
        Arr_TiempoReal = np.zeros(4)
        Mat_Datos = np.zeros((9999999,6+(number_subject*2)))
    
        LblAxisX = tkinter.Label(pesTracking, bg = Fun_Rgb(C_Primary), fg=Fun_Rgb(C_White), text='X = '+str(textEntryX))
        LblAxisX.config(font = (Font_1,12))
        LblAxisX.place(x=aux_width_monitor*8.5, y = aux_height_monitor*6.3)
        
        LblAxisY = tkinter.Label(pesTracking, bg = Fun_Rgb(C_Primary), fg=Fun_Rgb(C_White), text='Y = '+str(textEntryY))
        LblAxisY.config(font = (Font_1,12))
        LblAxisY.place(x=aux_width_monitor*12.5, y = aux_height_monitor*3)
       
    except NameError:
        messagebox.showerror("Error", "Config file not found") 
    
#%%---- 1.- Image project from cut video     
    if Seleccion_Track == 1 and pathDirectoryTrack != '':
        List_Contenido = ordenarAlfabeticamente(os.listdir(pathDirectoryTrack+'/Images/'))
#%%---- 1.1- Image project from cut video with only one subject   
        if number_subject == 0:
            for elemento in List_Contenido:
                ruta = pathDirectoryTrack + '/Images/'
                documento = ruta + elemento
                
                Img_Original = imageio.imread(documento)
                Img_Original = Img_Original[round(Img_Original.shape[0]*Y1):round(Img_Original.shape[0]*Y2),
                                            round(Img_Original.shape[1]*X1):round(Img_Original.shape[1]*X2)]
                Img_Original = PIL.Image.open(documento).rotate(Rotar)
                Img_WebCam = np.copy(Img_Original)
                Img_WebCam = changeColorAndFilter(Img_WebCam, Mat_RGB, Img_Filtro)
                    
                try:
                    Mat_Centroide = ndimage.label(Img_WebCam)[0]
                    Centroide = scipy.ndimage.measurements.center_of_mass(Img_WebCam, Mat_Centroide, [1])
                    Mat_Size = ndimage.label(Img_WebCam)[0]
                    Size = np.sqrt(scipy.ndimage.measurements.sum(Img_WebCam, Mat_Size, [1]))
                    MinSize = int(np.where(Size == np.min(Size[(Size >= Track_MinSize)]))[0])
                    cv2.circle(Img_WebCam,(int(Centroide[MinSize][1]),int(Centroide[MinSize][0])),2,(0,0,255),5)
                except:
                    Img_WebCam = Img_WebCam
                    
                Img_WebCam = cv2.resize(Img_WebCam,(round(aux_width_monitor*4), round(aux_height_monitor*4))) #round((400/Img_WebCam.shape[1])*Img_WebCam.shape[1])))
                cv2.putText(Img_WebCam,'T: ',(5,15),Font_CV, .5,(255,255,255),1)
                cv2.putText(Img_WebCam,str(round(Mat_Datos[Int_Contador-1][0] ,2)),(20,15),Font_CV, .5,(255,255,255),1)
                cv2.imshow('Tracking',Img_WebCam)
                cv2.moveWindow('Tracking', int(aux_width_monitor*1), int(aux_height_monitor*3.2));
                cv2.waitKey(5)
                
                Mat_Datos[Int_Contador][0] = int(elemento.replace('.jpg',''))  
                try:
                    Mat_Datos[Int_Contador][1] = int(Centroide[MinSize][1])
                    Mat_Datos[Int_Contador][2] = int(Centroide[MinSize][0])
                except:
                    Mat_Datos[Int_Contador][1] = Mat_Datos[Int_Contador-1][1]
                    Mat_Datos[Int_Contador][2] = Mat_Datos[Int_Contador-1][2]
                Mat_Datos[Int_Contador][4] = Int_Datos_Consecuencia
                Mat_Datos[Int_Contador][3] = (Fun_Distancia(Mat_Datos[Int_Contador-1][1],Mat_Datos[Int_Contador][1],Mat_Datos[Int_Contador-1][2],Mat_Datos[Int_Contador][2],textEntryX/Img_WebCam1))
                
                if showPreview == 1:
                    X_ = (Mat_Datos[Int_Contador][1]*100)/Img_WebCam1
                    X_ = (aux_height_monitor*7)*(X_*.01)
                    
                    Y_ = (Mat_Datos[Int_Contador][2]*100)/Img_WebCam0
                    Y_ = (aux_height_monitor*5)*(Y_*.01)
                    putCircleCanvas(canShowDataXY, X_, Y_,5,Mat_RGB)
                
                Int_Contador += 1 
                
            cv2.destroyAllWindows()
            
            Mat_Datos = np.delete(Mat_Datos,np.where(Mat_Datos[:,1] == 0), axis=0) 
            Mat_Datos[0,3] = 0
            Mat_Datos[0,5] = 0
                                              
            i = 1
            Archivo_Mat_Datos = open(Dir_Datos + sessionName + '.txt','w')
            Archivo_Mat_Datos.write('Subject: ' + subject + '\n' +
                                    'Session: ' + session + '\n' +
                                    'Group: ' + group + '\n' +
                                    'Time: '+ str(round(max(Mat_Datos[:,0]),3)) + '\n' +
                                    'Consecuences: ' + str(np.size(np.where(Mat_Datos[:,4] == 1))) + '\n' +
                                    'Distance: ' + str(round(sum(Mat_Datos[:,3]),3)) + 'cm' + '\n' +
                                    'Velocity: ' + str(round(sum(Mat_Datos[:,3])/max(Mat_Datos[:,0]),3)) + 'cm/seg' + '\n' +
                                    '\n' + 'Frame;Time;X;Y;Aceleration;Distance;Consecuences' + '\n')
            for i in range(0,len(Mat_Datos)): 
                Archivo_Mat_Datos.write(str(i) + ',' + str(round(Mat_Datos[i][0],3)) +
                                                 ',' + str(round(Mat_Datos[i][1] * (textEntryX/Img_WebCam1),3)) +
                                                 ',' + str(round(Mat_Datos[i][2] * (textEntryY/Img_WebCam0),3)) +
                                                 ',' + str(round(Mat_Datos[i][3],3)) +
                                                 ',' + str(Mat_Datos[i][4]) + '\n')
            Archivo_Mat_Datos.close() 
            messagebox.showinfo("Finalized", "Video has been traked")
#%%---- 1.2- Image project from cut video with more than one subject         
        else:
            for elemento in List_Contenido:
                ruta = pathDirectoryTrack + '/Images/'
                documento = ruta + elemento
                
                Img_Original = imageio.imread(documento)
                Img_Original = Img_Original[round(Img_Original.shape[0]*Y1):round(Img_Original.shape[0]*Y2),
                                            round(Img_Original.shape[1]*X1):round(Img_Original.shape[1]*X2)]
                Img_Original = PIL.Image.open(documento).rotate(Rotar)
                Img_WebCam = np.copy(Img_Original)
                
                image_total= np.zeros((Img_WebCam.shape))
                
                i=0
                for i in range(number_subject):
                    image_aux = np.zeros((Img_WebCam.shape))
                    image_aux[(np.where((Img_WebCam[:,:,0]>=(Mat_RGB[i][0]-Mat_RGB[i][3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[i][0]+Mat_RGB[i][3])))[0]),
                              (np.where((Img_WebCam[:,:,0]>=(Mat_RGB[i][0]-Mat_RGB[i][3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[i][0]+Mat_RGB[i][3])))[1]),0] = 1
                    image_aux[(np.where((Img_WebCam[:,:,1]>=(Mat_RGB[i][1]-Mat_RGB[i][3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[i][1]+Mat_RGB[i][3])))[0]),
                              (np.where((Img_WebCam[:,:,1]>=(Mat_RGB[i][1]-Mat_RGB[i][3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[i][1]+Mat_RGB[i][3])))[1]),1] = 1
                    image_aux[(np.where((Img_WebCam[:,:,2]>=(Mat_RGB[i][2]-Mat_RGB[i][3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[i][2]+Mat_RGB[i][3])))[0]),
                              (np.where((Img_WebCam[:,:,2]>=(Mat_RGB[i][2]-Mat_RGB[i][3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[i][2]+Mat_RGB[i][3])))[1]),2] = 1
        
                    if Img_Filtro[i][0]==1:
                        image_aux = ndimage.gaussian_filter(image_aux, sigma=3)
                    elif Img_Filtro[i][0]==2:
                        image_aux = ndimage.gaussian_filter(image_aux, sigma=5)
                    elif Img_Filtro[i][0]==3:
                        image_aux =ndimage.uniform_filter(image_aux, size=2)
                    elif Img_Filtro[i][0]==4:
                        image_aux =ndimage.uniform_filter(image_aux, size=11)
                    elif Img_Filtro[i][0]==5:
                        image_aux = image_aux
                    np.place(image_aux[:,:,:], image_aux[:,:,:]>=Mat_RGB[i][4], 1)
                    np.place(image_aux[:,:,:], image_aux[:,:,:]<Mat_RGB[i][4], 0)
                    
                    try:
                        Mat_Centroide = ndimage.label(image_aux)[0]
                        Centroide = scipy.ndimage.measurements.center_of_mass(image_aux, Mat_Centroide, [1,2,3])
                        Mat_Size = ndimage.label(image_aux)[0]
                        Size = np.sqrt(scipy.ndimage.measurements.sum(image_aux, Mat_Size, [1,2,3]))
                        MinSize = int(np.where(Size == np.min(Size[(Size >= Track_MinSize)]))[0])
                        cv2.circle(image_aux,(int(Centroide[MinSize][1]),int(Centroide[MinSize][0])),2,(0,0,255),5)
                    except:
                        image_aux = image_aux
                    
                    try:
                        Mat_Datos_X[Int_Contador][i] = int(Centroide[MinSize][1])
                        Mat_Datos_Y[Int_Contador][i] = int(Centroide[MinSize][0])
                    except:
                        Mat_Datos_X[Int_Contador][i] = Mat_Datos_X[Int_Contador-1][i]
                        Mat_Datos_Y[Int_Contador][i] = Mat_Datos_Y[Int_Contador-1][i]
                    Mat_Datos_D[Int_Contador][i] = (Fun_Distancia(Mat_Datos_X[Int_Contador-1][i],Mat_Datos_X[Int_Contador][i],Mat_Datos_Y[Int_Contador-1][i],Mat_Datos_Y[Int_Contador][i],textEntryX/Img_WebCam1))    
                    
                    if showPreview == 1:
                        X_ = (Mat_Datos_X[Int_Contador][i]*100)/Img_WebCam1
                        X_ = (aux_height_monitor*7)*(X_*.01)
                        
                        Y_ = (Mat_Datos_Y[Int_Contador][i]*100)/Img_WebCam0
                        Y_ = (aux_height_monitor*5)*(Y_*.01)
                        putCircleCanvas(canShowDataXY, X_, Y_,5, Mat_RGB[i][:])
                      
                    image_total += image_aux
                    if i == number_subject -1:
                        j = 0
                        for j in range(number_subject):
                            cv2.putText(image_total,str(j+1),(int(Mat_Datos_X[Int_Contador][j])+10,int(Mat_Datos_Y[Int_Contador][j])),Font_CV, .5,(0,0,255),1)
                        image_total = cv2.resize(image_total,(round(aux_width_monitor*4), round(aux_height_monitor*4))) 
                        cv2.putText(image_total,'T: ',(5,15),Font_CV, .5,(255,255,255),1)
                        cv2.putText(image_total,str(round(Mat_Datos[Int_Contador-1][0] ,2)),(20,15),Font_CV, .5,(255,255,255),1)
                        cv2.imshow('Tracking',image_total)
                        cv2.moveWindow('Tracking', int(aux_width_monitor*1), int(aux_height_monitor*3.2));
                        cv2.waitKey(5)
                    
                    # Mat_Datos[Int_Contador][0] = (int(elemento.replace('image_','').replace('.jpg',''))/int(Int_Frame_2)) * float(Int_Frame)     
                    Mat_Datos[Int_Contador][0] = int(elemento.replace('.jpg',''))
                Mat_Datos[Int_Contador][4] = Int_Datos_Consecuencia
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break  
                
                Int_Contador += 1   
                
            cv2.destroyAllWindows()
            
            Mat_Datos = np.delete(Mat_Datos,np.where(Mat_Datos[:,0] == 0), axis=0)
            Mat_Datos_X = Mat_Datos_X[0:len(Mat_Datos),:]
            Mat_Datos_Y = Mat_Datos_Y[0:len(Mat_Datos),:]
            Mat_Datos_D = Mat_Datos_D[0:len(Mat_Datos),:]
              
            j = 0
            for j in range(number_subject):
                Archivo_Mat_Datos = open(Dir_Datos + sessionName + '_' + str(j+1) + '.txt','w')
                Archivo_Mat_Datos.write('Subject: ' + subject + '_' + str(j+1) +'\n' +
                                        'Session: ' + session + '\n' +
                                        'Group: ' + group + '\n' +
                                        'Time: '+ str(round(max(Mat_Datos[:,0]),3)) + '\n' +
                                        'Consecuences: ' + str(np.size(np.where(Mat_Datos[:,4] == 1))) + '\n' +
                                        'Distance: ' + str(round(sum(Mat_Datos_D[:,j]),3)) + 'cm' + '\n' +
                                        'Velocity: ' + str(round(sum((Mat_Datos_D[:,j]/100)/Mat_Datos[:,0]),3)) + 'cm/seg' + '\n' +
                                        '\n' + 'Frame;Time;X;Y;Distance;Consecuences' + '\n')
                i = 1
                for i in range(0,len(Mat_Datos)): 
                    Archivo_Mat_Datos.write(str(i) + ',' + str(round(Mat_Datos[i][0],3)) +
                                                     ',' + str(round(Mat_Datos_X[i][j] * (textEntryX/Img_WebCam1),3)) +
                                                     ',' + str(round(Mat_Datos_Y[i][j] * (textEntryY/Img_WebCam0),3)) +
                                                     ',' + str(round(Mat_Datos_D[i][j],3)) +
                                                     ',' + str(Mat_Datos[i][4]) + '\n')
                Archivo_Mat_Datos.close()
            messagebox.showinfo("Finalized", "Sesion has been traked")    
#%%---- 2.-Live project (from camera) 
    elif (Seleccion_Track == 1 or Seleccion_Track == 2) and pathDirectoryTrack == '':
        Mat_Datos[:,0] = -1
        
        Dev_WebCam_Resolution = Seleccion_Resolucion
        Dev_WebCam_Resolution = 3
        Dev_WebCam_Read = cv2.VideoCapture(Seleccion_Camara) 
        if Dev_WebCam_Resolution == 1:
            Dev_WebCam_Resolution=(320,200)
        elif Dev_WebCam_Resolution == 2:
            Dev_WebCam_Resolution=(480,320)
        elif Dev_WebCam_Resolution == 3:
            Dev_WebCam_Resolution=(640,480)
        elif Dev_WebCam_Resolution == 4:
            Dev_WebCam_Resolution=(800,600)
        elif Dev_WebCam_Resolution == 5:
            Dev_WebCam_Resolution=(1280,800)   
        Dev_WebCam_Read.set(3,Dev_WebCam_Resolution[0])
        Dev_WebCam_Read.set(4,Dev_WebCam_Resolution[1])
        
        if saveVideo == 1:
            fourcc = cv2.VideoWriter_fourcc(*'MP4V')
            out = cv2.VideoWriter(Dir_Videos + sessionName + '.mp4',fourcc, 30.0, (640,480))
#%%---- 2.1-Live project (from camera) only one subject 
        if number_subject == 0:
            Arr_TiempoReal[0]=time.time()
            while(int(timeSession) >= Arr_TiempoReal[3]):
                ret, Img_WebCam = Dev_WebCam_Read.read()
                
                if ret==True and saveVideo == 1:
                    out.write(Img_WebCam)
                    
                num_rows, num_cols = Img_WebCam.shape[:2]
                Mat_Img_Rotada = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), Rotar, 1)
                Img_WebCam  = cv2.warpAffine(Img_WebCam, Mat_Img_Rotada, (num_cols, num_rows))
                Img_WebCam = Img_WebCam[round(Img_WebCam.shape[0]*Y1):round(Img_WebCam.shape[0]*Y2),
                                round(Img_WebCam.shape[1]*X1):round(Img_WebCam.shape[1]*X2)]
                
                Mat_WebCam_RGB = np.zeros((Img_WebCam.shape))
                Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,2]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[0]+Mat_RGB[3])))[0]),
                                (np.where((Img_WebCam[:,:,2]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[0]+Mat_RGB[3])))[1]),0] = 1
                Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[0]),
                                (np.where((Img_WebCam[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[1]),1] = 1
                Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,0]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[2]+Mat_RGB[3])))[0]),
                                (np.where((Img_WebCam[:,:,0]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[2]+Mat_RGB[3])))[1]),2] = 1          
                Img_WebCam = Mat_WebCam_RGB  
                       
                if Img_Filtro==1:
                    Img_WebCam = ndimage.gaussian_filter(Img_WebCam, sigma=3)
                elif Img_Filtro==2:
                    Img_WebCam = ndimage.gaussian_filter(Img_WebCam, sigma=5)
                elif Img_Filtro==3:
                    Img_WebCam =ndimage.uniform_filter(Img_WebCam, size=2)
                elif Img_Filtro==4:
                    Img_WebCam =ndimage.uniform_filter(Img_WebCam, size=11)
                np.place(Img_WebCam[:,:,:], Img_WebCam[:,:,:]>=Mat_RGB[4], 1)
                np.place(Img_WebCam[:,:,:], Img_WebCam[:,:,:]<Mat_RGB[4], 0)
                
                try:
                    Mat_Centroide = ndimage.label(Img_WebCam)[0]
                    Centroide = scipy.ndimage.measurements.center_of_mass(Img_WebCam, Mat_Centroide, [1,2,3])
                    Mat_Size = ndimage.label(Img_WebCam)[0]
                    Size = np.sqrt(scipy.ndimage.measurements.sum(Img_WebCam, Mat_Size, [1,2,3]))
                    MinSize = int(np.where(Size == np.min(Size[(Size >= Track_MinSize)]))[0])
                    cv2.circle(Img_WebCam,(int(Centroide[MinSize][1]),int(Centroide[MinSize][0])),2,(0,0,255),5)
                except:
                    Img_WebCam = Img_WebCam
            
                Img_WebCam = cv2.resize(Img_WebCam,(round(aux_width_monitor*4), round(aux_height_monitor*4)))#(400, round((400/Img_WebCam.shape[1])*Img_WebCam.shape[1])))
                cv2.putText(Img_WebCam,'Time: ',(5,15),Font_CV, .5,(255,255,255),1)
                cv2.putText(Img_WebCam,str(round((Arr_TiempoReal[3]) ,2)),(65,15),Font_CV, .5,(255,255,255),1)
                cv2.putText(Img_WebCam,'D: ',(5,35),Font_CV, .5,(255,255,255),1)
                cv2.putText(Img_WebCam,str(round(Int_Contador_Distancia ,2)),(20,35),Font_CV, .5,(255,255,255),1)
                cv2.imshow('Tracking',Img_WebCam)
                cv2.moveWindow('Tracking', int(aux_width_monitor*1), int(aux_height_monitor*3.2));
                
                Mat_Datos[Int_Contador][0] = Arr_TiempoReal[3]
                try:
                    Mat_Datos[Int_Contador][1] = int(Centroide[MinSize][1])
                    Mat_Datos[Int_Contador][2] = int(Centroide[MinSize][0])
                except:
                    Mat_Datos[Int_Contador][1] = Mat_Datos[Int_Contador-1][1]
                    Mat_Datos[Int_Contador][2] = Mat_Datos[Int_Contador-1][2]
                Mat_Datos[Int_Contador][3] = (Fun_Distancia(Mat_Datos[Int_Contador-1][1],Mat_Datos[Int_Contador][1],Mat_Datos[Int_Contador-1][2],Mat_Datos[Int_Contador][2],textEntryX/Img_WebCam1))
                Mat_Datos[Int_Contador][4] = Int_Datos_Consecuencia
                Int_Contador_Distancia += Mat_Datos[Int_Contador][3]
                
                if showPreview == 1:
                    X_ = (Mat_Datos[Int_Contador][1]*100)/Img_WebCam1
                    X_ = (aux_height_monitor*7)*(X_*.01)
                    
                    Y_ = (Mat_Datos[Int_Contador][2]*100)/Img_WebCam0
                    Y_ = (aux_height_monitor*5)*(Y_*.01)
                    putCircleCanvas(canShowDataXY, X_, Y_,5, Mat_RGB)
                
                Int_Contador += 1          
    
                Arr_TiempoReal[1]=time.time()
                Arr_TiempoReal[2]=Arr_TiempoReal[1]-Arr_TiempoReal[0] 
                Arr_TiempoReal[3]+= Arr_TiempoReal[2]
                Mat_Datos[Int_Contador-1][5] = (Mat_Datos[Int_Contador-1][3]/100) / Arr_TiempoReal[2]
                
                Arr_TiempoReal[0]=time.time()
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
               
            Dev_WebCam_Read.release()
            cv2.destroyAllWindows()
            
            if saveVideo == 1:
                out.release()
       
            Mat_Datos = np.delete(Mat_Datos,np.where(Mat_Datos[:,0] == -1), axis=0)
            Mat_Datos[0,3] = 0
            Mat_Datos[0,5] = 0
            
            #Frames Datos
            Select_Frames_Number = messagebox.askyesno("Change frames","Would you like to change the default frames?")
            
            if Select_Frames_Number == True: 
                Number_Frames_ask = askstring('Frames per sec.', 'Insert the number of frames')
                Number_Frames = int(Number_Frames_ask)
                try:
                    Final_Values = []
                    i = 1
                    for i in range(1,int(round(max(Mat_Datos[:,0])))+1):
                        Temp_C = []
                        Temp_P = []
                        Temp_R = []
                        Temp_values = Mat_Datos[np.where((Mat_Datos[:,0] < i) & (Mat_Datos[:,0] > i-1) ),:]
                        Temp_values2 = Mat_Datos[np.where((Mat_Datos[:,0] < i) & (Mat_Datos[:,0] > i-1) ),:]
                        Temp_value_Size = Temp_values[0,:,0].size
                        Frame_range = math.floor(Temp_value_Size / Number_Frames)
                        if np.sum(Temp_values[:,:,4]) > 0:
                            Temp_P = np.arange(0, (Frame_range * Number_Frames)-1, Frame_range)
                            Temp_C = np.where(Temp_values[:,:,4] == 1)[1]
                            Temp_R = np.where(Temp_P[:] == Temp_C[0])[0]
                            try:
                                if int(Temp_R[0]) >= 0:
                                    for i in range(0,Number_Frames-1):
                                        Temp_values[0,i,0] = Temp_values[0,int(Temp_P[i]),0]
                                    Temp_values = Temp_values[0,:Number_Frames,0]
                            except:
                                for i in range(0,Number_Frames-1):
                                    Temp_values[0,i,0] = Temp_values[0,int(Temp_P[i]),0]
                                Temp_values = Temp_values[0,:Number_Frames,0]
                                Temp_values[Number_Frames-1] = Temp_values2[0,Temp_C[0],0]
                                Temp_values= np.sort(Temp_values)
                                    
                        else:
                            Temp_P = np.arange(0, (Frame_range * Number_Frames)-1, Frame_range)
                            for i in range(0,Number_Frames):
                                Temp_values[0,i,0] = Temp_values[0,int(Temp_P[i]),0]
                            Temp_values = Temp_values[0,:Number_Frames,0]
                        Final_Values = np.hstack((Final_Values,Temp_values))    
                    i = 0
                    Mat_Datos_N = np.zeros((len(Final_Values),7))
                    for i in range(0,len(Final_Values)):
                        Temp_Data = Mat_Datos[np.where( (Mat_Datos[:,0] == Final_Values[i])),:]
                        Mat_Datos_N[i,:] = Temp_Data[0,:]
                    Mat_Datos = Mat_Datos_N
                except:
                    messagebox.showinfo("Error", "Not enough frames")   
                      
            #Datos_Generales
            Archivo_Mat_Datos = open(Dir_Datos + sessionName + '.txt','w')
            Archivo_Mat_Datos.write('Subject: ' + subject + '\n' +
                                    'Session: ' + session + '\n' +
                                    'Group: ' + group + '\n' +
                                    'Time: '+ str(max(Mat_Datos[:,0])) + '\n' +
                                    'Consecuences: ' + str(np.size(np.where(Mat_Datos[:,4] == 1))) + '\n' +
                                    'Distance: ' + str(round(sum(Mat_Datos[:,3]),3)) + 'cm' + '\n' +
                                    'Velocity: ' + str(round(sum(Mat_Datos[:,3])/max(Mat_Datos[:,0]),3)) + 'cm/seg' + '\n' +
                                    '\n' + 'Frame;Time;X;Y;Distance;Consecuences' + '\n')
            i = 1
            for i in range(0,len(Mat_Datos)): 
                Archivo_Mat_Datos.write(str(i) +   ',' + str(round(Mat_Datos[i][0],3)) +
                                                   ',' + str(round(Mat_Datos[i][1] * (textEntryX/Img_WebCam1),3)) +
                                                   ',' + str(round(Mat_Datos[i][2] * (textEntryY/Img_WebCam0),3)) +
                                                   ',' + str(round(Mat_Datos[i][3],3)) +
                                                   ',' + str(Mat_Datos[i][4]) + '\n')
            Archivo_Mat_Datos.close() 
            messagebox.showinfo("Finalized", "Session has been traked")
#%%---- 2.2-Live project (from camera) more than one subject 
        else:
            Mat_Datos_X = np.zeros((9999999,16))
            Mat_Datos_Y = np.zeros((9999999,16))
            Mat_Datos_D = np.zeros((9999999,16))
            
            Arr_TiempoReal[0]=time.time()
                            
            while(int(timeSession) >= Arr_TiempoReal[3]):                
                ret, Img_WebCam = Dev_WebCam_Read.read()
                
                if ret==True and saveVideo == 1:
                    out.write(Img_WebCam)
                    
                num_rows, num_cols = Img_WebCam.shape[:2]
                Mat_Img_Rotada = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), Rotar, 1)
                Img_WebCam  = cv2.warpAffine(Img_WebCam, Mat_Img_Rotada, (num_cols, num_rows))
                Img_WebCam = Img_WebCam[round(Img_WebCam.shape[0]*Y1):round(Img_WebCam.shape[0]*Y2),
                                round(Img_WebCam.shape[1]*X1):round(Img_WebCam.shape[1]*X2)]
                
                image_total= np.zeros((Img_WebCam.shape))
                
                i=0
                for i in range(number_subject):
                    image_aux = np.zeros((Img_WebCam.shape))
                    image_aux[(np.where((Img_WebCam[:,:,2]>=(Mat_RGB[i][0]-Mat_RGB[i][3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[i][0]+Mat_RGB[i][3])))[0]),
                              (np.where((Img_WebCam[:,:,2]>=(Mat_RGB[i][0]-Mat_RGB[i][3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[i][0]+Mat_RGB[i][3])))[1]),0] = 1
                    image_aux[(np.where((Img_WebCam[:,:,1]>=(Mat_RGB[i][1]-Mat_RGB[i][3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[i][1]+Mat_RGB[i][3])))[0]),
                              (np.where((Img_WebCam[:,:,1]>=(Mat_RGB[i][1]-Mat_RGB[i][3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[i][1]+Mat_RGB[i][3])))[1]),1] = 1
                    image_aux[(np.where((Img_WebCam[:,:,0]>=(Mat_RGB[i][2]-Mat_RGB[i][3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[i][2]+Mat_RGB[i][3])))[0]),
                              (np.where((Img_WebCam[:,:,0]>=(Mat_RGB[i][2]-Mat_RGB[i][3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[i][2]+Mat_RGB[i][3])))[1]),2] = 1
                            
                    if Img_Filtro[i][0]==1:
                        image_aux = ndimage.gaussian_filter(image_aux, sigma=3)
                    elif Img_Filtro[i][0]==2:
                        image_aux = ndimage.gaussian_filter(image_aux, sigma=5)
                    elif Img_Filtro[i][0]==3:
                        image_aux =ndimage.uniform_filter(image_aux, size=2)
                    elif Img_Filtro[i][0]==4:
                        image_aux =ndimage.uniform_filter(image_aux, size=11)
                    elif Img_Filtro[i][0]==5:
                        image_aux = image_aux
                    np.place(image_aux[:,:,:], image_aux[:,:,:]>=Mat_RGB[i][4], 1)
                    np.place(image_aux[:,:,:], image_aux[:,:,:]<Mat_RGB[i][4], 0)
                    
                    try:
                        Mat_Centroide = ndimage.label(image_aux)[0]
                        Centroide = scipy.ndimage.measurements.center_of_mass(image_aux, Mat_Centroide, [1,2,3])
                        Mat_Size = ndimage.label(image_aux)[0]
                        Size = np.sqrt(scipy.ndimage.measurements.sum(image_aux, Mat_Size, [1,2,3]))
                        MinSize = int(np.where(Size == np.min(Size[(Size >= Track_MinSize)]))[0])
                        cv2.circle(image_aux,(int(Centroide[MinSize][1]),int(Centroide[MinSize][0])),2,(0,0,255),5)
                    except:
                        image_aux = image_aux
                           
                    try:
                        Mat_Datos_X[Int_Contador][i] = int(Centroide[MinSize][1])
                        Mat_Datos_Y[Int_Contador][i] = int(Centroide[MinSize][0])
                    except:
                        Mat_Datos_X[Int_Contador][i] = Mat_Datos_X[Int_Contador-1][i]
                        Mat_Datos_Y[Int_Contador][i] = Mat_Datos_Y[Int_Contador-1][i]
                    Mat_Datos_D[Int_Contador][i] = (Fun_Distancia(Mat_Datos_X[Int_Contador-1][i],Mat_Datos_X[Int_Contador][i],Mat_Datos_Y[Int_Contador-1][i],Mat_Datos_Y[Int_Contador][i],textEntryX/Img_WebCam1))  
                    
                    if showPreview == 1:
                        X_ = (Mat_Datos_X[Int_Contador][i]*100)/Img_WebCam1
                        X_ = (aux_height_monitor*7)*(X_*.01)
                        
                        Y_ = (Mat_Datos_Y[Int_Contador][i]*100)/Img_WebCam0
                        Y_ = (aux_height_monitor*5)*(Y_*.01)
                        putCircleCanvas(canShowDataXY, X_, Y_,5, Mat_RGB[i][:])
                    
                    image_total += image_aux
                    if i == number_subject -1:
                        image_total = cv2.resize(image_total,(round(aux_width_monitor*4), round(aux_height_monitor*4))) 
                        j = 0
                        for j in range(number_subject):
                            cv2.putText(image_total,str(j+1),(int(Mat_Datos_X[Int_Contador][j])+10,int(Mat_Datos_Y[Int_Contador][j])),Font_CV, .5,(0,0,255),1)    
                        cv2.putText(image_total,'T: ',(5,15),Font_CV, .5,(255,255,255),1)
                        cv2.putText(image_total,str(round((Arr_TiempoReal[3]) ,2)),(65,15),Font_CV, .5,(255,255,255),1)
                        cv2.imshow('Tracking',image_total)
                        cv2.moveWindow('Tracking', int(aux_width_monitor*1), int(aux_height_monitor*3.2));
                        cv2.waitKey(5)
                      
                        
                Mat_Datos[Int_Contador][0] = Arr_TiempoReal[3]
                Mat_Datos[Int_Contador][2] = Arr_TiempoReal[2]
                Mat_Datos[Int_Contador][4] = Int_Datos_Consecuencia
                
                Int_Contador += 1          

                Arr_TiempoReal[1]=time.time()
                Arr_TiempoReal[2]=Arr_TiempoReal[1]-Arr_TiempoReal[0] 
                Arr_TiempoReal[3]+= Arr_TiempoReal[2]
                Arr_TiempoReal[0]=time.time()
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break  
                    
            Dev_WebCam_Read.release()
            cv2.destroyAllWindows()
            
            if saveVideo == 1:
                out.release()
            
            Mat_Datos = np.delete(Mat_Datos,np.where(Mat_Datos[:,0] == -1), axis=0)
            Mat_Datos_X = Mat_Datos_X[0:len(Mat_Datos),:]
            Mat_Datos_Y = Mat_Datos_Y[0:len(Mat_Datos),:]
            Mat_Datos_D = Mat_Datos_D[0:len(Mat_Datos),:]
            
            Select_Frames_Number = messagebox.askyesno("Change frames","Would you like to change the default frames?")
            
            if Select_Frames_Number == True: 
                Number_Frames_ask = askstring('Frames per sec.', 'Insert the number of frames')
                Number_Frames = int(Number_Frames_ask)
                try:
                    Number_Frames = 2
                    Final_Values = []
                    i = 1
                    for i in range(1,len(Mat_Datos)):
                        Temp_values = Mat_Datos[np.where( (Mat_Datos[:,0] < i) & (Mat_Datos[:,0] > i-1)),0]
                        Temp_Perm = np.random.permutation(Temp_values.size)[0:Number_Frames]
                        Temp_values = np.sort(Temp_values[0,Temp_Perm])
                        Final_Values = np.hstack((Final_Values,Temp_values))
                    
                    i = 0
                    Mat_Datos_N = np.zeros((len(Final_Values),7))
                    Mat_Datos_X_N = np.zeros((len(Final_Values),16)) 
                    Mat_Datos_Y_N = np.zeros((len(Final_Values),16)) 
                    Mat_Datos_D_N = np.zeros((len(Final_Values),16)) 
                    for i in range(0,len(Final_Values)):
                        Temp_Data = Mat_Datos[np.where( (Mat_Datos[:,0] == Final_Values[i])),:]
                        Temp_Data_X = Mat_Datos_X[np.where( (Mat_Datos[:,0] == Final_Values[i])),:]
                        Temp_Data_Y = Mat_Datos_Y[np.where( (Mat_Datos[:,0] == Final_Values[i])),:]
                        Temp_Data_D = Mat_Datos_Y[np.where( (Mat_Datos[:,0] == Final_Values[i])),:]
                        Mat_Datos_N[i,:] = Temp_Data
                        Mat_Datos_X_N[i,:] = Temp_Data_X
                        Mat_Datos_Y_N[i,:] = Temp_Data_Y
                        Mat_Datos_D_N[i,:] = Temp_Data_D
                    Mat_Datos = Mat_Datos_N
                    Mat_Datos_X = Mat_Datos_X_N
                    Mat_Datos_Y = Mat_Datos_Y_N
                    Mat_Datos_D = Mat_Datos_D_N
                except:
                    messagebox.showinfo("Error", "Not enough frames")    
            
                   
            #Datos
            j = 0
            for j in range(number_subject):
                #Datos_Generales
                Archivo_Mat_Datos = open(Dir_Datos + sessionName + '_' + str(j+1) + '.txt','w')
                Archivo_Mat_Datos.write('Subject: ' + subject + '_' + str(j+1) +'\n' +
                                        'Session: ' + session + '\n' +
                                        'Group: ' + group + '\n' +
                                        'Time: '+ str(max(Mat_Datos[:,0])) + '\n' +
                                        'Consecuences: ' + str(np.size(np.where(Mat_Datos[:,4] == 1))) + '\n' +
                                        'Distance: ' + str(round(sum(Mat_Datos_D[:,j]),3)) + 'cm' + '\n' +
                                        'Velocity: ' + str(round(sum(Mat_Datos_D[:,j])/max(Mat_Datos[:,0]),3)) + 'cm/seg' + '\n' +
                                        '\n' + 'Frame;Time;X;Y;Distance;Consecuences' + '\n')
                #Datos_Matriz
                i = 1
                for i in range(0,len(Mat_Datos)): 
                    Archivo_Mat_Datos.write(str(i) + ';' + str(round(Mat_Datos[i][0],3)) +
                                                     ';' + str(round(Mat_Datos_X[i][j] * (textEntryX/Img_WebCam1),3)) +
                                                     ';' + str(round(Mat_Datos_Y[i][j] * (textEntryY/Img_WebCam0),3)) +
                                                     ';' + str(round(Mat_Datos_D[i][j],3)) +
                                                     ';' + str(Mat_Datos[i][4]) + '\n')
                
                Archivo_Mat_Datos.close()
                
            messagebox.showinfo("Finalized", "Sesion has been traked")
#%%Fun_Nuevo_Proyecto_Vivo      
def Fun_Nuevo_Proyecto_Vivo():
    global Seleccion_Track, Dialog_Video_File, Ruta_Proyecto, Ruta_Video, Carpeta_Imagenes, Ruta_Carpeta_Imagenes, Nombre_Archivo, Ruta_Imagen
    global Lbl_Img_Original
    Seleccion_Track = 2
    
    Dialog_Video_File = filedialog.asksaveasfilename(initialdir = Dir_Videos,
                                                     title = "Guardar archivo",
                                                     filetypes = (("all files","*.*"), ("jpeg files","*.jpg")))
    Ruta_Proyecto = Dir_Videos
    Ruta_Video = Dialog_Video_File+'/'
    Carpeta_Imagenes ='/Images/'
    Ruta_Carpeta_Imagenes = Dialog_Video_File + Carpeta_Imagenes
    Nombre_Archivo = Dialog_Video_File.split('/')[(np.size(Dialog_Video_File.split('/')))-1]
    
    if os.path.exists(Dialog_Video_File):
        os.path.exists(Dialog_Video_File)
        os.mkdir(Dialog_Video_File+Carpeta_Imagenes)
    else:
        os.mkdir(Dialog_Video_File)
        os.mkdir(Dialog_Video_File+Carpeta_Imagenes)
        
    Dev_WebCam_Resolution = Seleccion_Resolucion
    Dev_WebCam_Read = FunSetResolutionParameter(Dev_WebCam_Resolution, Seleccion_Camara)
    j=0
    while (Dev_WebCam_Read.isOpened()):
        ret, frame = Dev_WebCam_Read.read()    
        Ruta_Imagen = Ruta_Carpeta_Imagenes+'Image_1.jpg'
        cv2.imwrite(Ruta_Imagen, frame)
        j+=1
        if j==3:
            break
    Dev_WebCam_Read.release()
    
    global Dialog_Video_File_Aux
    Dialog_Video_File_Aux = Ruta_Imagen.replace('Image_1', 'Aux_Image')
    
    Lbl_Img_Original.place_forget()
    Img_Original= PIL.Image.open(Ruta_Imagen)
    Img_Original_2 = imageRezicePesNewProject(Img_Original)
    
    Photo_Img_Aux = ImageTk.PhotoImage(Img_Original_2)
    Lbl_Img_Original = tkinter.Label(pesNewProject, image=Photo_Img_Aux, bg = Fun_Rgb(C_Primary), bd = 0)
    Lbl_Img_Original.image = Photo_Img_Aux 
    Lbl_Img_Original.place(x = (aux_width_monitor*1), y = (aux_height_monitor*1)+1) 
    
    def Fun_Borrar_Y_Tomar_Nueva():
        os.remove(Ruta_Carpeta_Imagenes+'Image_1.jpg')
        global Lbl_Img_Original, Lbl_Img_Original_Aux
        
        Dev_WebCam_Resolution = Seleccion_Resolucion
        Dev_WebCam_Read = FunSetResolutionParameter(Dev_WebCam_Resolution, Seleccion_Camara)
        j=0
        while (Dev_WebCam_Read.isOpened()):
            ret, frame = Dev_WebCam_Read.read()    
            Ruta_Imagen = Ruta_Carpeta_Imagenes+'Image_1.jpg'# +  str(int(i)) + ".jpg"
            cv2.imwrite(Ruta_Imagen, frame)
            j+=1
            if j==3:
                break
        Dev_WebCam_Read.release()
        
        global Dialog_Video_File_Aux
        Dialog_Video_File_Aux = Ruta_Imagen.replace('Image_1', 'Aux_Image')
        
        Img_Original= PIL.Image.open(Ruta_Imagen)
        Img_Original_2 = imageRezicePesNewProject(Img_Original)
        
        Photo_Img_Aux = ImageTk.PhotoImage(Img_Original_2)
        Lbl_Img_Original = tkinter.Label(pesNewProject, image=Photo_Img_Aux, bg = Fun_Rgb(C_Primary), bd = 0)
        Lbl_Img_Original.image = Photo_Img_Aux 
        Lbl_Img_Original.place(x = (aux_width_monitor*1), y = (aux_height_monitor*1)+1) 
        
        
        mensaje1 = messagebox.askyesno(message= 'Take another picture?', title="Picture")
        if mensaje1==True:
            Lbl_Img_Original.place_forget()
            Fun_Borrar_Y_Tomar_Nueva()
     
    mensaje1 =messagebox.askyesno(message="Take another picture?", title="Picture")
    if mensaje1==True:
        Lbl_Img_Original.place_forget()
        Fun_Borrar_Y_Tomar_Nueva()
    updateSeleccionTrackLive()
#%%Fun updateSeleccionTrackLive
def updateSeleccionTrackLive():
    global Seleccion_Track
    Seleccion_Track = 2      
#%%Fun updateSeleccionTrackVideo
def updateSeleccionTrackVideo():
    global Seleccion_Track
    Seleccion_Track = 1 
    
def Fun_Abrir_Proyecto_Vivo():
    global Seleccion_Track
    Seleccion_Track = 2
    # Fun_Iniciar_Track()
#%%-------------WIDGETS APLICATION-------------
#%%Window
root = Tk()
root.title('Walden Tracking System v-3.0')
root.geometry(str(width_monitor)+'x'+str(height_monitor-70)+'+0+0') 
root.iconbitmap(Dir_Images+"Icon.ico")
root.resizable(0,0)
root.config(bg = Fun_Rgb(C_Primary))
root.isStopped = False

Lbl_Img_Original = Label(root, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
LblXAxis = tkinter.Label(root, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
LblYAxis = tkinter.Label(root, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
#%%Toolbar and menu
toolbar = Frame(root)

imgSettings = PIL.Image.open(Dir_Images+'settings.png')
useImgSettings= ImageTk.PhotoImage(imgSettings)
imgCutVideo = PIL.Image.open(Dir_Images+'cutVideo.png')
useImgCutVideo = ImageTk.PhotoImage(imgCutVideo)
imgOpenImageProject = PIL.Image.open(Dir_Images+'imageProject.png')
useImgOpenImageProject = ImageTk.PhotoImage(imgOpenImageProject)
imgOpenVideoProject = PIL.Image.open(Dir_Images+'videoProject.png')
useImgOpenVideoProject = ImageTk.PhotoImage(imgOpenVideoProject)
imgConfigImage = PIL.Image.open(Dir_Images+'configImage.png')
useImgConfigImage = ImageTk.PhotoImage(imgConfigImage)
imgConfigLive = PIL.Image.open(Dir_Images+'configLive.png')
useImgConfigLive = ImageTk.PhotoImage(imgConfigLive)
imgGetRGB = PIL.Image.open(Dir_Images+'rgb.png')
useImgGetRGB = ImageTk.PhotoImage(imgGetRGB)
imgOpenConfigFile = PIL.Image.open(Dir_Images+'openConfigFile.png')
useImgOpenConfigFile = ImageTk.PhotoImage(imgOpenConfigFile)
imgOpenDirectory = PIL.Image.open(Dir_Images+'openDirectory.png')
useImgOpenDirectory = ImageTk.PhotoImage(imgOpenDirectory)

img6 = PIL.Image.open(Dir_Images+'changeCamera.png')
useImg6 = ImageTk.PhotoImage(img6)

iconTool_Options = Button(toolbar, image=useImgSettings, text="Settings", command=openSettings)
iconTool_Options.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconTool_Options, text = 'Settings')

iconTool_CutVideo = Button(toolbar, image=useImgCutVideo, text="Select video to cut", command=SelectVideo)
iconTool_CutVideo.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconTool_CutVideo, text = 'Cut video')

iconOpneImageProject = Button(toolbar, image=useImgOpenImageProject, text="Open image project", command=openImage)
iconOpneImageProject.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconOpneImageProject, text = 'Open image project')

iconOpenVideo = Button(toolbar, image=useImgOpenVideoProject, text="Open video project", command=openVideo)
iconOpenVideo.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconOpenVideo, text = 'Open video project')

iconNewVideoProject = Button(toolbar, image=useImgConfigImage, text="Image project", command=newVideoProject)
iconNewVideoProject.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconNewVideoProject, text = 'Config image project')

iconNewLiveProject = Button(toolbar, image=useImgConfigLive, text="Live project", command= Fun_Nuevo_Proyecto_Vivo)
iconNewLiveProject.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconNewLiveProject, text = 'Config live project')

iconOpenObservation = Button(toolbar, image=useImgGetRGB, text="Get RGB values", command= Fun_Get_RGB)
iconOpenObservation.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconOpenObservation, text = 'Get RGB values')

closeButton = Button(toolbar, image=useImgOpenConfigFile, text="Open config file", command=openConfigFile)
closeButton.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(closeButton, text = 'Open config file')

checkInputButton = Button(toolbar, image=useImgOpenDirectory, text="Open directory", command=openProjectDirectoryToTrack)
checkInputButton.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(checkInputButton, text = 'Open directory')

toolbar.pack(side=TOP, fill=X)

menubar = tkinter.Menu(root)
root.config(menu=menubar)

if theme == 1:
    Menu_Opc1 = tkinter.Menu(root, bg=Fun_Rgb(C_White), fg=Fun_Rgb(C_Primary),
                                 activebackground=Fun_Rgb(C_Grey), activeforeground=Fun_Rgb(C_Light_Dark),
                                 tearoff=0) 
    Menu_Videos = tkinter.Menu(root, bg=Fun_Rgb(C_White), fg=Fun_Rgb(C_Primary),
                             activebackground=Fun_Rgb(C_Grey), activeforeground=Fun_Rgb(C_Light_Dark),
                             tearoff=1)   
    Menu_Config = tkinter.Menu(root, bg=Fun_Rgb(C_White), fg=Fun_Rgb(C_Primary),
                             activebackground=Fun_Rgb(C_Grey), activeforeground=Fun_Rgb(C_Light_Dark),
                             tearoff=0)
    Menu_Track = tkinter.Menu(root, bg=Fun_Rgb(C_White), fg=Fun_Rgb(C_Primary),
                             activebackground=Fun_Rgb(C_Grey), activeforeground=Fun_Rgb(C_Light_Dark),
                             tearoff=0) 
elif theme == 0:
    Menu_Opc1 = tkinter.Menu(root, bg=Fun_Rgb(C_Dark), fg=Fun_Rgb(C_White),
                                 activebackground=Fun_Rgb(C_Grey), activeforeground=Fun_Rgb(C_Dark),
                                 tearoff=0)  
    Menu_Videos = tkinter.Menu(root, bg=Fun_Rgb(C_Dark), fg=Fun_Rgb(C_White),
                                 activebackground=Fun_Rgb(C_Grey), activeforeground=Fun_Rgb(C_Dark),
                                 tearoff=0)  
    Menu_Config = tkinter.Menu(root, bg=Fun_Rgb(C_Dark), fg=Fun_Rgb(C_White),
                                 activebackground=Fun_Rgb(C_Grey), activeforeground=Fun_Rgb(C_Dark),
                                 tearoff=0) 
    Menu_Track = tkinter.Menu(root, bg=Fun_Rgb(C_Dark), fg=Fun_Rgb(C_White),
                                 activebackground=Fun_Rgb(C_Grey), activeforeground=Fun_Rgb(C_Dark),
                                 tearoff=0)                        
menubar.add_cascade(label="File", menu=Menu_Opc1)
Menu_Opc1.add_command(label='Select video to cut', command=SelectVideo)
Menu_Opc1.add_command(label='Open image project', command=openImage) 
Menu_Opc1.add_command(label='Open video', command=openVideo) 
Menu_Opc1.add_separator()
Menu_Opc1.add_command(label='Config image project', command = newVideoProject)
Menu_Opc1.add_command(label='Config live project', command = Fun_Nuevo_Proyecto_Vivo)
Menu_Opc1.add_command(label='Get RGB values', command = Fun_Get_RGB)
Menu_Opc1.add_separator()
Menu_Opc1.add_command(label='Data analysis')
Menu_Opc1.add_command(label='User information')
Menu_Opc1.add_separator()
Menu_Opc1.add_command(label='Settings', command = openSettings)
Menu_Opc1.add_separator()
Menu_Opc1.add_command(label='License', command=info)
                     
menubar.add_cascade(label="Videos", menu=Menu_Videos)
Menu_Videos.add_command(label='Select video to cut', command=SelectVideo)
Menu_Videos.add_command(label='Open image project', command=openImage) 
Menu_Videos.add_command(label='Open video', command=openVideo)   
                         
menubar.add_cascade(label="Config file", menu=Menu_Config)
Menu_Config.add_command(label='Video project', command = newVideoProject)
Menu_Config.add_command(label='Live project', command = Fun_Nuevo_Proyecto_Vivo)
Menu_Config.add_separator()
Menu_Config.add_command(label='Get RGB values', command = Fun_Get_RGB)
                    
menubar.add_cascade(label="Tracking", menu=Menu_Track)
Menu_Track.add_command(label='Open Config file', command = openConfigFile)
Menu_Track.add_command(label='Open Project directory', command = openProjectDirectoryToTrack)
Menu_Track.add_separator()
Menu_Track.add_command(label='Start tracking', command = TrackProject)
Menu_Track.add_command(label='Clear preview space', command = clearCanvas)
#%%Notebooks
style = ttk.Style()
if theme == 0:
    settings = {"TNotebook.Tab": {"configure": {"padding": [100, 10],
                                            "background": Fun_Rgb(C_Light_Dark)
                                           },
                              "map": {"background": [("selected", Fun_Rgb(C_Primary)), 
                                                     ("active", Fun_Rgb(C_Light_Dark))],
                                      
                                      "foreground": [("selected", Fun_Rgb(C_White)),
                                                     ("active", "#000000")]

                                     }
                              }
           }  
if theme == 1:
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
pesCutVideo = tkinter.Frame(notebook, background = Fun_Rgb(C_Light_Dark))
pesNewProject = tkinter.Frame(notebook, background = Fun_Rgb(C_Light_Dark))
pesTracking = tkinter.Frame(notebook, background = Fun_Rgb(C_Light_Dark))

notebook.add(pesCutVideo, text = 'Videos', compound=LEFT)
notebook.add(pesNewProject, text = 'Config file')
notebook.add(pesTracking, text= 'Tracking')
#%%-------------WIDGETS NOTEBOOK VIDEOS-------------
#%%Canvas notebook Videos
canTittle = Canvas(pesCutVideo, width=int(width_monitor), height=int(aux_height_monitor*14), bg=Fun_Rgb(C_Primary))

#Left side
canTittle.create_rectangle(int(aux_width_monitor*1), int(aux_height_monitor*1), 
                           int(aux_width_monitor*8), int(aux_height_monitor*9), 
                           fill=Fun_Rgb(C_Dark), outline=Fun_Rgb(C_White), width=.1)#Set videos and images
canTittle.create_rectangle(int(aux_width_monitor*1), int(aux_height_monitor*9.6), 
                           int(aux_width_monitor*4), int(aux_height_monitor*12), 
                           fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=1)#Change images x1 and x10
canTittle.create_rectangle(int(aux_width_monitor*4.5), int(aux_height_monitor*9.6), 
                           int(aux_width_monitor*8), int(aux_height_monitor*12), 
                           fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=1)#Open video 

#Right side
#cut video
canTittle.create_rectangle(int(aux_width_monitor*8.3), int(aux_height_monitor*1), int(aux_width_monitor*14.3), int(aux_height_monitor*3), fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=.1)
canTittle.create_rectangle(int(aux_width_monitor*8.4), int(aux_height_monitor*1.1), 
                           int(aux_width_monitor*12.5), int(aux_height_monitor*1.9), fill=Fun_Rgb(C_Primary), outline=Fun_Rgb(C_White), width=1)
canTittle.create_rectangle(int(aux_width_monitor*8.4), int(aux_height_monitor*2), 
                           int(aux_width_monitor*12.5), int(aux_height_monitor*2.9), fill=Fun_Rgb(C_Primary), outline=Fun_Rgb(C_White), width=1)
#open video project
canTittle.create_rectangle(int(aux_width_monitor*8.3), int(aux_height_monitor*4), int(aux_width_monitor*14.3), int(aux_height_monitor*5), fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=.1)
canTittle.create_rectangle(int(aux_width_monitor*8.4), int(aux_height_monitor*4.1), 
                           int(aux_width_monitor*12.5), int(aux_height_monitor*4.9), fill=Fun_Rgb(C_Primary), outline=Fun_Rgb(C_White), width=1)
#take video
canTittle.create_rectangle(int(aux_width_monitor*8.3), int(aux_height_monitor*6), int(aux_width_monitor*14.3), int(aux_height_monitor*8), fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=.1)
canTittle.create_rectangle(int(aux_width_monitor*8.4), int(aux_height_monitor*6.1), 
                           int(aux_width_monitor*12.5), int(aux_height_monitor*6.9), fill=Fun_Rgb(C_Primary), outline=Fun_Rgb(C_White), width=1)
canTittle.create_rectangle(int(aux_width_monitor*8.4), int(aux_height_monitor*7), 
                           int(aux_width_monitor*12.5), int(aux_height_monitor*7.9), fill=Fun_Rgb(C_Primary), outline=Fun_Rgb(C_White), width=1)
#download from youtube
canTittle.create_rectangle(int(aux_width_monitor*8.3), int(aux_height_monitor*9), int(aux_width_monitor*14.3), int(aux_height_monitor*10), fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=.1)
canTittle.create_rectangle(int(aux_width_monitor*8.4), int(aux_height_monitor*9.1), 
                           int(aux_width_monitor*12.5), int(aux_height_monitor*9.9), fill=Fun_Rgb(C_Primary), outline=Fun_Rgb(C_White), width=1)
#open video project
canTittle.create_rectangle(int(aux_width_monitor*8.3), int(aux_height_monitor*11), int(aux_width_monitor*14.3), int(aux_height_monitor*12), fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=.1)
canTittle.create_rectangle(int(aux_width_monitor*8.4), int(aux_height_monitor*11.1), 
                           int(aux_width_monitor*12.5), int(aux_height_monitor*11.9), fill=Fun_Rgb(C_Primary), outline=Fun_Rgb(C_White), width=1)
canTittle.place(x=0,y=0) 
#%%Labels, buttons and entries of notebook Video         
lblVideo = Label(pesCutVideo, text="Image/Video", bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblVideo.config(font = (Font_1,15))
lblVideo.place(x=aux_width_monitor*1, y=aux_height_monitor*0.5)

lblCutVideo = Label(pesCutVideo, text="Cut video", bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblCutVideo.config(font = (Font_1,15))
lblCutVideo.place(x=aux_width_monitor*8.3, y=aux_height_monitor*.5)

lblOpenImage = Label(pesCutVideo, text="Open image project", bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblOpenImage.config(font = (Font_1,15))
lblOpenImage.place(x=aux_width_monitor*8.3, y=aux_height_monitor*8.5)

lblTakeVideo = Label(pesCutVideo, text='Take video ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblTakeVideo.config(font = (Font_1,15))
lblTakeVideo.place(x=aux_width_monitor*8.3, y=aux_height_monitor*5.5)

lblTakeVideo = Label(pesCutVideo, text='Download video from YouTube ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblTakeVideo.config(font = (Font_1,15))
lblTakeVideo.place(x=aux_width_monitor*8.3, y=aux_height_monitor*3.5)

lblVideoProject = Label(pesCutVideo, text="Open video project", bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblVideoProject.config(font = (Font_1,15))
lblVideoProject.place(x=aux_width_monitor*8.3, y=aux_height_monitor*10.5)

var1 = StringVar()
videoName = StringVar()
cameraNumber = StringVar()
rate = "Frames per second in the video: "
rateNumber = "0"
rateVideo = StringVar()
rateVideo.set(rate + rateNumber)
videoURL = StringVar()

entSub1 = Entry(pesCutVideo, textvariable = var1, bd =1, width = 15)
entSub1.place(x=aux_width_monitor*11.2, y=aux_height_monitor*2.35)

entVideoName = Entry(pesCutVideo, textvariable = videoName, bd =1, width = 20)
entVideoName.place(x=aux_width_monitor*9.7, y=aux_height_monitor*6.3)

entVideoURL = Entry(pesCutVideo, textvariable = videoURL, bd =1, width = 50)
entVideoURL.place(x=aux_width_monitor*9.1, y=aux_height_monitor*4.3)

#------------  labels  --------------------
lblSetRate = tkinter.Label(pesCutVideo, bg = Fun_Rgb(C_Primary), 
                            fg = Fun_Rgb(C_White), textvariable = rateVideo)
lblSetRate.config(font = ('Arial',13))
lblSetRate.place(x= aux_width_monitor*8.5, y = aux_height_monitor*1.3)

lblSetRate_2 = tkinter.Label(pesCutVideo, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), text = 'Select the frames per second (f/s):')
lblSetRate_2.config(font = ('Arial',13))
lblSetRate_2.place(x= aux_width_monitor*8.5, y = aux_height_monitor*2.3)

lblNumberCamera = Label(pesCutVideo, text=str(Seleccion_Camara), bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblNumberCamera.config(font = (Font_1,20))
lblNumberCamera.place(x=aux_width_monitor*12, y=aux_height_monitor*6.2)

lblNameVideo = Label(pesCutVideo, text='Video name:', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblNameVideo.config(font = (Font_1,15))
lblNameVideo.place(x=aux_width_monitor*8.5, y=aux_height_monitor*6.2)

lblURL = Label(pesCutVideo, text='URL:', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblURL.config(font = (Font_1,15))
lblURL.place(x=aux_width_monitor*8.5, y=aux_height_monitor*4.25)

lblNumberImage = Label(pesCutVideo, text='Image '+str(currentPicture+1)+ ' of '+str(len(List_Contenido)) +'       ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblNumberImage.config(font = (Font_1,15))
lblNumberImage.place(x=aux_width_monitor*1, y=aux_height_monitor*9.1)

lblOpenVideo = Label(pesCutVideo, text = 'Video info', bg= Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblOpenVideo.config(font = (Font_1, 15))
lblOpenVideo.place(x = aux_width_monitor*4.5, y = aux_height_monitor*9.1)

lblVideoProject = Label(pesCutVideo, text='Project: ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblVideoProject.config(font = (Font_1,15))
lblVideoProject.place(x=aux_width_monitor*8.5, y=aux_height_monitor*9.2)

lblVideoProject = Label(pesCutVideo, text='Project: ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblVideoProject.config(font = (Font_1,15))
lblVideoProject.place(x=aux_width_monitor*8.5, y=aux_height_monitor*11.3)

lblFrames = Label(pesCutVideo, text='Frames per second: ', bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblFrames.config(font = (Font_1,15))
lblFrames.place(x=aux_width_monitor*4.6, y = aux_height_monitor*9.8)

lblTotalFrames = Label(pesCutVideo, text='Total frames: ', bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblTotalFrames.config(font = (Font_1,15))
lblTotalFrames.place(x=aux_width_monitor*4.6, y = aux_height_monitor*10.3)

lblDuration = Label(pesCutVideo, text='Duration: ', bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblDuration.config(font = (Font_1,15))
lblDuration.place(x=aux_width_monitor*4.6, y = aux_height_monitor*10.8)

lblName = Label(pesCutVideo, text='Name: ', bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblName.config(font = (Font_1,15))
lblName.place(x=aux_width_monitor*4.6, y = aux_height_monitor*11.3)
    
#------------  Buttons  --------------------
btnSelectVideo = tkinter.Button(pesCutVideo,  bd=1, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark), highlightcolor = Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,  
    text = 'Select video', command = SelectVideo, relief=GROOVE)
btnSelectVideo.config(font = ("Arial",12))
btnSelectVideo.place(x=aux_width_monitor*13, y=aux_height_monitor*1.1)

btnCutVideo = tkinter.Button(pesCutVideo,  bd=1, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark), highlightcolor = Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,  
    text = 'Cut video', command = cutVideo, relief=GROOVE)
btnCutVideo.config(font = ("Arial",12))
btnCutVideo.place(x=aux_width_monitor*13, y=aux_height_monitor*2)

btnBacktImgX1 = tkinter.Button(pesCutVideo,  bd=1, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),  highlightcolor = Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,
    text = 'Prev', command = lambda: changeImage(-1))#prevImage, relief=GROOVE)
btnBacktImgX1.config(font = ("Arial",12))
btnBacktImgX1.place(x=aux_width_monitor*1.1, y=aux_height_monitor*10)
CreateToolTip(btnBacktImgX1, text = 'X1')

btnNextImgX1 = tkinter.Button(pesCutVideo,  bd=1, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),  highlightcolor = Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,
    text = 'Next ', command = lambda: changeImage(1))
btnNextImgX1.config(font = ("Arial",12))
btnNextImgX1.place(x=aux_width_monitor*2.7, y=aux_height_monitor*10)
CreateToolTip(btnNextImgX1, text = 'X1')

btnBacktImgX10 = tkinter.Button(pesCutVideo,  bd=1, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),  highlightcolor = Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,
    text = 'Prev', command = lambda: changeImage(-10), relief=GROOVE)
btnBacktImgX10.config(font = ("Arial",12))
btnBacktImgX10.place(x=aux_width_monitor*1.1, y=aux_height_monitor*11)
CreateToolTip(btnBacktImgX10, text = 'X10')

btnNextImgX10 = tkinter.Button(pesCutVideo,  bd=1, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),  highlightcolor = Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,
    text = 'Next ', command = lambda: changeImage(10), relief=GROOVE)
btnNextImgX10.config(font = ("Arial",12))
btnNextImgX10.place(x=aux_width_monitor*2.7, y=aux_height_monitor*11)
CreateToolTip(btnNextImgX10, text = 'X10')

btnOpenImageProject = tkinter.Button(pesCutVideo,  bd=1, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),  highlightcolor = Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,
    text = 'Open ', command = openImage, relief=GROOVE)
btnOpenImageProject.config(font = ("Arial",12))
btnOpenImageProject.place(x=aux_width_monitor*13, y=aux_height_monitor*9.1)

btnChangeCamera = tkinter.Button(pesCutVideo,  bd=1, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),  highlightcolor = Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=80, height = 45,
    image=useImg6, command = Fun_Change_Camera, relief=GROOVE)
btnChangeCamera.config(font = ("Arial",12))
btnChangeCamera.place(x=aux_width_monitor*11.2, y=aux_height_monitor*6.15)
# CreateToolTip(btnChangeCamera, text = 'Change camera')

btnTestVideo = tkinter.Button(pesCutVideo,  bd=1, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),  highlightcolor = Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,
    text = 'Test video', command = Fun_Test_Video, relief=GROOVE)
btnTestVideo.config(font = ("Arial",12))
btnTestVideo.place(x=aux_width_monitor*13, y=aux_height_monitor*6.1)

btnTakeVideo = tkinter.Button(pesCutVideo,  bd=1, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),  highlightcolor = Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,
    text = 'Record ', command = Fun_Take_Video, relief=GROOVE)
btnTakeVideo.config(font = ("Arial",12))
btnTakeVideo.place(x=aux_width_monitor*13, y=aux_height_monitor*7.1)

btnDownload = tkinter.Button(pesCutVideo,  bd=1, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),  highlightcolor = Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,
    text = 'Download', command = Fun_Download_Video, relief=GROOVE)
btnDownload.config(font = ("Arial",12))
btnDownload.place(x=aux_width_monitor*13, y=aux_height_monitor*4.1)

btnPlayVideo = tkinter.Button(pesCutVideo, bd =1, fg=Fun_Rgb(C_White), 
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark), highlightcolor = Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,
    text = 'Open', command = openVideo, relief=GROOVE)
btnPlayVideo.config(font=('Arial', 12))
btnPlayVideo.place(x=aux_width_monitor*13, y=aux_height_monitor*11.1)

#------------  RadioButton  --------------------
opcion = IntVar() # Como StrinVar pero en entero

R1 = Radiobutton(pesCutVideo, bg=Fun_Rgb(C_Primary), activebackground=Fun_Rgb(C_Light_Dark), indicatoron=0, bd = 0,
    text="480x320", variable=opcion, value=1, command=FunSetResolution)
R1.config(font=('Arial', 12))
R1.place(x=aux_width_monitor*8.5, y=aux_height_monitor*7.2)

R2 = Radiobutton(pesCutVideo, bg=Fun_Rgb(C_Primary), activebackground=Fun_Rgb(C_Light_Dark), indicatoron=0, bd = 0,
    text="600x480", variable=opcion, value=2, command=FunSetResolution)
R2.config(font=('Arial', 12))
R2.place(x=aux_width_monitor*9.5, y=aux_height_monitor*7.2)

R3 = Radiobutton(pesCutVideo, bg=Fun_Rgb(C_Primary), activebackground=Fun_Rgb(C_Light_Dark), indicatoron=0, bd = 0,
    text="800x600", variable=opcion, value=3, command=FunSetResolution)
R3.config(font=('Arial', 12))
R3.place(x=aux_width_monitor*10.5, y=aux_height_monitor*7.2)

R4 = Radiobutton(pesCutVideo, bg=Fun_Rgb(C_Primary), activebackground=Fun_Rgb(C_Light_Dark), indicatoron=0, bd=0, 
    text="1280x800", variable=opcion, value=4, command=FunSetResolution)
R4.config(font=('Arial', 12))
R4.place(x=aux_width_monitor*11.5, y=aux_height_monitor*7.2)
#%%-------------WIDGETS NOTBOOK CONFIG PROJECTS-------------
#%%Canvas notebook pesNewProject
canNewProject = Canvas(pesNewProject, width=int(width_monitor), height=int(aux_height_monitor*14), bg=Fun_Rgb(C_Primary))

#left side
# canNewProject.create_rectangle(int(aux_width_monitor*.7), int(aux_height_monitor*1), 
#                                int(aux_width_monitor*4.75), int(aux_width_monitor*3.2), fill=Fun_Rgb(C_Dark), outline=Fun_Rgb(C_White), width=.1)
        
canNewProject.create_rectangle(int(aux_width_monitor*1), int(aux_height_monitor*1), int(aux_width_monitor*8), int(aux_height_monitor*9), fill=Fun_Rgb(C_Dark), outline=Fun_Rgb(C_White), width=.1)
canNewProject.place(x=0,y=0) 
#%%Sliders notebook pesNewProject (cut image)
#-------------------- Sliders to cut images (left side) --------------------
Slider_X1 = tkinter.Scale(pesNewProject, 
            from_=0, to=.5, resolution=0.01,
            orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*3.4,
            fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
            activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
            showvalue=1, command = getValuesSliders)
Slider_X1.config(font=(Font_1,11))
Slider_X1.place(x=int(aux_width_monitor*1), y=int(aux_height_monitor*.1))

Slider_X2 = tkinter.Scale(pesNewProject, 
            from_=.51, to=1, resolution=0.01,
            orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*3.4,
            fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
            activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
            showvalue=1, command = getValuesSliders)
Slider_X2.config(font=(Font_1,11))
Slider_X2.set(1)
Slider_X2.place(x=aux_width_monitor*4.6, y=aux_height_monitor*.1)

Slider_Y1 = tkinter.Scale(pesNewProject,
            from_=0, to=.5, resolution=0.01,
            orient=tkinter.VERTICAL, width = aux_height_monitor*.3,  length=aux_height_monitor*3.9,
            fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
            activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
            showvalue=1, command = getValuesSliders)
Slider_Y1.config(font=(Font_1,11))
Slider_Y1.place(x=aux_width_monitor*.2, y=aux_height_monitor*1)

Slider_Y2 = tkinter.Scale(pesNewProject, 
            from_=.51, to=1, resolution=0.01,
            orient=tkinter.VERTICAL, width = aux_height_monitor*.3,  length=aux_height_monitor*3.9,
            fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
            activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
            showvalue=1, command = getValuesSliders)
Slider_Y2.config(font=(Font_1,11))
Slider_Y2.set(1)
Slider_Y2.place(x=aux_width_monitor*.2, y=aux_height_monitor*5.1)


Slider_Grados_Rotar = tkinter.Scale(pesNewProject, 
            from_=-180, to=180, resolution=1,
            orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*3.5,
            fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
            activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
            showvalue=1, command = getValuesSliders)
Slider_Grados_Rotar.config(font = (Font_1,10))
Slider_Grados_Rotar.set(0)
Slider_Grados_Rotar.place(x=aux_width_monitor*1, y=aux_height_monitor*9.7)
#%%Labels notebook pesNewProject (cut image)
Lbl_Slider_Grados_Rotar = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                              text = 'Degrees')
Lbl_Slider_Grados_Rotar.config(font=(Font_1,15))
Lbl_Slider_Grados_Rotar.place(x=aux_width_monitor*1, y=aux_height_monitor*9.1)

Lbl_Etr_Tamano_Caja = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                              text = 'X axis')
Lbl_Etr_Tamano_Caja.config(font=(Font_1,14))
Lbl_Etr_Tamano_Caja.place(x=aux_width_monitor*1, y=aux_height_monitor*10.7)

Lbl_Etr_Tamano_Caja_cm = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                              text = '(cm)')
Lbl_Etr_Tamano_Caja_cm.config(font=(Font_1,14))
Lbl_Etr_Tamano_Caja_cm.place(x=aux_width_monitor*2.7, y=aux_height_monitor*10.7)

Lbl2_Etr_Tamano_Caja = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                              text = 'Y axis')
Lbl2_Etr_Tamano_Caja.config(font=(Font_1,14))
Lbl2_Etr_Tamano_Caja.place(x=aux_width_monitor*1, y=aux_height_monitor*11.5)

Lbl2_Etr_Tamano_Caja_cm = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                              text = '(cm)')
Lbl2_Etr_Tamano_Caja_cm.config(font=(Font_1,14))
Lbl2_Etr_Tamano_Caja_cm.place(x=aux_width_monitor*2.7, y=aux_height_monitor*11.5)
#%%Entries notebook pesNewProject (cut image) 
Etr_Tamano_Caja = tkinter.Entry(pesNewProject, width = 8, bg = Fun_Rgb(C_Light_Dark),
                                fg = Fun_Rgb(C_White))
Etr_Tamano_Caja.config(font = (Font_1,13))
Etr_Tamano_Caja.place(x=aux_width_monitor*1.7, y=aux_height_monitor*10.7)
Etr_Tamano_Caja.insert(0,'1')

Etr2_Tamano_Caja = tkinter.Entry(pesNewProject, width = 8, bg = Fun_Rgb(C_Light_Dark),
                                fg = Fun_Rgb(C_White))
Etr2_Tamano_Caja.config(font = (Font_1,13))
Etr2_Tamano_Caja.place(x=aux_width_monitor*1.7, y=aux_height_monitor*11.5)
Etr2_Tamano_Caja.insert(0,'1')
#%%Sliders notebook pesNewProject (edit image)
#-------------------- Sliders to edit images (right side) -------------------- 
Lbl_Slider_1 = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                             text = 'Color')
Lbl_Slider_1.config(font=(Font_1,20))
Lbl_Slider_1.place(x=aux_width_monitor*8.2, y=aux_height_monitor*.2)

#Slider 1
Lbl_Slider_RojoText_1 = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                                      text = 'R')
Lbl_Slider_RojoText_1.config(font = (Font_1,20))
Lbl_Slider_RojoText_1.place(x=aux_width_monitor*8.2, y=aux_height_monitor*1)

Slider_Rojo = tkinter.Scale(pesNewProject, 
        from_=0, to=255, resolution=1,
        orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*2.5,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1, command = getValuesSliders)    
Slider_Rojo.set(255)
Slider_Rojo.config(font = (Font_1,12))
Slider_Rojo.place(x=aux_width_monitor*8.5, y=aux_height_monitor*1)

#Slider 2
Lbl_Slider_VerdeText_1 = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                                       text = 'G')
Lbl_Slider_VerdeText_1.config(font = (Font_1,20))
Lbl_Slider_VerdeText_1.place(x=aux_width_monitor*8.2, y=aux_height_monitor*2.1)

Slider_Verde = tkinter.Scale(pesNewProject, 
        from_=0, to=255, resolution=1,
        orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*2.5,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1, command = getValuesSliders)
Slider_Verde.set(255)
Slider_Verde.config(font = (Font_1,12))
Slider_Verde.place(x=aux_width_monitor*8.5, y=aux_height_monitor*2)

#Slider 3
Lbl_Slider_AzulText_1 = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                                      text = 'B')
Lbl_Slider_AzulText_1.config(font = (Font_1,20))
Lbl_Slider_AzulText_1.place(x=aux_width_monitor*8.2, y=aux_height_monitor*3)
Slider_Azul = tkinter.Scale(pesNewProject, 
        from_=0, to=255, resolution=1,
        orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*2.5,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1, command = getValuesSliders)
Slider_Azul.set(255)
Slider_Azul.config(font = (Font_1,12))
Slider_Azul.place(x=aux_width_monitor*8.5, y=aux_height_monitor*3)

#Slider Desviación
Lbl_Slider_Desviacio = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                             text = 'Range')
Lbl_Slider_Desviacio.config(font=(Font_1,15))
Lbl_Slider_Desviacio.place(x=aux_width_monitor*13.5, y=aux_height_monitor*.2)

Slider_Desviacion = tkinter.Scale(pesNewProject, 
        from_=0, to=150, resolution=1,
        orient=tkinter.VERTICAL, width = aux_height_monitor*.3,  length= aux_width_monitor*2,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1, command = getValuesSliders)
Slider_Desviacion.set(0)
Slider_Desviacion.config(font = (Font_1,14))
Slider_Desviacion.place(x=aux_width_monitor*13.5, y=aux_height_monitor*.7)

Rgb_Can = Canvas(pesNewProject, width=int(aux_width_monitor*2), 
                 height= int(aux_width_monitor*2), bg=Fun_Rgb(C_Primary))
Cuadro_Rgb2 =  Rgb_Can.create_rectangle(0, 0, aux_width_monitor*.7, aux_width_monitor*2.1, outline=Fun_Rgb(C_White), width=0)
Cuadro_Rgb1 =  Rgb_Can.create_rectangle(aux_width_monitor*.7, 0, aux_width_monitor*1.4, aux_width_monitor*2.1, outline=Fun_Rgb(C_White), width=0)
Cuadro_Rgb3 =  Rgb_Can.create_rectangle(aux_width_monitor*1.4, 0, aux_width_monitor*2.1, aux_width_monitor*2.1, outline=Fun_Rgb(C_White
                                                                                                                                ), width=0)
Rgb_Can.place(x=aux_width_monitor*11.2, y=aux_height_monitor*.7)  

imgCubo = Fun_Size(Dir_Images  +'cubo2.png',.2*aux_size)
lblCubo = Label(pesNewProject, bg = Fun_Rgb(C_Primary), 
                                    image = imgCubo)
lblCubo.place(x=aux_width_monitor*5.5,y=aux_height_monitor*9.2)

#filtros
Lbl_Filtro_1 = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                             text = 'Filter')
Lbl_Filtro_1.config(font = (Font_1,20))
Lbl_Filtro_1.place(x=aux_width_monitor*8.2, y=aux_height_monitor*4.5)

Var_Filtro = tkinter.IntVar()
RdBtn_1 = tkinter.Radiobutton(pesNewProject, bd=0, fg = Fun_Rgb(C_Dark),
                              bg = Fun_Rgb(C_Light_Dark), 
                              activebackground=Fun_Rgb(C_White),
                              text="Black & White - Weak  ", variable=Var_Filtro, 
                              value=1, indicatoron=0, width = 23, command = lambda: getValuesSliders(1))
RdBtn_1.config(font = (Font_1,15))
RdBtn_1.place(x=aux_width_monitor*8.2, y=aux_height_monitor*5.4)
RdBtn_2 = tkinter.Radiobutton(pesNewProject, bd=0, fg = Fun_Rgb(C_Dark),
                              bg = Fun_Rgb(C_Light_Dark), 
                              activebackground=Fun_Rgb(C_White),
                              text="Black & White - Strong", variable=Var_Filtro, 
                              value=2, indicatoron=0, width = 23, command = lambda: getValuesSliders(2))
RdBtn_2.config(font = (Font_1,15))
RdBtn_2.place(x=aux_width_monitor*8.2, y=aux_height_monitor*6.2)
RdBtn_3 = tkinter.Radiobutton(pesNewProject, bd=0, fg = Fun_Rgb(C_Dark),
                              bg = Fun_Rgb(C_Light_Dark), 
                              activebackground=Fun_Rgb(C_White),
                              text="Uniform - Weak       ", variable=Var_Filtro, 
                              value=3, indicatoron=0, width = 22, command = lambda: getValuesSliders(3))
RdBtn_3.config(font = (Font_1,15))
RdBtn_3.place(x=aux_width_monitor*11.4, y=aux_height_monitor*5.4)
RdBtn_4 = tkinter.Radiobutton(pesNewProject, bd=0, fg = Fun_Rgb(C_Dark),
                              bg = Fun_Rgb(C_Light_Dark), 
                              activebackground=Fun_Rgb(C_White),
                              text="Uniform - Strong     ", variable=Var_Filtro, 
                              value=4, indicatoron=0, width = 22, command = lambda: getValuesSliders(4))
RdBtn_4.config(font = (Font_1,15))
RdBtn_4.place(x=aux_width_monitor*11.4, y=aux_height_monitor*6.2)
RdBtn_5 = tkinter.Radiobutton(pesNewProject, bd=0, fg = Fun_Rgb(C_Dark),
                              bg = Fun_Rgb(C_Light_Dark), 
                              activebackground=Fun_Rgb(C_White),
                              text="No Filter             ", variable=Var_Filtro, 
                              value=5, indicatoron=0, width = 23, command = lambda: getValuesSliders(5))
RdBtn_5.config(font = (Font_1,15))
RdBtn_5.place(x=aux_width_monitor*8.2, y=aux_height_monitor*7)

Var_Filtro.get()

#Otros
Lbl_Filtro_2 = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                             text = 'Threshold')
Lbl_Filtro_2.config(font = (Font_1,18))
Lbl_Filtro_2.place(x=aux_width_monitor*8.2, y=aux_height_monitor*8)

Entr_Umbral = tkinter.Scale(pesNewProject, 
        from_= 0, to=1, resolution=0.01,
        orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*3,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1, command = getValuesSliders)
Entr_Umbral.config(font = (Font_1,12))
Entr_Umbral.set(.5)
Entr_Umbral.place(x=aux_width_monitor*8.2, y=aux_height_monitor*8.7)

Lbl_Filtro_3 = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                             text = 'Target size')
Lbl_Filtro_3.config(font = (Font_1,18))
Lbl_Filtro_3.place(x=aux_width_monitor*11.4, y=aux_height_monitor*8)        
Entr_Valor_Minimo_Animal = tkinter.Scale(pesNewProject, 
        from_= 0, to=50, resolution=1,
        orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*3,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue = 1)
Entr_Valor_Minimo_Animal.config(font = (Font_1,12))
Entr_Valor_Minimo_Animal.set(3)
Entr_Valor_Minimo_Animal.place(x=aux_width_monitor*11.4, y=aux_height_monitor*8.7)

lblConfigFileName =  tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                             text = 'Config file name')
lblConfigFileName.config(font = (Font_1,18))
lblConfigFileName.place(x=aux_width_monitor*8.2, y=aux_height_monitor*10)

auxConfigName = StringVar()
entConfigFile = Entry(pesNewProject, textvariable = auxConfigName, bd =1, width = 40)
entConfigFile.config(font = (Font_1,12))
entConfigFile.place(x=aux_width_monitor*10, y = aux_height_monitor*10.1)
#%%Bnt Funciones Ventana Cortar imagen
Btn_Ver_Imagen = tkinter.Button(pesNewProject, bd=0, fg = Fun_Rgb(C_White),
                                  bg = Fun_Rgb(C_Primary), activebackground=Fun_Rgb(C_Light_Dark),
                                  text = ' Restart ', highlightbackground = Fun_Rgb(C_Light_Dark), 
                                  command = lambda: getValuesSliders('Restart'))
Btn_Ver_Imagen.config(font = (Font_1,22))
Btn_Ver_Imagen.place(x=aux_width_monitor*8, y=aux_height_monitor*11)

########################
Btn_Next_Subject = tkinter.Button(pesNewProject, bd=0, fg = Fun_Rgb(C_White),
                          bg = Fun_Rgb(C_Primary), activebackground=Fun_Rgb(C_Light_Dark),
                          text = 'Next subject ', highlightbackground = Fun_Rgb(C_Light_Dark), 
                          command =Fun_Next_Subject)
Btn_Next_Subject.config(font = (Font_1,22))
Btn_Next_Subject.place(x=aux_width_monitor*10, y=aux_height_monitor*11)
###########################

Btn_Cortar_Imagen = tkinter.Button(pesNewProject, bd=0, fg = Fun_Rgb(C_White),
                                  bg = Fun_Rgb(C_Primary), activebackground=Fun_Rgb(C_Light_Dark),
                                  text = '   Save   ', highlightbackground = Fun_Rgb(C_Light_Dark), 
                                  command =saveParameters)
Btn_Cortar_Imagen.config(font = (Font_1,22))
Btn_Cortar_Imagen.place(x=aux_width_monitor*12, y=aux_height_monitor*11)
#%%--------------------WIDGETS NOTEBOOK TRACK---------------------
#%%Canvas notebook Track
canTracking = Canvas(pesTracking, width=int(width_monitor), height=int(aux_height_monitor*14), bg=Fun_Rgb(C_Primary))

#left side
canTracking.create_rectangle(int(aux_width_monitor*1), int(aux_height_monitor*1), int(aux_width_monitor*8), int(aux_height_monitor*9), fill=Fun_Rgb(C_Dark), outline=Fun_Rgb(C_White), width=.1)

#right side
#father FILES
canTracking.create_rectangle(int(aux_width_monitor*1), int(aux_height_monitor*9.7), 
                              int(aux_width_monitor*8), int(aux_height_monitor*12), 
                              fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=.1)
#2 childs
canTracking.create_rectangle(int(aux_width_monitor*1.1), int(aux_height_monitor*10), 
                            int(aux_width_monitor*5), int(aux_height_monitor*10.7), 
                            fill=Fun_Rgb(C_Primary), outline=Fun_Rgb(C_White), width=1)
canTracking.create_rectangle(int(aux_width_monitor*1.1), int(aux_height_monitor*11), 
                            int(aux_width_monitor*5), int(aux_height_monitor*11.7), 
                            fill=Fun_Rgb(C_Primary), outline=Fun_Rgb(C_White), width=1)

#father Session parameters
canTracking.create_rectangle(int(aux_width_monitor*8.5), int(aux_height_monitor*7.5), 
                              int(aux_width_monitor*13.5), int(aux_height_monitor*11), 
                              fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=.1)
#child
canTracking.create_rectangle(int(aux_width_monitor*8.6), int(aux_height_monitor*7.6), 
                            int(aux_width_monitor*13.4), int(aux_height_monitor*10), 
                            fill=Fun_Rgb(C_Primary), outline=Fun_Rgb(C_White), width=1)

canTracking.create_rectangle(int(aux_width_monitor*8.6), int(aux_height_monitor*10.2), 
                            int(aux_width_monitor*13.4), int(aux_height_monitor*10.9), 
                            fill=Fun_Rgb(C_Primary), outline=Fun_Rgb(C_White), width=1)
canTracking.place(x=0,y=0) 

if theme == 1:
    canShowDataXY = Canvas(canTracking, width=int(aux_height_monitor*7), height=int(aux_height_monitor*5), 
                           bg=Fun_Rgb(C_White))
    canShowDataXY.place(x=aux_width_monitor*8.5, y=aux_height_monitor*1)
elif theme == 0:
    canShowDataXY = Canvas(canTracking, width=int(aux_height_monitor*7), height=int(aux_height_monitor*5), 
                           bg=Fun_Rgb(C_Dark))
    canShowDataXY.place(x=aux_width_monitor*8.5, y=aux_height_monitor*1)  
#%%Labels and entries
#Labels
lblSetParametersFiles = Label(pesTracking, text="Set tracking parameters", bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblSetParametersFiles.config(font = (Font_1,15))
lblSetParametersFiles.place(x=aux_width_monitor*1, y=aux_height_monitor*9.1)

lblSetSessionParameters = Label(pesTracking, text="Set session parameters", bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblSetSessionParameters.config(font = (Font_1,15))
lblSetSessionParameters.place(x=aux_width_monitor*8.5, y=aux_height_monitor*7)

LblSesionTime = tkinter.Label(pesTracking, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),  text = 'Time (sec)')
LblSesionTime.config(font = (Font_1,15))
LblSesionTime.place(x=aux_width_monitor*8.7, y=aux_height_monitor*7.7)

LblSujeto = tkinter.Label(pesTracking, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), text = 'Subject')
LblSujeto.config(font = (Font_1,15))
LblSujeto.place(x=aux_width_monitor*8.7, y=aux_height_monitor*8.3)

LblSession = tkinter.Label(pesTracking, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), text = 'Session')
LblSession.config(font = (Font_1,15))
LblSession.place(x=aux_width_monitor*8.7, y=aux_height_monitor*8.9)

LblGroup = tkinter.Label(pesTracking, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), text = 'Group')
LblGroup.config(font = (Font_1,15))
LblGroup.place(x=aux_width_monitor*8.7, y=aux_height_monitor*9.5)

lblSetSessionParameters = Label(pesTracking, text="Session name", bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblSetSessionParameters.config(font = (Font_1,13))
lblSetSessionParameters.place(x=aux_width_monitor*8.7, y=aux_height_monitor*10.3)

lblConfigFile = Label(pesTracking, text='Config: ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblConfigFile.config(font = (Font_1,15))
lblConfigFile.place(x=aux_width_monitor*1.2, y=aux_height_monitor*10.1)
CreateToolTip(lblConfigFile, text='Press button Open')

lblProjectFile = Label(pesTracking, text='Project: ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblProjectFile.config(font = (Font_1,15))
lblProjectFile.place(x=aux_width_monitor*1.2, y=aux_height_monitor*11.1)
CreateToolTip(lblProjectFile, text='Press button Open')

LblPreviewTrack = tkinter.Label(pesTracking, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), text = 'Preview')
LblPreviewTrack.config(font = (Font_1,15))
LblPreviewTrack.place(x=aux_width_monitor*8.5, y = aux_height_monitor*.5)


Var_SaveVideo = IntVar()
Var_ShowPreview = IntVar()
radBtnSaveVideo = Checkbutton(pesTracking, text="Save video", variable=Var_SaveVideo,
                              bg = Fun_Rgb(C_Light_Dark),
                              onvalue=1, offvalue=0)
radBtnSaveVideo.config(font = (Font_1,15))
radBtnSaveVideo.place(x=aux_width_monitor*6, y = aux_height_monitor*10)

radBtnShowPreview = Checkbutton(pesTracking, text="Show preview", variable=Var_ShowPreview,
                                bg = Fun_Rgb(C_Light_Dark),
                                onvalue=1, offvalue=0)
radBtnShowPreview.config(font = (Font_1,15))
radBtnShowPreview.place(x=aux_width_monitor*6, y = aux_height_monitor*10.5)

#Entries
varTime = StringVar()
varSubject = StringVar()
varSession = StringVar()
varGroup = StringVar()
varSessionName = StringVar()

entTime = Entry(pesTracking, textvariable = varTime, bd =1, width = 35)
entTime.config(font = (Font_1,12))
entTime.place(x=aux_width_monitor*10, y = aux_height_monitor*7.7)

entSubject = Entry(pesTracking, textvariable = varSubject, bd =1, width = 35)
entSubject.config(font = (Font_1,12))
entSubject.place(x=aux_width_monitor*10, y = aux_height_monitor*8.3)

entSession = Entry(pesTracking, textvariable = varSession, bd =1, width = 35)
entSession.config(font = (Font_1,12))
entSession.place(x=aux_width_monitor*10, y = aux_height_monitor*8.9)

entGroup = Entry(pesTracking, textvariable = varGroup, bd =1, width = 35)
entGroup.config(font = (Font_1,12))
entGroup.place(x=aux_width_monitor*10, y = aux_height_monitor*9.5)

entSessionName = Entry(pesTracking, textvariable = varSessionName, bd =1, width = 35)
entSessionName.config(font = (Font_1,12))
entSessionName.place(x=aux_width_monitor*10, y = aux_height_monitor*10.35)

#Bnt 
BntTrack = tkinter.Button(pesTracking, bd=0, fg = Fun_Rgb(C_White),
                        bg = Fun_Rgb(C_Primary), activebackground=Fun_Rgb(C_Light_Dark),
                        text = 'Track', highlightbackground = Fun_Rgb(C_Light_Dark), 
                        command =  TrackProject)
BntTrack.config(font = (Font_1,20))
BntTrack.place(x=aux_width_monitor*8.5, y = aux_height_monitor*11.2)  

btnOpenConfigFile = tkinter.Button(pesTracking, bd=0, fg = Fun_Rgb(C_White), 
                        bg = Fun_Rgb(C_Light_Dark), activebackground=Fun_Rgb(C_Primary),
                        text = 'Open', highlightbackground = Fun_Rgb(C_Light_Dark),
                        command = openConfigFile)
btnOpenConfigFile.config(font = (Font_1,15))
btnOpenConfigFile.place(x=aux_width_monitor*5.1, y = aux_height_monitor*10.1)

btnOpenProjectDirectory = tkinter.Button(pesTracking, bd=0, fg = Fun_Rgb(C_White), 
                        bg = Fun_Rgb(C_Light_Dark), activebackground=Fun_Rgb(C_Primary),
                        text = 'Open', highlightbackground = Fun_Rgb(C_Light_Dark), 
                        command = openProjectDirectoryToTrack)
btnOpenProjectDirectory.config(font = (Font_1,15))
btnOpenProjectDirectory.place(x=aux_width_monitor*5.1, y = aux_height_monitor*11.1)   

btnClearCanvas = tkinter.Button(pesTracking, bd=0, fg = Fun_Rgb(C_White), 
                        bg = Fun_Rgb(C_Primary), activebackground=Fun_Rgb(C_Light_Dark),
                        text = 'Clear', highlightbackground = Fun_Rgb(C_Light_Dark), 
                        command = clearCanvas)
btnClearCanvas.config(font = (Font_1,20))
btnClearCanvas.place(x=aux_width_monitor*12.5, y = aux_height_monitor*5)            
#%%--------------------MAILOOP---------------------
#%%Mainloop
# for i in range(10):
#     putCircleCanvas(canShowDataXY, i, i+1, 5, 1)
root.mainloop()
 