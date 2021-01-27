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
# print(theme, showTextImage, type(showTextImage))
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
Dir_Projects = 'Projects/'
Dir_Videos = 'Videos/'
Dir_Project_Images = '/Images/'
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
    Var_Tamaño_Lbl_X = int(((height_monitor/2)*1.99)-(aux_width_monitor*1.4))
    Var_Tamaño_Lbl_Y = int(((height_monitor/2)*1.37)-(aux_width_monitor*1.3))
    
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
        
    return(Img_Original_2)
#%%Fun imageRezicePesNewProject
def imageRezicePesNewProject(img):
    Var_Tamaño_Lbl_X = int(aux_width_monitor*3.25)-2
    Var_Tamaño_Lbl_Y = int(aux_height_monitor*4.7)-2
    
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
#%%FunSetResolution
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
    
    lblNumberImage = Label(pesCutVideo, text='Image '+str(currentPicture)+ ' of '+str(len(List_Contenido)) +'   ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
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
            pathNewProject = filedialog.asksaveasfilename(initialdir = Dir_Projects,
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
        currentPicture = len(List_Contenido)
    if currentPicture <= 0:
        currentPicture = 0
    
    img = Dir_Project_Img+str(List_Contenido[currentPicture])
    milisecond = img.split(Dir_Project_Img)[1]
    lblNumberImage.place_forget()
    
    lblNumberImage = Label(pesCutVideo, text='Image '+str(currentPicture)+ 
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
                cv2.moveWindow('Press Esc to abort', int(aux_width_monitor*1), int(aux_height_monitor*2.9))
                
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
            cv2.moveWindow('Press Esc to abort', int(aux_width_monitor*1), int(aux_height_monitor*2.9))
            
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
            cv2.moveWindow('Press Esc to abort', int(aux_width_monitor*1), int(aux_height_monitor*2.9))
            
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
    Lbl_Img_Original.place(x = (aux_width_monitor*.7), y = (aux_height_monitor*1)+1)
#%%Fun getValuesSliders
def getValuesSliders(value):
    global Dialog_Video_File_Aux, Lbl_Img_Original, Dialog_Video_File_Aux_2, Img_Original
    global Ruta_Imagen, Seleccion_Track
    
    # if Seleccion_Track == 0:
    #     messagebox.showinfo("Error", "Select a traking option")
    
    X1 = Slider_X1.get()
    X2 = Slider_X2.get()
    Y1 = Slider_Y1.get()
    Y2 = Slider_Y2.get()
    Rotar = Slider_Grados_Rotar.get()
    
    textEntryX = Etr_Tamano_Caja.get()
    textEntryY = Etr2_Tamano_Caja.get()
    textEntryZ = Etr3_Tamano_Caja.get()
    
    LblXAxis = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                             text = textEntryX)
    LblXAxis.config(font = (Font_1,12))
    LblXAxis.place(x=aux_width_monitor*5.2, y=aux_height_monitor*3.5)
    
    LblYAxis = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                             text = textEntryY)
    LblYAxis.config(font = (Font_1,12))
    LblYAxis.place(x=aux_width_monitor*6.8, y=aux_height_monitor*3.5)
    
    LblZAxis = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                             text = textEntryZ)
    LblZAxis.config(font = (Font_1,12))
    LblZAxis.place(x=aux_width_monitor*7, y=aux_height_monitor*2.5)
    
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
        Lbl_Img_Original.place(x = (aux_width_monitor*.7), y = (aux_height_monitor*1)+1)
    except:
        Seleccion_Track = 0
   
    if value == 'a':
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
            Lbl_Img_Original.place(x = (aux_width_monitor*.7), y = (aux_height_monitor*1)+1)   
        except:
            Seleccion_Track = 0 
#%%Fun_Next_Subject
def Fun_Next_Subject(): 
    
    global number_subject, Mat_RGB, Seleccion_Track
      
    if Seleccion_Track == 0:
        messagebox.showinfo("Error", "Select a traking option")
    
    aux_count = 0
    Var_R = int(Slider_Rojo.get())
    Var_G = int(Slider_Verde.get())
    Var_B = int(Slider_Azul.get())
    Var_Des = int(Slider_Desviacion.get())
    Var_Umbral = float(Entr_Umbral.get())
    Img_Filtro = Var_Filtro.get()
    Mat_RGB2 = ([Var_R, Var_G, Var_B, Var_Des, Var_Umbral, Img_Filtro])
    
    global Lbl_Img_Original, Lbl_Img_Original_Aux
    Lbl_Img_Original.place_forget()
    # Lbl_Img_Original_Aux.place_forget()
    
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
    Lbl_Img_Original.place(x = (aux_width_monitor*.7), y = (aux_height_monitor*1)+1) 
    
    if aux_count == 0:
        Mat_RGB[number_subject][:]= Mat_RGB2
        number_subject += 1 
        
        Slider_Rojo.set(0)
        Slider_Verde.set(0)
        Slider_Azul.set(0)
        Slider_Desviacion.set(0)
        Entr_Umbral.set(.5)
        Var_Filtro.set(0)      
#%% Fun_Editar_Todas_Imagenes
def Fun_Editar_Todas_Imagenes():
    global Mat_RGB, number_subject, Dialog_Video_File_Aux_2, Dialog_Video_File_Aux, Ruta_Imagen, Seleccion_Track
    global Dialog_Video_File_Aux, Ruta_Proyecto, Ruta_Video, Carpeta_Imagenes, Ruta_Carpeta_Imagenes, Nombre_Archivo
    # print( Dialog_Video_File_Aux, Ruta_Proyecto, Ruta_Video, Carpeta_Imagenes, Ruta_Carpeta_Imagenes, Nombre_Archivo)
    
    if Seleccion_Track == 0:
        messagebox.showinfo("Error", "Select a traking option")
    
    if Seleccion_Track == 1:
        pathProjectImage = Ruta_Proyecto + Nombre_Archivo + '/Images/'
        pathProject = Ruta_Proyecto + Nombre_Archivo 
        plt.rcParams['image.cmap'] = 'gray'
        plt.show()
        X1 = Slider_X1.get()
        X2 = Slider_X2.get()
        Y1 = Slider_Y1.get()
        Y2 = Slider_Y2.get()
        Rotar = Slider_Grados_Rotar.get()
        Dev_Espacio_Tamano = Etr_Tamano_Caja.get()
        Img_Filtro = Var_Filtro.get()
        Track_MinSize = float(Entr_Valor_Minimo_Animal.get())
        Img_Original = imageio.imread(Dialog_Video_File_Aux)
        Img_Original = Img_Original[round(Img_Original.shape[0]*Y1):round(Img_Original.shape[0]*Y2),
                                    round(Img_Original.shape[1]*X1):round(Img_Original.shape[1]*X2)]
        Img_Original = PIL.Image.open(Dialog_Video_File_Aux).rotate(Rotar)
        Img_WebCam = np.copy(Img_Original)
        os.remove(Dialog_Video_File_Aux)
        os.remove(Dialog_Video_File_Aux_2)
        
        if number_subject == 0:
            Var_R = Slider_Rojo.get()
            Var_G = Slider_Verde.get()
            Var_B = Slider_Azul.get()
            Var_Des = Slider_Desviacion.get()
            Var_Umbral = float(Entr_Umbral.get())
            Mat_RGB = ([Var_R, Var_G, Var_B, Var_Des, Var_Umbral])
        
            List_Contenido = ordenarAlfabeticamente(os.listdir(pathProjectImage))
       
            #Remplazar Imagenes
            #con esta sección de código se CORTAN, no editan, todas las imagenés
            # for elemento in List_Contenido:
            #     ruta = pathProjectImage
            #     documento = ruta + elemento
                
            #     Img_Original = imageio.imread(documento)
            #     Img_Original = Img_Original[round(Img_Original.shape[0]*Y1):round(Img_Original.shape[0]*Y2),
            #                                 round(Img_Original.shape[1]*X1):round(Img_Original.shape[1]*X2)]
            #     imageio.imsave(documento, Img_Original)
            #     Img_Original = PIL.Image.open(documento).rotate(Rotar)
        
            #     Img_WebCam = np.copy(Img_Original)
            #     imageio.imsave(documento, Img_WebCam)
            
            #Guardar txt
            Arr_Variables = [str(Seleccion_Camara), str(Seleccion_Resolucion),
                             str(X1), str(X2), str(Y1), str(Y2), str(Rotar), 
                             str(Dev_Espacio_Tamano), str(Var_R), str(Var_G), str(Var_B),
                             str(Var_Des), str(Var_Umbral), str(Img_Filtro), 
                             str(Track_MinSize), 
                             str(Img_WebCam.shape[1]),str(Img_WebCam.shape[0]), str(number_subject)] 
            
            Archivo_Variables = open(pathProject + '/' + 'Config_' + Nombre_Archivo +'.txt','w')
            for i in Arr_Variables:
                Archivo_Variables.write(i +'\n')
            Archivo_Variables.close()
                
            if Seleccion_Track == 1:
                messagebox.showinfo("Finalized", "Parameters has been saved")
            elif Seleccion_Track == 2:
                messagebox.showinfo("Finalized", "Images has been edited")
            elif Seleccion_Track == 3:
                messagebox.showinfo("Finalized", "Open Parameters")
            
        else:
            c = 0
            for q in range(len(Mat_RGB)):
                suma = np.sum(Mat_RGB[c][:], axis=0)
                if (suma == 0):
                    Mat_RGB = np.delete(Mat_RGB[:,:], c, axis=0)
                    c = c
                else:
                    c+=1
            
            for elemento in List_Contenido:
                ruta = pathProjectImage
                documento = ruta + elemento
                
                Img_Original = imageio.imread(documento)/255.0
                Img_Original = Img_Original[round(Img_Original.shape[0]*Y1):round(Img_Original.shape[0]*Y2),
                                round(Img_Original.shape[1]*X1):round(Img_Original.shape[1]*X2)]
                imageio.imsave(documento, Img_Original)
                Img_Original = PIL.Image.open(documento).rotate(Rotar)
        
                Img_WebCam = np.copy(Img_Original)
                imageio.imsave(documento, Img_WebCam)
            
            if Seleccion_Track == 1:
                messagebox.showinfo("Finalized", "Parameters have been saved")
            elif Seleccion_Track == 2:
                messagebox.showinfo("Finalized", "Images have been edited")
            elif Seleccion_Track == 3:
                messagebox.showinfo("Finalized", "Open Parameters")
            
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
                             str(Dev_Espacio_Tamano), str(Track_MinSize), 
                             str(Img_WebCam.shape[1]),str(Img_WebCam.shape[0]), str(number_subject)]      
            
            Archivo_Variables = open(pathProject + '/' + 'Config_' + Nombre_Archivo +'.txt','w')
            cont_Grabar = 0
            for j in Arr_Variables:
                Archivo_Variables.write(j +'\n')
                cont_Grabar += 1
                if cont_Grabar == 8:
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
#%%-------------WIDGETS APLICATION-------------
#%%Principal window
root = Tk()
root.title('Walden Tracking System v-3.0')
root.geometry(str(width_monitor)+'x'+str(height_monitor-70)+'+0+0') 
root.iconbitmap(Dir_Images+"Icon.ico")
root.resizable(0,0)
root.config(bg = Fun_Rgb(C_Primary))
root.isStopped = False
#%%Global variables   
global Lbl_Img_Original, List_Contenido, pathImageProject, textEnt, currentProject, openProjectVar, lblVideo

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
img3 = PIL.Image.open(Dir_Images+'newVideoProject.png')
useImg3 = ImageTk.PhotoImage(img3)
img4 = PIL.Image.open(Dir_Images+'open.png')
useImg4 = ImageTk.PhotoImage(img4)
img5 = PIL.Image.open(Dir_Images+'video.jpg')
useImg5 = ImageTk.PhotoImage(img5)
img6 = PIL.Image.open(Dir_Images+'changeCamera.png')
useImg6 = ImageTk.PhotoImage(img6)
img7 = PIL.Image.open(Dir_Images+'openVideo.png')
useImg7 = ImageTk.PhotoImage(img7)
# img8 = PIL.Image.open(Dir_Images+'data.png')
# useImg8 = ImageTk.PhotoImage(img8)
# img9 = PIL.Image.open(Dir_Images+'user.png')
# useImg9 = ImageTk.PhotoImage(img9)


iconTool_Options = Button(toolbar, image=useImg1, text="Settings", width=20, command=openSettings)
iconTool_Options.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconTool_Options, text = 'Aettings')

iconTool_CutVideo = Button(toolbar, image=useImg5, text="Select video to cut", width=20, command=SelectVideo)
iconTool_CutVideo.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconTool_CutVideo, text = 'Select video to cut')

iconOpneImageProject = Button(toolbar, image=useImg7, text="Open image project", width=20, command=openImage)
iconOpneImageProject.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconOpneImageProject, text = 'Open image project')

iconOpenVideo = Button(toolbar, image=useImg2, text="Open video project", width=20, command=openVideo)
iconOpenVideo.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconOpenVideo, text = 'Open video project')

iconNewProject = Button(toolbar, image=useImg3, text="New video project", width=20, command=newVideoProject)
iconNewProject.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconNewProject, text = 'New video project')



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
Menu_Opc1.add_command(label='Select video to cut', command=SelectVideo)
Menu_Opc1.add_command(label='Open image project', command=openImage) 
Menu_Opc1.add_command(label='Open video', command=openVideo) 
Menu_Opc1.add_separator()
Menu_Opc1.add_command(label='New video project', command = newVideoProject)
Menu_Opc1.add_command(label='Get RGB values', command = Fun_Get_RGB)
Menu_Opc1.add_separator()
Menu_Opc1.add_command(label='Data analysis')
Menu_Opc1.add_command(label='User information')
Menu_Opc1.add_separator()
Menu_Opc1.add_command(label='Settings', command = openSettings)
Menu_Opc1.add_separator()
Menu_Opc1.add_command(label='License', command=info)  
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
pesCutVideo = tkinter.Frame(notebook, background = Fun_Rgb(C_Primary))
pesNewProject = tkinter.Frame(notebook, background = Fun_Rgb(C_Light_Dark))
pesTracking = tkinter.Frame(notebook, background = Fun_Rgb(C_Dark))

notebook.add(pesNewProject, text = 'New project')
notebook.add(pesCutVideo, text = '  Videos', compound=LEFT)
notebook.add(pesTracking, text= 'Track')
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

lblNumberImage = Label(pesCutVideo, text='Image '+str(currentPicture)+ ' of '+str(len(List_Contenido)) +'       ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblNumberImage.config(font = (Font_1,15))
lblNumberImage.place(x=aux_width_monitor*1, y=aux_height_monitor*9.1)

lblOpenVideo = Label(pesCutVideo, text = 'Video info', bg= Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblOpenVideo.config(font = (Font_1, 15))
lblOpenVideo.place(x = aux_width_monitor*4.5, y = aux_height_monitor*9.1)

lblImageProject = Label(pesCutVideo, text='Project: ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblImageProject.config(font = (Font_1,15))
lblImageProject.place(x=aux_width_monitor*8.5, y=aux_height_monitor*9.2)

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
#%%-------------WIDGETS NEW PROJECT-------------
#%%Canvas notebook pesNewProject
canNewProject = Canvas(pesNewProject, width=int(width_monitor), height=int(aux_height_monitor*14), bg=Fun_Rgb(C_Primary))

#left side
canNewProject.create_rectangle(int(aux_width_monitor*.7), int(aux_height_monitor*1), 
                               int(aux_width_monitor*4.75), int(aux_width_monitor*3.2), fill=Fun_Rgb(C_Dark), outline=Fun_Rgb(C_White), width=.1)
canNewProject.create_rectangle(int(aux_width_monitor*.7), int(aux_height_monitor*7),
                               int(aux_width_monitor*4.75), int(aux_width_monitor*6.6), fill=Fun_Rgb(C_Dark), outline=Fun_Rgb(C_White), width=.1)
        
# canNewProject.create_rectangle(int(aux_width_monitor*1), int(aux_height_monitor*1), int(aux_width_monitor*8), int(aux_height_monitor*9), fill=Fun_Rgb(C_Dark), outline=Fun_Rgb(C_White), width=.1)
canNewProject.place(x=0,y=0) 
#%%Sliders notebook pesNewProject (cut image)
#-------------------- Sliders to cut images (left side) --------------------
Slider_X1 = tkinter.Scale(pesNewProject, 
            from_=0, to=.5, resolution=0.01,
            orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*2,
            fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
            activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
            showvalue=1, command = getValuesSliders)
Slider_X1.config(font=(Font_1,11))
Slider_X1.place(x=int(aux_width_monitor*.7), y=int(aux_height_monitor*.1))

Slider_X2 = tkinter.Scale(pesNewProject, 
            from_=.51, to=1, resolution=0.01,
            orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*2,
            fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
            activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
            showvalue=1, command = getValuesSliders)
Slider_X2.config(font=(Font_1,11))
Slider_X2.set(1)
Slider_X2.place(x=aux_width_monitor*2.8, y=aux_height_monitor*.1)

Slider_Y1 = tkinter.Scale(pesNewProject,
            from_=0, to=.5, resolution=0.01,
            orient=tkinter.VERTICAL, width = aux_height_monitor*.3,  length=aux_height_monitor*2.2,
            fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
            activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
            showvalue=1, command = getValuesSliders)
Slider_Y1.config(font=(Font_1,11))
Slider_Y1.place(x=aux_width_monitor*.1, y=aux_height_monitor*1)

Slider_Y2 = tkinter.Scale(pesNewProject, 
            from_=.51, to=1, resolution=0.01,
            orient=tkinter.VERTICAL, width = aux_height_monitor*.3,  length=aux_height_monitor*2.2,
            fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
            activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
            showvalue=1, command = getValuesSliders)
Slider_Y2.config(font=(Font_1,11))
Slider_Y2.set(1)
Slider_Y2.place(x=aux_width_monitor*.1, y=aux_height_monitor*3.6)


Slider_Grados_Rotar = tkinter.Scale(pesNewProject, 
            from_=-180, to=180, resolution=1,
            orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*2.5,
            fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
            activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
            showvalue=1, command = getValuesSliders)
Slider_Grados_Rotar.config(font = (Font_1,10))
Slider_Grados_Rotar.set(0)
Slider_Grados_Rotar.place(x=aux_width_monitor*5, y=aux_height_monitor*5)


Slider2_X1 = tkinter.Scale(pesNewProject, 
        from_=0, to=.5, resolution=0.01,
        orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*2,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1)
Slider2_X1.config(font=(Font_1,11))
Slider2_X1.place(x=int(aux_width_monitor*.7), y=int(aux_height_monitor*6))

Slider2_X2 = tkinter.Scale(pesNewProject, 
        from_=.51, to=1, resolution=0.01,
        orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*2,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1)
Slider2_X2.config(font=(Font_1,11))
Slider2_X2.set(1)
Slider2_X2.place(x=aux_width_monitor*2.8, y=aux_height_monitor*6)

Slider2_Y1 = tkinter.Scale(pesNewProject,
        from_=0, to=.5, resolution=0.01,
        orient=tkinter.VERTICAL, width = aux_height_monitor*.3,  length=aux_height_monitor*2.2,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1)
Slider2_Y1.config(font=(Font_1,11))
Slider2_Y1.place(x=aux_width_monitor*.1, y=aux_height_monitor*7)

Slider2_Y2 = tkinter.Scale(pesNewProject, 
        from_=.51, to=1, resolution=0.01,
        orient=tkinter.VERTICAL, width = aux_height_monitor*.3,  length=aux_height_monitor*2.2,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1)
Slider2_Y2.config(font=(Font_1,11))
Slider2_Y2.set(1)
Slider2_Y2.place(x=aux_width_monitor*.1, y=aux_height_monitor*9.6)


Slider2_Grados_Rotar = tkinter.Scale(pesNewProject, 
        from_=-90, to=90, resolution=1,
        orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*2.5,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1)
Slider2_Grados_Rotar.config(font = (Font_1,11))
Slider2_Grados_Rotar.set(0)
Slider2_Grados_Rotar.place(x=aux_width_monitor*5, y=aux_height_monitor*10.5)
#%%Labels notebook pesNewProject (cut image)
Lbl_Slider_Grados_Rotar = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                              text = 'Degrees')
Lbl_Slider_Grados_Rotar.config(font=(Font_1,12))
Lbl_Slider_Grados_Rotar.place(x=aux_width_monitor*4.9, y=aux_height_monitor*4.5)

Lbl2_Slider_Grados_Rotar = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                              text = 'Degrees')
Lbl2_Slider_Grados_Rotar.config(font=(Font_1,12))
Lbl2_Slider_Grados_Rotar.place(x=aux_width_monitor*4.9, y=aux_height_monitor*10)

Lbl_Etr_Tamano_Caja = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                              text = 'X axis')
Lbl_Etr_Tamano_Caja.config(font=(Font_1,14))
Lbl_Etr_Tamano_Caja.place(x=aux_width_monitor*5.3, y=aux_height_monitor*6.7)

Lbl_Etr_Tamano_Caja_cm = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                              text = '(cm)')
Lbl_Etr_Tamano_Caja_cm.config(font=(Font_1,14))
Lbl_Etr_Tamano_Caja_cm.place(x=aux_width_monitor*7, y=aux_height_monitor*6.7)

Lbl2_Etr_Tamano_Caja = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                              text = 'Y axis')
Lbl2_Etr_Tamano_Caja.config(font=(Font_1,14))
Lbl2_Etr_Tamano_Caja.place(x=aux_width_monitor*5.3, y=aux_height_monitor*7.7)

Lbl2_Etr_Tamano_Caja_cm = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                              text = '(cm)')
Lbl2_Etr_Tamano_Caja_cm.config(font=(Font_1,14))
Lbl2_Etr_Tamano_Caja_cm.place(x=aux_width_monitor*7, y=aux_height_monitor*7.7)

Lbl3_Etr_Tamano_Caja = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                              text = 'Z axis')
Lbl3_Etr_Tamano_Caja.config(font=(Font_1,14))
Lbl3_Etr_Tamano_Caja.place(x=aux_width_monitor*5.3, y=aux_height_monitor*8.7)

Lbl3_Etr_Tamano_Caja_cm = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                              text = '(cm)')
Lbl3_Etr_Tamano_Caja_cm.config(font=(Font_1,14))
Lbl3_Etr_Tamano_Caja_cm.place(x=aux_width_monitor*7, y=aux_height_monitor*8.7)
#%%Entries notebook pesNewProject (cut image) 
Etr_Tamano_Caja = tkinter.Entry(pesNewProject, width = 8, bg = Fun_Rgb(C_Light_Dark),
                                fg = Fun_Rgb(C_White))
Etr_Tamano_Caja.config(font = (Font_1,13))
Etr_Tamano_Caja.place(x=aux_width_monitor*6, y=aux_height_monitor*6.7)
Etr_Tamano_Caja.insert(0,'1')

Etr2_Tamano_Caja = tkinter.Entry(pesNewProject, width = 8, bg = Fun_Rgb(C_Light_Dark),
                                fg = Fun_Rgb(C_White))
Etr2_Tamano_Caja.config(font = (Font_1,13))
Etr2_Tamano_Caja.place(x=aux_width_monitor*6, y=aux_height_monitor*7.7)
Etr2_Tamano_Caja.insert(0,'1')

Etr3_Tamano_Caja = tkinter.Entry(pesNewProject, width = 8, bg = Fun_Rgb(C_Light_Dark),
                                fg = Fun_Rgb(C_White))
Etr3_Tamano_Caja.config(font = (Font_1,13))
Etr3_Tamano_Caja.place(x=aux_width_monitor*6, y=aux_height_monitor*8.7)
Etr3_Tamano_Caja.insert(0,'1')
#%%Sliders notebook pesNewProject (edit image)
#-------------------- Sliders to edit images (right side) -------------------- 
Lbl_Slider_1 = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                             text = 'Color')
Lbl_Slider_1.config(font=(Font_1,20))
Lbl_Slider_1.place(x=aux_width_monitor*8, y=aux_height_monitor*.7)

#Slider 1
Lbl_Slider_RojoText_1 = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                                      text = 'R')
Lbl_Slider_RojoText_1.config(font = (Font_1,20))
Lbl_Slider_RojoText_1.place(x=aux_width_monitor*8, y=aux_height_monitor*1.5)

Slider_Rojo = tkinter.Scale(pesNewProject, 
        from_=0, to=255, resolution=1,
        orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*2.5,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1, command = getValuesSliders)#Fun_Color_CuadroR)      
Slider_Rojo.set(255)
Slider_Rojo.config(font = (Font_1,12))
Slider_Rojo.place(x=aux_width_monitor*8.3, y=aux_height_monitor*1.5)


#Slider 2
Lbl_Slider_VerdeText_1 = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                                       text = 'G')
Lbl_Slider_VerdeText_1.config(font = (Font_1,20))
Lbl_Slider_VerdeText_1.place(x=aux_width_monitor*8, y=aux_height_monitor*2.9)
Slider_Verde = tkinter.Scale(pesNewProject, 
        from_=0, to=255, resolution=1,
        orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*2.5,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1, command = getValuesSliders)
Slider_Verde.set(255)
Slider_Verde.config(font = (Font_1,12))
Slider_Verde.place(x=aux_width_monitor*8.3, y=aux_height_monitor*2.9)

#Slider 3
Lbl_Slider_AzulText_1 = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                                      text = 'B')
Lbl_Slider_AzulText_1.config(font = (Font_1,20))
Lbl_Slider_AzulText_1.place(x=aux_width_monitor*8, y=aux_height_monitor*4.3)
Slider_Azul = tkinter.Scale(pesNewProject, 
        from_=0, to=255, resolution=1,
        orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*2.5,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1, command = getValuesSliders)
Slider_Azul.set(255)
Slider_Azul.config(font = (Font_1,12))
Slider_Azul.place(x=aux_width_monitor*8.3, y=aux_height_monitor*4.2)

#Slider Desviación
Lbl_Slider_Desviacio = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                             text = 'Range')
Lbl_Slider_Desviacio.config(font=(Font_1,20))
Lbl_Slider_Desviacio.place(x=aux_width_monitor*13.8, y=aux_height_monitor*.7)
Slider_Desviacion = tkinter.Scale(pesNewProject, 
        from_=0, to=150, resolution=1,
        orient=tkinter.VERTICAL, width = aux_height_monitor*.3,  length= aux_width_monitor*2,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1, command = getValuesSliders)
Slider_Desviacion.set(0)
Slider_Desviacion.config(font = (Font_1,14))
Slider_Desviacion.place(x=aux_width_monitor*13.9, y=aux_height_monitor*1.5)

Rgb_Can = Canvas(pesNewProject, width=int(aux_width_monitor*2), 
                 height= int(aux_width_monitor*2), bg=Fun_Rgb(C_Primary))
Cuadro_Rgb2 =  Rgb_Can.create_rectangle(0, 0, aux_width_monitor*.7, aux_width_monitor*2.1, outline=Fun_Rgb(C_White), width=0)
Cuadro_Rgb1 =  Rgb_Can.create_rectangle(aux_width_monitor*.7, 0, aux_width_monitor*1.4, aux_width_monitor*2.1, outline=Fun_Rgb(C_White), width=0)
Cuadro_Rgb3 =  Rgb_Can.create_rectangle(aux_width_monitor*1.4, 0, aux_width_monitor*2.1, aux_width_monitor*2.1, outline=Fun_Rgb(C_White
                                                                                                                                ), width=0)
Rgb_Can.place(x=aux_width_monitor*11.15, y=aux_height_monitor*1.5)  

imgCubo = Fun_Size(Dir_Images  +'cubo2.png',.2*aux_size)
lblCubo = Label(pesNewProject, bg = Fun_Rgb(C_Primary), 
                                    image = imgCubo)
lblCubo.place(x=aux_width_monitor*5.5,y=aux_height_monitor*1.5)

#filtros
Lbl_Filtro_1 = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White),
                             text = 'Filter')
Lbl_Filtro_1.config(font = (Font_1,20))
Lbl_Filtro_1.place(x=aux_width_monitor*8, y=aux_height_monitor*5.5)

Var_Filtro = tkinter.IntVar()
RdBtn_1 = tkinter.Radiobutton(pesNewProject, bd=0, fg = Fun_Rgb(C_Dark),
                              bg = Fun_Rgb(C_Primary), 
                              activebackground=Fun_Rgb(C_Light_Dark),
                              text="Black & White - Weak  ", variable=Var_Filtro, 
                              value=1, indicatoron=0, width = 23, command = lambda: getValuesSliders(1))
RdBtn_1.config(font = (Font_1,15))
RdBtn_1.place(x=aux_width_monitor*8, y=aux_height_monitor*6.4)
RdBtn_2 = tkinter.Radiobutton(pesNewProject, bd=0, fg = Fun_Rgb(C_Dark),
                              bg = Fun_Rgb(C_Primary), 
                              activebackground=Fun_Rgb(C_Light_Dark),
                              text="Black & White - Strong", variable=Var_Filtro, 
                              value=2, indicatoron=0, width = 23, command = lambda: getValuesSliders(2))
RdBtn_2.config(font = (Font_1,15))
RdBtn_2.place(x=aux_width_monitor*8, y=aux_height_monitor*7.2)
RdBtn_3 = tkinter.Radiobutton(pesNewProject, bd=0, fg = Fun_Rgb(C_Dark),
                              bg = Fun_Rgb(C_Primary), 
                              activebackground=Fun_Rgb(C_Light_Dark),
                              text="Uniform - Weak       ", variable=Var_Filtro, 
                              value=3, indicatoron=0, width = 22, command = lambda: getValuesSliders(3))
RdBtn_3.config(font = (Font_1,15))
RdBtn_3.place(x=aux_width_monitor*11.4, y=aux_height_monitor*6.4)
RdBtn_4 = tkinter.Radiobutton(pesNewProject, bd=0, fg = Fun_Rgb(C_Dark),
                              bg = Fun_Rgb(C_Primary), 
                              activebackground=Fun_Rgb(C_Light_Dark),
                              text="Uniform - Strong     ", variable=Var_Filtro, 
                              value=4, indicatoron=0, width = 22, command = lambda: getValuesSliders(4))
RdBtn_4.config(font = (Font_1,15))
RdBtn_4.place(x=aux_width_monitor*11.4, y=aux_height_monitor*7.2)
RdBtn_5 = tkinter.Radiobutton(pesNewProject, bd=0, fg = Fun_Rgb(C_Dark),
                              bg = Fun_Rgb(C_Primary), 
                              activebackground=Fun_Rgb(C_Light_Dark),
                              text="No Filter             ", variable=Var_Filtro, 
                              value=5, indicatoron=0, width = 23, command = lambda: getValuesSliders(5))
RdBtn_5.config(font = (Font_1,15))
RdBtn_5.place(x=aux_width_monitor*8, y=aux_height_monitor*8)

Var_Filtro.get()

#Otros
Lbl_Filtro_2 = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                             text = 'Threshold')
Lbl_Filtro_2.config(font = (Font_1,20))
Lbl_Filtro_2.place(x=aux_width_monitor*8, y=aux_height_monitor*9.1)

Entr_Umbral = tkinter.Scale(pesNewProject, 
        from_= 0, to=1, resolution=0.01,
        orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*3,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue=1, command = getValuesSliders)
Entr_Umbral.config(font = (Font_1,15))
Entr_Umbral.set(.5)
Entr_Umbral.place(x=aux_width_monitor*8, y=aux_height_monitor*10)

Lbl_Filtro_3 = tkinter.Label(pesNewProject, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), 
                             text = 'Target size')
Lbl_Filtro_3.config(font = (Font_1,20))
Lbl_Filtro_3.place(x=aux_width_monitor*11.4, y=aux_height_monitor*9.1)        
Entr_Valor_Minimo_Animal = tkinter.Scale(pesNewProject, 
        from_= 0, to=50, resolution=1,
        orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*3,
        fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
        activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
        showvalue = 1)
Entr_Valor_Minimo_Animal.config(font = (Font_1,15))
Entr_Valor_Minimo_Animal.set(3)
Entr_Valor_Minimo_Animal.place(x=aux_width_monitor*11.4, y=aux_height_monitor*10)
#%%Bnt Funciones Ventana Cortar imagen
Btn_Ver_Imagen = tkinter.Button(pesNewProject, bd=0, fg = Fun_Rgb(C_White),
                                  bg = Fun_Rgb(C_Primary), activebackground=Fun_Rgb(C_Light_Dark),
                                  text = ' Restart ', highlightbackground = Fun_Rgb(C_Light_Dark), 
                                  command = lambda: getValuesSliders('a'))
Btn_Ver_Imagen.config(font = (Font_1,20))
Btn_Ver_Imagen.place(x=aux_width_monitor*7.8, y=aux_height_monitor*11.6)

########################
Btn_Next_Subject = tkinter.Button(pesNewProject, bd=0, fg = Fun_Rgb(C_White),
                          bg = Fun_Rgb(C_Primary), activebackground=Fun_Rgb(C_Light_Dark),
                          text = 'Next subject ', highlightbackground = Fun_Rgb(C_Light_Dark), 
                          command =Fun_Next_Subject)
Btn_Next_Subject.config(font = (Font_1,20))
Btn_Next_Subject.place(x=aux_width_monitor*9.4, y=aux_height_monitor*11.6)
###########################

Btn_Cortar_Imagen = tkinter.Button(pesNewProject, bd=0, fg = Fun_Rgb(C_White),
                                  bg = Fun_Rgb(C_Primary), activebackground=Fun_Rgb(C_Light_Dark),
                                  text = '   Save   ', highlightbackground = Fun_Rgb(C_Light_Dark), 
                                  command =Fun_Editar_Todas_Imagenes)
Btn_Cortar_Imagen.config(font = (Font_1,20))
Btn_Cortar_Imagen.place(x=aux_width_monitor*11.5, y=aux_height_monitor*11.6)

Btn_Iniciar_Track = tkinter.Button(pesNewProject, bd=0, fg = Fun_Rgb(C_White),
                                  bg = Fun_Rgb(C_Primary), activebackground=Fun_Rgb(C_Light_Dark),
                                  text = 'Tracking ', highlightbackground = Fun_Rgb(C_Light_Dark), 
                                  )#command =Fun_Iniciar_Track)
Btn_Iniciar_Track.config(font = (Font_1,20))
Btn_Iniciar_Track.place(x=aux_width_monitor*13.1, y=aux_height_monitor*11.6)
#%%Mainloop
root.mainloop()
 