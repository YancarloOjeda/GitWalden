#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 18:00:53 2019

@author: Walden Modular Equipment
"""

#%%Libreias 
import tkinter 
import scipy
import imageio
import cv2
import os
import os.path
import re
import time
import random
import math
import statistics
import numpy as np
import serial
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from ast import literal_eval
from scipy import misc, ndimage
from tkinter import PhotoImage, messagebox, ttk, Canvas, filedialog, Tk, Frame, BOTH
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import serial.tools.list_ports
from sqlalchemy.sql.expression import column
from tkinter import font
from tkinter.font import Font
from tkinter.simpledialog import askstring
#from screeninfo import get_monitors
import matplotlib.image as mpimg

def Fun_Rgb(RGB):
    return "#%02x%02x%02x" % RGB  

def Fun_Size(img, size):
    img = Image.open(img)
    size_1 = img.size
    width = int(size_1[0]*size)
    height = int(size_1[1]*size)
    img = img.resize((width, height),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    return img

C_White = (255,255,255)
C_Black = (0,0,0)
C_Red = (255,0,0)
C_Green = (0,255,0)
C_Blue = (0,0,255)
C_Pal1 = (0,0,0)
C_Pal2 = (70,75,80)
C_Pal3 = (30,40,40)
C_Pal4 = (200,200,200)
C_Pal5 = (255,255,255)
C_Pal6 = (245,245,245)
C_Pal7 = (70,90,90)
C_Pal8 = (235,235,235)
Font_CV = cv2.FONT_HERSHEY_SIMPLEX
Font_1 = 'Sans'


         
#%%Diectorio_Programa
#Dir_Videos = '/home/yancarlo/WALDEN/Videos/'
#Dir_Proyecto = '/home/yancarlo/WALDEN/Projects/' 
#Dir_Datos = '/home/yancarlo/WALDEN/Data/'
#Dir_Archivo_PRef = '/home/yancarlo/WALDEN/Schedules'
#Dir_Archivo_Parametros = '/home/yancarlo/WALDEN/Config/'
#Dir_Archivo_Datos = '/home/yancarlo/WALDEN/Data/'
#Dir_Images = '/home/yancarlo/WALDEN/Images'

# Dir_Videos = 'C:/WALDEN/Videos/'
# Dir_Proyecto = 'C:/WALDEN/Projects/' 
# Dir_Datos = 'C:/WALDEN/Data/'
# Dir_Archivo_PRef = 'C:/WALDEN/Schedules'
# Dir_Archivo_Parametros = 'C:/WALDEN/Config/'
# Dir_Archivo_Datos = 'C:/WALDEN/Data/'
# Dir_Images = 'C:/WALDEN/Images/'

Dir_System = open("data.txt", "r")
Dir_System = Dir_System.read() + '/WTS-2.01/WTS-2.01/'


Dir_Videos = Dir_System+'Videos/'
Dir_Proyecto = Dir_System +'Projects/' 
Dir_Datos = Dir_System+'Data/'
Dir_Archivo_PRef = Dir_System+'Schedules'
Dir_Archivo_Parametros = Dir_System+'Config/'
Dir_Archivo_Datos = Dir_System+'Data/'
Dir_Images = Dir_System+'Images/'


#Dir_Videos = 'C:/Users/Laurent/Documents/WALDEN/Videos/'
#Dir_Proyecto = 'C:/Users/Laurent/Documents/WALDEN/Projects/' 
#Dir_Datos = 'C:/Users/Laurent/Documents/WALDEN/Data/'
#Dir_Archivo_PRef = 'C:/Users/Laurent/Documents/WALDEN/Schedules/'
#Dir_Archivo_Parametros = 'C:/Users/Laurent/Documents/WALDEN/Config/'
#Dir_Archivo_Datos = 'C:/Users/Laurent/Documents/WALDEN/Data/'
#Dir_Images = 'C:/Users/Laurent/Documents/WALDEN/Images'

#Dir_Videos = 'C:/Users/Walden/Google Drive/Desarrollo/2. Software/Walden Tracking System (WTS-001)/WTS_1.08/WALDEN/Videos/'
#Dir_Proyecto = 'C:/Users/Walden/Google Drive/Desarrollo/2. Software/Walden Tracking System (WTS-001)/WTS_1.08/WALDEN/Projects/' 
#Dir_Datos = 'C:/Users/Walden/Google Drive/Desarrollo/2. Software/Walden Tracking System (WTS-001)/WTS_1.08/WALDEN/Data/'
#Dir_Archivo_PRef = 'C:/Users/Walden/Google Drive/Desarrollo/2. Software/Walden Tracking System (WTS-001)/WTS_1.08/WALDEN/Schedules/'
#Dir_Archivo_Parametros = 'C:/Users/Walden/Google Drive/Desarrollo/2. Software/Walden Tracking System (WTS-001)/WTS_1.08/WALDEN/Config/'
#Dir_Archivo_Datos = 'C:/Users/Walden/Google Drive/Desarrollo/2. Software/Walden Tracking System (WTS-001)/WTS_1.08/WALDEN/Data/'
#Dir_Images = 'C:/Users/Walden/Google Drive/Desarrollo/2. Software/Walden Tracking System (WTS-001)/WTS_1.08/WALDEN/Images'

#%%Variables_Generales_Programa    
global arr_Color_Cuadro, arr_Color_Cuadro1, arr_Color_Cuadro2, Seleccion_Camara, Seleccion_Resolucion, Seleccion_Track 
arr_Color_Cuadro = np.zeros(4)
arr_Color_Cuadro1 = np.zeros(4)
arr_Color_Cuadro2 = np.zeros(4)
Seleccion_Camara = 0
Seleccion_Resolucion = 3
Seleccion_Track = 0
global number_subject, Mat_RGB 
Mat_RGB = np.zeros((16,6))
number_subject = 0

#%%Tamaño_Ventanas
aux_monitor = 0


#try:
#    for monitor in get_monitors():
#        aux_monitor += 1
#        if aux_monitor == 1:
#            monitor_size = monitor
#            aux_string_monitor = str(monitor_size)
#            aux_cortar = aux_string_monitor.split('monitor(')
#            aux_cortar = aux_cortar[1].split(')')
#            parameters_monitor = aux_cortar[0].split('x')
#            width_monitor = int(parameters_monitor[0])
#            parameters_monitor = parameters_monitor[1].split('+')
#            height_monitor = int(parameters_monitor[0])
#            X_monitor = int(parameters_monitor[1])
#            Y_monitor = int(parameters_monitor[2])
#            
#        if aux_monitor == 2:
#            monitor_size = monitor
#            aux_string_monitor = str(monitor_size)
#            aux_cortar = aux_string_monitor.split('monitor(')
#            aux_cortar = aux_cortar[1].split(')')
#            parameters_monitor = aux_cortar[0].split('x')
#            width_monitor = int(parameters_monitor[0])
#            parameters_monitor = parameters_monitor[1].split('+')
#            height_monitor = int(parameters_monitor[0])
#            X_monitor = int(parameters_monitor[1])
#            Y_monitor = int(parameters_monitor[2])
#            
#    if width_monitor > 1300:
#        width_monitor = 1366
#        height_monitor = 800
#        aux_size = .75
#    if width_monitor > 1024:
#        width_monitor = 1024
#        height_monitor = 768
#        aux_size = .65
#    else:
#        aux_size = .55
#except:
#    width_monitor = 1280
#    height_monitor = 800
#    aux_size = .75
 

width_monitor = 1280
height_monitor = 800
aux_size = .75   

aux_width_monitor = width_monitor/15 
aux_height_monitor = height_monitor/15   
Var_Tamaño_Lbl_X = int(((height_monitor/3)*2)-(aux_width_monitor*1.5))
Var_Tamaño_Lbl_Y = int(((height_monitor/3)*2)-(aux_width_monitor*1.5))

#%%Ventana Bienvenida 
ventanaInicio = tkinter.Tk()
ventanaInicio.geometry(str(width_monitor)+'x'+str(height_monitor-100)+'+0+0')#aux_cortar[0]) 
ventanaInicio.title('Walden Tracking System')
ventanaInicio.config(bg = Fun_Rgb(C_Pal5))

ventanaInicio_Can = Canvas(width=width_monitor, height=height_monitor-110, bg=Fun_Rgb(C_Pal5))
ventanaInicio_Can.create_rectangle(10, 10, width_monitor-10, height_monitor-120, outline=Fun_Rgb(C_Pal3), width=4)
ventanaInicio_Can.place(x=0,y=0)  

Img_ventanaInicio_1 = Fun_Size(Dir_Images + '/' +'interfaz-01.png',1.2*aux_size)
Lbl_ventanaInicio_1 = tkinter.Label(ventanaInicio, bg = Fun_Rgb(C_Pal5), image = Img_ventanaInicio_1)
Lbl_ventanaInicio_1.place(x=aux_width_monitor-10,y=aux_height_monitor+20) 

Img_ventanaInicio_2 = Fun_Size(Dir_Images + '/' +'interfaz-06.1.png',aux_size)
Lbl_ventanaInicio_2 = tkinter.Label(ventanaInicio, bg = Fun_Rgb(C_Pal5), image = Img_ventanaInicio_2)
Lbl_ventanaInicio_2.place(x=aux_width_monitor*6,y=aux_height_monitor)

Img_ventanaInicio_3 = Fun_Size(Dir_Images + '/' +'interfaz-09.png',aux_size)
Lbl_ventanaInicio_3 = tkinter.Label(ventanaInicio, bg = Fun_Rgb(C_Pal5), image = Img_ventanaInicio_3)
Lbl_ventanaInicio_3.place(x=aux_width_monitor+30,y=aux_height_monitor*10-30)

def Fun_Lincense():
    messagebox.showinfo('License A0001.WTS.1.08','A0001.WTS.1.08')

def Fun_WTS():
    messagebox.showinfo('Walden Tracking System 1.08',"Version: 1.08")
  
ventanaInicio_Menu = tkinter.Menu(ventanaInicio)
ventanaInicio.config(menu=ventanaInicio_Menu)

ventanaInicio_Menu_Opc1 = tkinter.Menu(ventanaInicio_Menu, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                             activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Black),
                             tearoff=0)                         
ventanaInicio_Menu.add_cascade(label="Information", menu=ventanaInicio_Menu_Opc1)
ventanaInicio_Menu_Opc1.add_command(label='Walden Tracking System', command=Fun_WTS) 
ventanaInicio_Menu_Opc1.add_command(label='License', command=Fun_Lincense)  

def Fun_AbrirVentanaMenuPrincipal1():
    
    U_X = list(('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'))
    U_Y = 'A0001.WTS.1.01.N9KA-GPXT-WFJC-MPDW'
    U_Z = ''
    
    i = 0
    for i in range(0,len(U_X)):
        try:
            U_T = open(str(U_X[i]) + ':/WaldenKey.txt', 'r')
            U_Z = U_T.read()
        except:
            print('')
            
#    U_Z = 'A0001.WTS.1.01.N9KA-GPXT-WFJC-MPDW'
    if U_Z == U_Y:
        Fun_AbrirVentanaMenuPrincipal2()        
    else:
        messagebox.showinfo("Error Key", "Connect USB Key")
    
def Fun_AbrirVentanaMenuPrincipal2():
    
    ventanaInicio.destroy()      
    
    def Fun_Cortar_Video():
        ventanaMenuPrincipal.destroy()
        
        aux_monitor = 0
        width_monitor = 1280
        height_monitor = 800
        aux_size = .75   
        
        aux_width_monitor = width_monitor/15 
        aux_height_monitor = height_monitor/15   
        Var_Tamaño_Lbl_X = int(((height_monitor/3)*1.48)-(aux_width_monitor*1.4))
        Var_Tamaño_Lbl_Y = int(((height_monitor/3)*1.39)-(aux_width_monitor*1.3))
        
        #############################3
        
        Win_Cortar_Imagen = tkinter.Tk()  
        Win_Cortar_Imagen.config(width=400, height=400)
        Win_Cortar_Imagen.geometry(str(width_monitor)+'x'+str(int(aux_height_monitor*13))+'+0+0') 
        Win_Cortar_Imagen.title('Projects')
        Win_Cortar_Imagen.config(bg = Fun_Rgb(C_Pal5))
        
        Win_Cortar_Imagen_Can = Canvas(width=int(width_monitor), height=int(aux_height_monitor*14), bg=Fun_Rgb(C_Pal5))#(Win_Cortar_Imagen, width=1280, height=800, bg=Fun_Rgb(C_Pal5))
        Win_Cortar_Imagen_Can.create_rectangle(aux_width_monitor*.1, aux_height_monitor*.1, aux_width_monitor*14.9, aux_height_monitor*12.9,
                                               outline=Fun_Rgb(C_Pal3), width=4)
        Win_Cortar_Imagen_Can.create_rectangle(int(aux_width_monitor*1.5), int(aux_height_monitor*1.5), int(aux_width_monitor*4.75), int(aux_width_monitor*4), fill=Fun_Rgb(C_Pal6), outline=Fun_Rgb(C_Pal3), width=2)
        Win_Cortar_Imagen_Can.create_rectangle(int(aux_width_monitor*1.5), int(aux_height_monitor*7.6), int(aux_width_monitor*4.75), int(aux_width_monitor*7.85), fill=Fun_Rgb(C_Pal8), outline=Fun_Rgb(C_Pal7), width=2)
        Win_Cortar_Imagen_Can.place(x=0,y=0)  
              
        def Fun_Ayuda():
            messagebox.showinfo("Help","")
            
        def Fun_Cam_Frontal():
            global Seleccion_Camara
            Seleccion_Camara = 0
            Seleccion_Camara2 = 1
            return(Seleccion_Camara)
        def Fun_Otra_Camara():
            global Seleccion_Camara
            Seleccion_Camara = 1
            Seleccion_Camara2 = 2
            return(Seleccion_Camara)  
            
        def Fun_Res_320x200():
            global Seleccion_Resolucion
            Seleccion_Resolucion = 1
            return(Seleccion_Resolucion)
        def Fun_Res_480x320():
            global Seleccion_Resolucion
            Seleccion_Resolucion = 2
            return(Seleccion_Resolucion)
        def Fun_Res_600x480():
            global Seleccion_Resolucion
            Seleccion_Resolucion = 3
            return(Seleccion_Resolucion)
        def Fun_Res_800x600():
            global Seleccion_Resolucion
            Seleccion_Resolucion = 4
            return(Seleccion_Resolucion)
        def Fun_Res_1280x800():
            global Seleccion_Resolucion
            Seleccion_Resolucion = 5
            return(Seleccion_Resolucion)
            
        def Fun_Open_Video(): 
            Ruta_Video = filedialog.askopenfilename(initialdir = Dir_Videos,
                                                    title = "Select Video",
                                                    filetypes = (("mp4 files","*.mp4"),
                                                    ("all files","*.*")))
        
            cap = cv2.VideoCapture(Ruta_Video)
            Arr_TiempoReal = np.zeros(4)    
            
            while(cap.isOpened()):
                Arr_TiempoReal[0]=time.time() 
                ret, frame = cap.read()
                if ret ==False:
                    break
            
                cv2.imshow('Video',frame)
                cv2.moveWindow('Video', int(aux_width_monitor*1.5), int(aux_height_monitor*1.5))
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                Arr_TiempoReal[1]=time.time()
                time.sleep(.03)
                Arr_TiempoReal[2]=Arr_TiempoReal[1]-Arr_TiempoReal[0] 
                Arr_TiempoReal[3]+= Arr_TiempoReal[2]
                
            cap.release()
            cv2.destroyAllWindows()
            
        def Fun_Take_video():
            global Name_Video, Seleccion_Camara
            Name_Video = filedialog.asksaveasfilename(initialdir = Dir_Videos,
                                                        title = "Video name",
                                                        filetypes = (("all files","*.*"),
                                                        ("jpeg files","*.jpg")))
            
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
            
            Str_SesionT = askstring('Duration', 'Insert the video duration (min)')
            Tiempo_Sesion = int(Str_SesionT)*60
            
            Arr_TiempoReal = np.zeros(4)
            
            fourcc = cv2.VideoWriter_fourcc(*'MP4V')
            out = cv2.VideoWriter(Name_Video + '.mp4',fourcc, 30.0, (640,480))
            
            
            while(Tiempo_Sesion >= Arr_TiempoReal[3]):
                Arr_TiempoReal[0]=time.time() 
                ret, Img_WebCam = Dev_WebCam_Read.read()
                
                if ret==True:
                    out.write(Img_WebCam)
                    
                    cv2.imshow('Video',Img_WebCam)
                    cv2.moveWindow('Video', int(aux_width_monitor*1.5), int(aux_height_monitor*1.5))
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
                
                Arr_TiempoReal[1]=time.time()
                Arr_TiempoReal[2]=Arr_TiempoReal[1]-Arr_TiempoReal[0] 
                Arr_TiempoReal[3]+= Arr_TiempoReal[2]
                    
        
            Dev_WebCam_Read.release()
            out.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Finalized", "Video has been saved")
        
        def Fun_Cut_Video():
            global Dir_Proyecto
            Ruta_Video = filedialog.askopenfilename(initialdir = Dir_Videos,
                                                    title = "Select Video",
                                                    filetypes = (("mp4 files","*.mp4"),
                                                    ("all files","*.*")))
            
            Ruta_Carpeta_Proyecto =  filedialog.asksaveasfilename(initialdir = Dir_Proyecto,
                                                                                title = "Save image project",
                                                                                filetypes = (("all files","*.*"),
                                                                                ("jpeg files","*.jpg")))
            
            Ruta_Carpeta_Proyecto = Ruta_Carpeta_Proyecto
            Carpeta_Imagenes = '/Images/'
            
            if os.path.exists(Ruta_Carpeta_Proyecto):
                os.path.exists(Ruta_Carpeta_Proyecto)
                os.mkdir(Ruta_Carpeta_Proyecto+Carpeta_Imagenes)
            else:
                os.mkdir(Ruta_Carpeta_Proyecto)
                os.mkdir(Ruta_Carpeta_Proyecto+Carpeta_Imagenes)
                
            Captura_Video = cv2.VideoCapture(Ruta_Video)    
            Rate_Video = round(Captura_Video.get(5))
    
            Win_Establecer_Rate = tkinter.Tk()
            Win_Establecer_Rate.config(width=400, height=400)
            Win_Establecer_Rate.geometry('700x230+0+0') 
            Win_Establecer_Rate.title('Video Capture')
            Win_Establecer_Rate.config(bg = Fun_Rgb(C_Pal5))
            
            Win_Establecer_Rate_Can = Canvas(Win_Establecer_Rate, width=700, height=230, bg=Fun_Rgb(C_Pal5))
            Win_Establecer_Rate_Can.create_rectangle(10, 10, 690, 220, outline=Fun_Rgb(C_Pal3), width=2)
            Win_Establecer_Rate_Can.create_rectangle(40, 40, 530, 95, outline=Fun_Rgb(C_Pal3), width=2)
            Win_Establecer_Rate_Can.create_rectangle(40, 130, 530, 200, outline=Fun_Rgb(C_Pal3), width=2)
            Win_Establecer_Rate_Can.place(x=0,y=0) 
    
            Lbl_Win_Establecer_Text_1 = tkinter.Label(Win_Establecer_Rate, bg = Fun_Rgb(C_Pal5), 
                                                      fg = Fun_Rgb(C_Pal2), text = 'Frames per second in the video:  ' + str(Rate_Video))
            Lbl_Win_Establecer_Text_1.config(font = (Font_1,16))
            Lbl_Win_Establecer_Text_1.place(x=60, y = 50)
            
            Lbl_Win_Establecer_Text_2 = tkinter.Label(Win_Establecer_Rate, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Select the number of frames per\n'+' second you want to analyze: ')
            Lbl_Win_Establecer_Text_2.config(font = (Font_1,16))
            Lbl_Win_Establecer_Text_2.place(x=60, y = 140)
    
            def Fun_Cortar():         
                if int(Lbl_Win_Establecer_TextBox_1.get('1.0','end-1c')) > int(Rate_Video):
                    messagebox.showerror("Error", "Frames per second must not exceed original video frames")
                    Win_Establecer_Rate.destroy()
                else:
                    Aux_Ent_Frame = round(Rate_Video/int(Lbl_Win_Establecer_TextBox_1.get('1.0','end-1c')))
                    Aux_Ent_Frame_2 = int(Lbl_Win_Establecer_TextBox_1.get('1.0','end-1c'))
                    Aux_Contador = 1
                    while(Captura_Video.isOpened()):
                        Id_Frame = Captura_Video.get(1)
                        ret, Frame = Captura_Video.read()
                        if (Aux_Contador == Aux_Ent_Frame):
                            Ruta_Frame = Ruta_Carpeta_Proyecto + Carpeta_Imagenes+ "/image_" +  str(int(Id_Frame)) + ".jpg"
                            cv2.imwrite(Ruta_Frame, Frame)
                            Aux_Contador = 1
                            if (ret != True):
                                break
                        else:
                            Aux_Contador += 1
                            if (ret != True):
                                break
                    Captura_Video.release()
                    def sorted_aphanumeric(data):
                            convert = lambda text: int(text) if text.isdigit() else text.lower()
                            alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
                            return sorted(data, key=alphanum_key)
            
                    List_Contenido = sorted_aphanumeric(os.listdir(Ruta_Carpeta_Proyecto+Carpeta_Imagenes))
                    i = len(List_Contenido)-1
                    Ultimo_Archivo_List_Contenido=List_Contenido[i]
                    os.remove(Ruta_Carpeta_Proyecto+Carpeta_Imagenes+Ultimo_Archivo_List_Contenido)
                    Win_Establecer_Rate.destroy()
                    
                    Archivo_Frames = open(Ruta_Carpeta_Proyecto + "/Frames" + '.txt','w')
                    Archivo_Frames.write(str(1/Aux_Ent_Frame) + '_' + str(Aux_Ent_Frame_2))
                    Archivo_Frames.close()
                    messagebox.showinfo("Finalized", "Video has been cut")
                
            Lbl_Win_Establecer_TextBox_1 = tkinter.Text(Win_Establecer_Rate,width = 5, height = 1)
            Lbl_Win_Establecer_TextBox_1.config(font = (Font_1,18))
            Lbl_Win_Establecer_TextBox_1.place(x=450, y = 151.5)    
            Lbl_Win_Establecer_TextBox_1.insert('end',str(round(Rate_Video/30)))  
            
            Btn_Win_Establecer = tkinter.Button(Win_Establecer_Rate,  bd=0, fg = Fun_Rgb(C_Pal5),
                                              bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                              highlightbackground=Fun_Rgb(C_Pal5),
                                              text = 'Accept', command = Fun_Cortar)
            Btn_Win_Establecer.config(font = (Font_1,20))
            Btn_Win_Establecer.place(x=570, y=151.5)
            
            Win_Establecer_Rate.mainloop()
        
            
        def Fun_Get_RGB():
            global Dir_Proyecto
            Main_Dir_Image = filedialog.askopenfilename(initialdir = Dir_Proyecto,
                                                        title = "Select Image",
                                                        filetypes = (("jpg files","*.jpg"),
                                                                      ("all files","*.*"))) 
            Get_Image = mpimg.imread(Main_Dir_Image)
            imgplot = plt.imshow(Get_Image)
    #            imgplot.window.setGeometry(10,10,250, 250)
            plt.show()
            
    
        def Fun_Track_Video():
            
            global Seleccion_Track, Ruta_Imagen, Dialog_Video_File_Aux, Ruta_Proyecto, Ruta_Video, Carpeta_Imagenes, Ruta_Carpeta_Imagenes, Nombre_Archivo, Img_Original_2
            
            Seleccion_Track = 1
            
            Ruta_Imagen = filedialog.askopenfilename(initialdir=Dir_Proyecto,
                                                     title="Select Image",
                                                     filetypes=(("jpg files","*.jpg"),
                                                     ("all files","*.*")))
            
            Dialog_Video_File_Aux = Ruta_Imagen.replace(Ruta_Imagen.split('/')[(np.size(Ruta_Imagen.split('/')))-1], 'Aux_Image.jpg')
            Ruta_Proyecto = Dir_Proyecto
            Len_Ruta_Proyecto = len(Ruta_Proyecto)
            posicionCarpeta = (Ruta_Imagen[Len_Ruta_Proyecto:].find('/'))
            Ruta_Video = Ruta_Imagen[:Len_Ruta_Proyecto+posicionCarpeta]
            Carpeta_Imagenes ='/Images/'
            Ruta_Carpeta_Imagenes = Ruta_Video + Carpeta_Imagenes
            Nombre_Archivo = Ruta_Imagen.split('/')[(np.size(Ruta_Imagen.split('/')))-3]
            
            Img_Original= Image.open(Ruta_Imagen)
            if int(Img_Original.size[0])>=Var_Tamaño_Lbl_X:
                Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))), 
                                Image.ANTIALIAS)
                if int(Img_Original_2.size[1]) >= Var_Tamaño_Lbl_Y:
                    Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y), 
                                Image.ANTIALIAS)
            elif int(Img_Original.size[1])>=Var_Tamaño_Lbl_Y:
                Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y), 
                                                Image.ANTIALIAS)
                if int(Img_Original_2.size[0]) >= Var_Tamaño_Lbl_X:
                    Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))), 
                                                    Image.ANTIALIAS)
            else:
                Img_Original_2 = Img_Original
                    
            global Lbl_Img_Original, Lbl_Img_Original_Aux
            Photo_Img_Original = ImageTk.PhotoImage(Img_Original_2)
            Lbl_Img_Original = tkinter.Label(Win_Cortar_Imagen_Can, image=Photo_Img_Original, bg = Fun_Rgb(C_Pal5), bd = 0)
            Lbl_Img_Original.image = Photo_Img_Original 
            Lbl_Img_Original.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*1.5)+1)
            Lbl_Img_Original_Aux = tkinter.Label()
            
        def Fun_Nuevo_Proyecto_Vivo():
            
            global Seleccion_Track, Dialog_Video_File, Ruta_Proyecto, Ruta_Video, Carpeta_Imagenes, Ruta_Carpeta_Imagenes, Nombre_Archivo, Ruta_Imagen, Ruta_Imagen2
            
            Seleccion_Track = 2
            
            Dialog_Video_File = filedialog.asksaveasfilename(initialdir = Dir_Proyecto,
                                                             title = "Guardar archivo",
                                                             filetypes = (("all files","*.*"), ("jpeg files","*.jpg")))
            Ruta_Proyecto = Dir_Proyecto
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
            Dev_WebCam_Read = cv2.VideoCapture(Seleccion_Camara)
            Dev_WebCam_Read2 = cv2.VideoCapture(Seleccion_Camara2)
            
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
            
            Dev_WebCam_Read2.set(3,Dev_WebCam_Resolution[0])
            Dev_WebCam_Read2.set(4,Dev_WebCam_Resolution[1])
            
            j=0
            while (Dev_WebCam_Read.isOpened()):
                ret, frame = Dev_WebCam_Read.read() 
                Ruta_Imagen = Ruta_Carpeta_Imagenes+'Image_1.jpg'
                cv2.imwrite(Ruta_Imagen, frame)
                
                j+=1
                if j==2:
                    break
            
            j=0
            while (Dev_WebCam_Read2.isOpened()): 
                ret2, frame2 = Dev_WebCam_Read2.read() 
                Ruta_Imagen2 = Ruta_Carpeta_Imagenes+'Image_2.jpg'
                cv2.imwrite(Ruta_Imagen2, frame2)
                j+=1
                if j==2:
                    break
                
            
            Dev_WebCam_Read.release()   
            Dev_WebCam_Read2.release() 
            
            global Dialog_Video_File_Aux, Dialog_Video_File_Aux2
            Dialog_Video_File_Aux = Ruta_Imagen.replace('Image_1', 'Aux_Image')
            Dialog_Video_File_Aux2 = Ruta_Imagen2.replace('Image_2', 'Aux_Image2')
            
            Img_Original= Image.open(Ruta_Imagen)
            if int(Img_Original.size[0])>Var_Tamaño_Lbl_X:
                Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))), 
                                Image.ANTIALIAS)
                if int(Img_Original_2.size[1]) > Var_Tamaño_Lbl_Y:
                    Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y), 
                                Image.ANTIALIAS)
            elif int(Img_Original.size[1])>Var_Tamaño_Lbl_Y:
                Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y), 
                                                Image.ANTIALIAS)
                if int(Img_Original_2.size[0]) > Var_Tamaño_Lbl_X:
                    Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))), 
                                                    Image.ANTIALIAS)
            else:
                Img_Original_2 = Img_Original        
            
            photo = ImageTk.PhotoImage(Img_Original_2)
            global Lbl_Img_Original, Lbl_Img_Original_Aux
            Lbl_Img_Original_Aux = tkinter.Label()
            Lbl_Img_Original = tkinter.Label(image=photo, bg = Fun_Rgb(C_Pal5), bd = 0)
            Lbl_Img_Original.image = photo
            Lbl_Img_Original.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*1.5)+1)
            
            ###
            Img_Original2= Image.open(Ruta_Imagen2)
            if int(Img_Original2.size[0])>Var_Tamaño_Lbl_X:
                Img_Original_22 = Img_Original2.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original2.size[0]))*int(Img_Original2.size[1]))), 
                                Image.ANTIALIAS)
                if int(Img_Original_22.size[1]) > Var_Tamaño_Lbl_Y:
                    Img_Original_22 = Img_Original2.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original2.size[1]))*int(Img_Original2.size[0])),Var_Tamaño_Lbl_Y), 
                                Image.ANTIALIAS)
            elif int(Img_Original2.size[1])>Var_Tamaño_Lbl_Y:
                Img_Original_22 = Img_Original2.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original2.size[1]))*int(Img_Original2.size[0])),Var_Tamaño_Lbl_Y), 
                                                Image.ANTIALIAS)
                if int(Img_Original_22.size[0]) > Var_Tamaño_Lbl_X:
                    Img_Original_22 = Img_Original2.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original2.size[0]))*int(Img_Original2.size[1]))), 
                                                    Image.ANTIALIAS)
            else:
                Img_Original_22 = Img_Original2        
            
            photo = ImageTk.PhotoImage(Img_Original_22)
            global Lbl_Img_Original2, Lbl_Img_Original_Aux2
            Lbl_Img_Original_Aux2 = tkinter.Label()
            Lbl_Img_Original2 = tkinter.Label(image=photo, bg = Fun_Rgb(C_Pal5), bd = 0)
            Lbl_Img_Original2.image = photo
            Lbl_Img_Original2.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*7.55)+1)
            
            def Fun_Borrar_Y_Tomar_Nueva():
                os.remove(Ruta_Carpeta_Imagenes+'Image_1.jpg')
                os.remove(Ruta_Carpeta_Imagenes+'Image_2.jpg')
                
                global Lbl_Img_Original, Lbl_Img_Original_Aux, Lbl_Img_Original2, Lbl_Img_Original_Aux2
                
                Lbl_Img_Original_Aux.place_forget()
                Lbl_Img_Original_Aux2.place_forget()
                
                Dev_WebCam_Resolution = Seleccion_Resolucion
                Dev_WebCam_Read = cv2.VideoCapture(Seleccion_Camara)
                Dev_WebCam_Read2 = cv2.VideoCapture(Seleccion_Camara2)
                
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
                
                Dev_WebCam_Read2.set(3,Dev_WebCam_Resolution[0])
                Dev_WebCam_Read2.set(4,Dev_WebCam_Resolution[1])
                
                j=0
                while (Dev_WebCam_Read.isOpened()):
                    ret, frame = Dev_WebCam_Read.read() 
                    Ruta_Imagen = Ruta_Carpeta_Imagenes+'Image_1.jpg'
                    cv2.imwrite(Ruta_Imagen, frame)
                    
                    j+=1
                    if j==3:
                        break
                Dev_WebCam_Read.release()
                
                j=0
                while (Dev_WebCam_Read2.isOpened()): 
                    ret2, frame2 = Dev_WebCam_Read2.read() 
                    Ruta_Imagen2 = Ruta_Carpeta_Imagenes+'Image_2.jpg'
                    cv2.imwrite(Ruta_Imagen2, frame2)
                    j+=1
                    if j==3:
                        break
                Dev_WebCam_Read2.release() 
                
                global Dialog_Video_File_Aux, Dialog_Video_File_Aux2
                Dialog_Video_File_Aux = Ruta_Imagen.replace('Image_1', 'Aux_Image')
                Dialog_Video_File_Aux2 = Ruta_Imagen2.replace('Image_2', 'Aux_Image2')
                
                Img_Original= Image.open(Ruta_Imagen)
                if int(Img_Original.size[0])>Var_Tamaño_Lbl_X:
                    Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))), 
                                    Image.ANTIALIAS)
                    if int(Img_Original_2.size[1]) > Var_Tamaño_Lbl_Y:
                        Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y), 
                                    Image.ANTIALIAS)
                elif int(Img_Original.size[1])>Var_Tamaño_Lbl_Y:
                    Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y), 
                                                    Image.ANTIALIAS)
                    if int(Img_Original_2.size[0]) > Var_Tamaño_Lbl_X:
                        Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))), 
                                                        Image.ANTIALIAS)
                else:
                    Img_Original_2 = Img_Original        
                
                photo = ImageTk.PhotoImage(Img_Original_2)
                Lbl_Img_Original_Aux = tkinter.Label()
                Lbl_Img_Original = tkinter.Label(image=photo, bg = Fun_Rgb(C_Pal5), bd = 0)
                Lbl_Img_Original.image = photo
                Lbl_Img_Original.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*1.5)+1)
                
                ###
                Img_Original2= Image.open(Ruta_Imagen2)
                if int(Img_Original2.size[0])>Var_Tamaño_Lbl_X:
                    Img_Original_22 = Img_Original2.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original2.size[0]))*int(Img_Original2.size[1]))), 
                                    Image.ANTIALIAS)
                    if int(Img_Original_22.size[1]) > Var_Tamaño_Lbl_Y:
                        Img_Original_22 = Img_Original2.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original2.size[1]))*int(Img_Original2.size[0])),Var_Tamaño_Lbl_Y), 
                                    Image.ANTIALIAS)
                elif int(Img_Original2.size[1])>Var_Tamaño_Lbl_Y:
                    Img_Original_22 = Img_Original2.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original2.size[1]))*int(Img_Original2.size[0])),Var_Tamaño_Lbl_Y), 
                                                    Image.ANTIALIAS)
                    if int(Img_Original_22.size[0]) > Var_Tamaño_Lbl_X:
                        Img_Original_22 = Img_Original2.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original2.size[0]))*int(Img_Original2.size[1]))), 
                                                        Image.ANTIALIAS)
                else:
                    Img_Original_22 = Img_Original2        
                
                photo = ImageTk.PhotoImage(Img_Original_22)
                Lbl_Img_Original_Aux2 = tkinter.Label()
                Lbl_Img_Original2 = tkinter.Label(image=photo, bg = Fun_Rgb(C_Pal5), bd = 0)
                Lbl_Img_Original2.image = photo
                Lbl_Img_Original2.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*7.55)+1)
                
                
                
                mensaje1 =messagebox.askyesno(message= 'Take another picture?', title="Picture")
                if mensaje1==True:
                    Lbl_Img_Original_Aux.place_forget()
                    Lbl_Img_Original.place_forget()
                    Lbl_Img_Original_Aux2.place_forget()
                    Lbl_Img_Original2.place_forget()
                    Fun_Borrar_Y_Tomar_Nueva()
             
            mensaje1 =messagebox.askyesno(message="Take another picture?", title="Picture")
            if mensaje1==True:
                Lbl_Img_Original_Aux.place_forget()
                Lbl_Img_Original.place_forget()
                Lbl_Img_Original_Aux2.place_forget()
                Lbl_Img_Original2.place_forget()
                Fun_Borrar_Y_Tomar_Nueva()
                
        def Fun_Abrir_Proyecto_Vivo():
            global Seleccion_Track
            Seleccion_Track = 3
            Fun_Iniciar_Track()
          
        Menu_Informacion = tkinter.Menu(Win_Cortar_Imagen)
        
        Submenu_Archivo = tkinter.Menu(Menu_Informacion, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                                       activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Black),
                                       tearoff=0)
    #    Submenu_Archivo.add_command(label='Open video', command = Fun_Open_Video)
    #    Submenu_Archivo.add_command(label='Record video', command = Fun_Take_video)
    #    Submenu_Archivo.add_command(label='Video to Frames', command = Fun_Cut_Video)
    #    Submenu_Archivo.add_command(label='Video project', command = Fun_Track_Video)
        Submenu_Archivo.add_command(label='Live set up', command = Fun_Nuevo_Proyecto_Vivo)
        Submenu_Archivo.add_command(label='Live project', command = Fun_Abrir_Proyecto_Vivo)
        Submenu_Archivo.add_command(label='RGB', command = Fun_Get_RGB)
        Menu_Informacion.add_cascade(label='File', menu=Submenu_Archivo)
         
        Submenu_Configuracion = tkinter.Menu(Menu_Informacion, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                                             activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Black),
                                             tearoff=0)
        
        Submenu_Camara = tkinter.Menu(Submenu_Configuracion, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                                      activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Black),
                                      tearoff=0)
        Submenu_Camara.add_command(label="WebCam 1", command = Fun_Cam_Frontal)
        Submenu_Camara.add_command(label="WebCam 2", command = Fun_Otra_Camara)
        Submenu_Configuracion.add_cascade(label='Select', menu=Submenu_Camara)
        
        Submenu_Resolucion = tkinter.Menu(Submenu_Configuracion, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                                          activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Black),
                                          tearoff=0)
        Submenu_Resolucion.add_command(label="320x200", command = Fun_Res_320x200)
        Submenu_Resolucion.add_command(label="480x320", command = Fun_Res_480x320)
        Submenu_Resolucion.add_command(label="600x480", command = Fun_Res_600x480)
        Submenu_Resolucion.add_command(label="800x600", command = Fun_Res_800x600)
        Submenu_Resolucion.add_command(label="1280x800", command = Fun_Res_1280x800)
        Submenu_Configuracion.add_cascade(label='Resolution', menu=Submenu_Resolucion)
        
        Menu_Informacion.add_cascade(label="WebCam", menu=Submenu_Configuracion)
         
        #Menu_Informacion.add_command(label="Help", command=Fun_Ayuda)
        
        Win_Cortar_Imagen.config(menu=Menu_Informacion)
    
        def Fun_Imagen():
            
            if Seleccion_Track == 0:
                messagebox.showinfo("Error", "Select a traking option")
    
            X1 = Slider_X1.get()
            X2 = Slider_X2.get()
            Y1 = Slider_Y1.get()
            Y2 = Slider_Y2.get()
            Rotar = Slider_Grados_Rotar.get()
            
            global Lbl_Img_Original, Lbl_Img_Original_Aux, Dialog_Video_File_Aux_2
            Lbl_Img_Original.place_forget()
            Lbl_Img_Original_Aux.place_forget()
            
            Img_Original = imageio.imread(Ruta_Imagen)
            Img_Original = Img_Original[round(Img_Original.shape[0]*Y1):round(Img_Original.shape[0]*Y2),
                                        round(Img_Original.shape[1]*X1):round(Img_Original.shape[1]*X2)]
        
            imageio.imsave(Dialog_Video_File_Aux, Img_Original)
            Img_Aux = Image.open(Dialog_Video_File_Aux).rotate(Rotar)
            
            Img_Original_2 = Img_Aux
            if int(Img_Aux.size[0])>Var_Tamaño_Lbl_X:
                Img_Original_2 = Img_Aux.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Aux.size[0]))*int(Img_Aux.size[1]))), 
                                Image.ANTIALIAS)
                if int(Img_Original_2.size[1]) > Var_Tamaño_Lbl_Y:
                    Img_Original_2 = Img_Aux.resize((round((Var_Tamaño_Lbl_Y/int(Img_Aux.size[1]))*int(Img_Aux.size[0])),Var_Tamaño_Lbl_Y), 
                                Image.ANTIALIAS)
            elif int(Img_Aux.size[1])>Var_Tamaño_Lbl_Y:
                Img_Original_2 = Img_Aux.resize((round((Var_Tamaño_Lbl_Y/int(Img_Aux.size[1]))*int(Img_Aux.size[0])),Var_Tamaño_Lbl_Y), 
                                                Image.ANTIALIAS)
                if int(Img_Original_2.size[0]) > Var_Tamaño_Lbl_X:
                    Img_Original_2 = Img_Aux.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Aux.size[0]))*int(Img_Aux.size[1]))), 
                                                    Image.ANTIALIAS)
                    
            Img_Aux.save(Dialog_Video_File_Aux)
            
            Photo_Img_Aux = ImageTk.PhotoImage(Img_Original_2)
            Lbl_Img_Original_Aux = tkinter.Label(image=Photo_Img_Aux, bg = Fun_Rgb(C_Pal5), bd = 0)
            Lbl_Img_Original_Aux.image = Photo_Img_Aux 
            Lbl_Img_Original_Aux.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*1.5)+1)
            
        def Fun_Imagen2():
            
            if Seleccion_Track == 0:
                messagebox.showinfo("Error", "Select a traking option")
    
            X1 = Slider2_X1.get()
            X2 = Slider2_X2.get()
            Y1 = Slider2_Y1.get()
            Y2 = Slider2_Y2.get()
            Rotar2 = Slider2_Grados_Rotar.get()
            
            global Lbl_Img_Original2, Lbl_Img_Original_Aux2, Dialog_Video_File_Aux_22
            Lbl_Img_Original2.place_forget()
            Lbl_Img_Original_Aux2.place_forget()
            
            Img_Original2 = imageio.imread(Ruta_Imagen2)
            Img_Original2 = Img_Original2[round(Img_Original2.shape[0]*Y1):round(Img_Original2.shape[0]*Y2),
                                        round(Img_Original2.shape[1]*X1):round(Img_Original2.shape[1]*X2)]
        
            imageio.imsave(Dialog_Video_File_Aux2, Img_Original2)
            Img_Aux2 = Image.open(Dialog_Video_File_Aux2).rotate(Rotar2)
            
            Img_Original_22 = Img_Aux2
            if int(Img_Aux2.size[0])>Var_Tamaño_Lbl_X:
                Img_Original_22 = Img_Aux2.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Aux2.size[0]))*int(Img_Aux2.size[1]))), 
                                Image.ANTIALIAS)
                if int(Img_Original_22.size[1]) > Var_Tamaño_Lbl_Y:
                    Img_Original_22 = Img_Aux2.resize((round((Var_Tamaño_Lbl_Y/int(Img_Aux2.size[1]))*int(Img_Aux2.size[0])),Var_Tamaño_Lbl_Y), 
                                Image.ANTIALIAS)
            elif int(Img_Aux2.size[1])>Var_Tamaño_Lbl_Y:
                Img_Original_22 = Img_Aux2.resize((round((Var_Tamaño_Lbl_Y/int(Img_Aux2.size[1]))*int(Img_Aux2.size[0])),Var_Tamaño_Lbl_Y), 
                                                Image.ANTIALIAS)
                if int(Img_Original_22.size[0]) > Var_Tamaño_Lbl_X:
                    Img_Original_22 = Img_Aux2.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Aux2.size[0]))*int(Img_Aux2.size[1]))), 
                                                    Image.ANTIALIAS)
                    
            Img_Aux2.save(Dialog_Video_File_Aux2)
            
            Photo_Img_Aux2 = ImageTk.PhotoImage(Img_Original_22)
            Lbl_Img_Original_Aux2 = tkinter.Label(image=Photo_Img_Aux2, bg = Fun_Rgb(C_Pal5), bd = 0)
            Lbl_Img_Original_Aux2.image = Photo_Img_Aux2 
            Lbl_Img_Original_Aux2.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*7.55)+1)
        
        def Fun_Editar_Imagen():
            
            if Seleccion_Track == 0:
                messagebox.showinfo("Error", "Select a traking option")
            
            Var_R = Slider_Rojo.get()
            Var_G = Slider_Verde.get()
            Var_B = Slider_Azul.get()
            Var_Des = Slider_Desviacion.get()
            Var_Umbral = float(Entr_Umbral.get())
            Mat_RGB = ([Var_R, Var_G, Var_B, Var_Des, Var_Umbral])
            Img_Filtro = Var_Filtro.get()
            Track_MinSize = float(Entr_Valor_Minimo_Animal.get())
            
            global Lbl_Img_Original, Lbl_Img_Original_Aux, Lbl_Img_Original2, Lbl_Img_Original_Aux2
            Lbl_Img_Original.place_forget()
            Lbl_Img_Original_Aux.place_forget()
            
            Lbl_Img_Original2.place_forget()
            Lbl_Img_Original_Aux2.place_forget()
            
            global Dialog_Video_File_Aux_2, Dialog_Video_File_Aux_22
            Dialog_Video_File_Aux_2 = Dialog_Video_File_Aux.replace('Aux_Image', 'Aux_Imagee')
            Dialog_Video_File_Aux_22 = Dialog_Video_File_Aux2.replace('Aux_Image2', 'Aux_Imagee2')
            
            Img_Cortable = imageio.imread(Dialog_Video_File_Aux)
            Img_Cortable_Aux = Img_Cortable[:, :]
            imageio.imsave(Dialog_Video_File_Aux_2, Img_Cortable_Aux)
            Img_WebCam = np.copy(Img_Cortable_Aux)
            
            Img_Cortable2 = imageio.imread(Dialog_Video_File_Aux2)
            Img_Cortable_Aux2 = Img_Cortable2[:, :]
            imageio.imsave(Dialog_Video_File_Aux_22, Img_Cortable_Aux2)
            Img_WebCam2 = np.copy(Img_Cortable_Aux2)
            
            Mat_WebCam_RGB = np.zeros((Img_WebCam.shape))
            Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,0]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[0]+Mat_RGB[3])))[0]),
                           (np.where((Img_WebCam[:,:,0]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[0]+Mat_RGB[3])))[1]),0] = 1
            Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[0]),
                           (np.where((Img_WebCam[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[1]),1] = 1
            Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,2]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[2]+Mat_RGB[3])))[0]),
                           (np.where((Img_WebCam[:,:,2]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[2]+Mat_RGB[3])))[1]),2] = 1          
            Img_WebCam = Mat_WebCam_RGB   
                    
            Mat_WebCam_RGB2 = np.zeros((Img_WebCam2.shape))
            Mat_WebCam_RGB2[(np.where((Img_WebCam2[:,:,0]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam2[:,:,0]<=(Mat_RGB[0]+Mat_RGB[3])))[0]),
                           (np.where((Img_WebCam2[:,:,0]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam2[:,:,0]<=(Mat_RGB[0]+Mat_RGB[3])))[1]),0] = 1
            Mat_WebCam_RGB2[(np.where((Img_WebCam2[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam2[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[0]),
                           (np.where((Img_WebCam2[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam2[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[1]),1] = 1
            Mat_WebCam_RGB2[(np.where((Img_WebCam2[:,:,2]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam2[:,:,2]<=(Mat_RGB[2]+Mat_RGB[3])))[0]),
                           (np.where((Img_WebCam2[:,:,2]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam2[:,:,2]<=(Mat_RGB[2]+Mat_RGB[3])))[1]),2] = 1          
            Img_WebCam2 = Mat_WebCam_RGB2  
            
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
            
            if Img_Filtro==1:
                Img_WebCam2 = ndimage.gaussian_filter(Img_WebCam2, sigma=3)
            elif Img_Filtro==2:
                Img_WebCam2 = ndimage.gaussian_filter(Img_WebCam2, sigma=5)
            elif Img_Filtro==3:
                Img_WebCam2 =ndimage.uniform_filter(Img_WebCam2, size=2)
            elif Img_Filtro==4:
                Img_WebCam2 =ndimage.uniform_filter(Img_WebCam2, size=11)
            elif Img_Filtro==5:
                Img_WebCam2 = Img_WebCam2
            np.place(Img_WebCam2[:,:,:], Img_WebCam2[:,:,:]>=Mat_RGB[4], 1)
            np.place(Img_WebCam2[:,:,:], Img_WebCam2[:,:,:]<Mat_RGB[4], 0)
    
            imageio.imsave(Dialog_Video_File_Aux_2, Img_WebCam)
            Img_Cortable_Aux = Image.open(Dialog_Video_File_Aux_2)
            
            imageio.imsave(Dialog_Video_File_Aux_22, Img_WebCam2)
            Img_Cortable_Aux2 = Image.open(Dialog_Video_File_Aux_22)
            
            Img_Original_2 = Image.open(Dialog_Video_File_Aux_2)
            if int(Img_Cortable_Aux.size[0])>Var_Tamaño_Lbl_X:
                Img_Original_2 = Img_Cortable_Aux.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Cortable_Aux.size[0]))*int(Img_Cortable_Aux.size[1]))), 
                                Image.ANTIALIAS)
                if int(Img_Original_2.size[1]) > Var_Tamaño_Lbl_Y:
                    Img_Original_2 = Img_Cortable_Aux.resize((round((Var_Tamaño_Lbl_Y/int(Img_Cortable_Aux.size[1]))*int(Img_Cortable_Aux.size[0])),Var_Tamaño_Lbl_Y), 
                                Image.ANTIALIAS)
            elif int(Img_Cortable_Aux.size[1])>Var_Tamaño_Lbl_Y:
                Img_Original_2 = Img_Cortable_Aux.resize((round((Var_Tamaño_Lbl_Y/int(Img_Cortable_Aux.size[1]))*int(Img_Cortable_Aux.size[0])),Var_Tamaño_Lbl_Y), 
                                                Image.ANTIALIAS)
                if int(Img_Original_2.size[0]) > Var_Tamaño_Lbl_X:
                    Img_Original_2 = Img_Cortable_Aux.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Cortable_Aux.size[0]))*int(Img_Cortable_Aux.size[1]))), 
                                                    Image.ANTIALIAS)
                    
            Img_Original_22 = Image.open(Dialog_Video_File_Aux_22)
            if int(Img_Cortable_Aux2.size[0])>Var_Tamaño_Lbl_X:
                Img_Original_22 = Img_Cortable_Aux2.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Cortable_Aux2.size[0]))*int(Img_Cortable_Aux2.size[1]))), 
                                Image.ANTIALIAS)
                if int(Img_Original_22.size[1]) > Var_Tamaño_Lbl_Y:
                    Img_Original_22 = Img_Cortable_Aux2.resize((round((Var_Tamaño_Lbl_Y/int(Img_Cortable_Aux2.size[1]))*int(Img_Cortable_Aux2.size[0])),Var_Tamaño_Lbl_Y), 
                                Image.ANTIALIAS)
            elif int(Img_Cortable_Aux2.size[1])>Var_Tamaño_Lbl_Y:
                Img_Original_22 = Img_Cortable_Aux2.resize((round((Var_Tamaño_Lbl_Y/int(Img_Cortable_Aux2.size[1]))*int(Img_Cortable_Aux2.size[0])),Var_Tamaño_Lbl_Y), 
                                                Image.ANTIALIAS)
                if int(Img_Original_22.size[0]) > Var_Tamaño_Lbl_X:
                    Img_Original_22 = Img_Cortable_Aux2.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Cortable_Aux2.size[0]))*int(Img_Cortable_Aux2.size[1]))), 
                                                    Image.ANTIALIAS)
            
            #Guardar_Axuliar_2
            Img_Cortable_Aux.save(Dialog_Video_File_Aux_2)   
            Img_Cortable_Aux2.save(Dialog_Video_File_Aux_22)   
            
            #Mostrar Imagen
            Pho_Img_Cortable_Aux = ImageTk.PhotoImage(Img_Original_2)
            Lbl_Parametros_Aux = tkinter.Label(image=Pho_Img_Cortable_Aux, bg = Fun_Rgb(C_Pal5), bd = 0)
            Lbl_Parametros_Aux.image = Pho_Img_Cortable_Aux 
            Lbl_Parametros_Aux.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*1.5)+1)
            
            
            Pho_Img_Cortable_Aux2 = ImageTk.PhotoImage(Img_Original_22)
            Lbl_Parametros_Aux2 = tkinter.Label(image=Pho_Img_Cortable_Aux2, bg = Fun_Rgb(C_Pal5), bd = 0)
            Lbl_Parametros_Aux2.image = Pho_Img_Cortable_Aux2 
            Lbl_Parametros_Aux2.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*7.55)+1)
       
        #%% Fun_Editar_Todas_Imagenes
        def Fun_Editar_Todas_Imagenes():
            
            if Seleccion_Track == 0:
                messagebox.showinfo("Error", "Select a traking option")
            
            global Mat_RGB, number_subject
            
            plt.rcParams['image.cmap'] = 'gray'
            X1 = Slider_X1.get()
            X2 = Slider_X2.get()
            Y1 = Slider_Y1.get()
            Y2 = Slider_Y2.get()
            Rotar = Slider_Grados_Rotar.get()
            Dev_Espacio_Tamano = Etr_Tamano_Caja.get()
            Img_Filtro = Var_Filtro.get()
            Track_MinSize = float(Entr_Valor_Minimo_Animal.get())
            os.remove(Dialog_Video_File_Aux)
            os.remove(Dialog_Video_File_Aux_2)
            
            X12 = Slider2_X1.get()
            X22 = Slider2_X2.get()
            Y12 = Slider2_Y1.get()
            Y22 = Slider2_Y2.get()
            Rotar2 = Slider2_Grados_Rotar.get()
            Dev_Espacio_Tamano2 = Etr2_Tamano_Caja.get()
            Img_Filtro = Var_Filtro.get()
            Track_MinSize = float(Entr_Valor_Minimo_Animal.get())
            os.remove(Dialog_Video_File_Aux2)
            os.remove(Dialog_Video_File_Aux_22)
            
            if number_subject == 0:
                Var_R = Slider_Rojo.get()
                Var_G = Slider_Verde.get()
                Var_B = Slider_Azul.get()
                Var_Des = Slider_Desviacion.get()
                Var_Umbral = float(Entr_Umbral.get())
                Mat_RGB = ([Var_R, Var_G, Var_B, Var_Des, Var_Umbral])
            
            #Imagenes
            def sorted_aphanumeric(data):
                convert = lambda text: int(text) if text.isdigit() else text.lower()
                alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
                return sorted(data, key=alphanum_key)
            List_Contenido = sorted_aphanumeric(os.listdir(Ruta_Carpeta_Imagenes))
           
            if number_subject == 0:
                #Remplazar Imagenes
                for elemento in List_Contenido:
                    ruta = Ruta_Carpeta_Imagenes
                    documento = ruta + elemento
                    
                    Img_Original = imageio.imread(documento)/255.0
                    Img_Original = Img_Original[round(Img_Original.shape[0]*Y1):round(Img_Original.shape[0]*Y2),
                                    round(Img_Original.shape[1]*X1):round(Img_Original.shape[1]*X2)]
                    imageio.imsave(documento, Img_Original)
                    Img_Original = Image.open(documento).rotate(Rotar)
            
                    Img_WebCam = np.copy(Img_Original)
                    imageio.imsave(documento, Img_WebCam)
                
                    Img_Original2 = imageio.imread(documento)/255.0
                    Img_Original2 = Img_Original2[round(Img_Original2.shape[0]*Y1):round(Img_Original2.shape[0]*Y2),
                                    round(Img_Original2.shape[1]*X1):round(Img_Original2.shape[1]*X2)]
                    imageio.imsave(documento, Img_Original2)
                    Img_Original2 = Image.open(documento).rotate(Rotar2)
            
                    Img_WebCam2 = np.copy(Img_Original2)
                    imageio.imsave(documento, Img_WebCam2)
                    
                if Seleccion_Track == 1:
                    messagebox.showinfo("Finalized", "Images have been edited")
                elif Seleccion_Track == 2:
                    messagebox.showinfo("Finalized", "Parameters have been saved")
                elif Seleccion_Track == 3:
                    messagebox.showinfo("Finalized", "Open Parameters")
                
                #Guardar txt
                Arr_Variables = [str(Seleccion_Camara), str(Seleccion_Resolucion),
                                 str(X1), str(X2), str(Y1), str(Y2), str(Rotar), 
                                 str(Dev_Espacio_Tamano), str(Var_R), str(Var_G), str(Var_B),
                                 str(Var_Des), str(Var_Umbral), str(Img_Filtro), 
                                 str(Track_MinSize), 
                                 str(Img_WebCam.shape[1]),str(Img_WebCam.shape[0]), str(number_subject),     
                                 str(Seleccion_Camara), str(Seleccion_Resolucion),
                                 str(X12), str(X22), str(Y12), str(Y22), str(Rotar2), 
                                 str(Dev_Espacio_Tamano2), str(Var_R), str(Var_G), str(Var_B),
                                 str(Var_Des), str(Var_Umbral), str(Img_Filtro), 
                                 str(Track_MinSize), 
                                 str(Img_WebCam2.shape[1]),str(Img_WebCam2.shape[0]), str(number_subject)] 
                
                Archivo_Variables = open(Ruta_Video + '/' + 'Config3D_' + Nombre_Archivo +'.txt','w')
                for i in Arr_Variables:
                    Archivo_Variables.write(i +'\n')
                Archivo_Variables.close()
                
    
           
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
                    ruta = Ruta_Carpeta_Imagenes
                    documento = ruta + elemento
                    
                    Img_Original = imageio.imread(documento)/255.0
                    Img_Original = Img_Original[round(Img_Original.shape[0]*Y1):round(Img_Original.shape[0]*Y2),
                                    round(Img_Original.shape[1]*X1):round(Img_Original.shape[1]*X2)]
                    imageio.imsave(documento, Img_Original)
                    Img_Original = Image.open(documento).rotate(Rotar)
            
                    Img_WebCam = np.copy(Img_Original)
                    imageio.imsave(documento, Img_WebCam)
                
                if Seleccion_Track == 1:
                    messagebox.showinfo("Finalized", "Images have been edited")
                elif Seleccion_Track == 2:
                    messagebox.showinfo("Finalized", "Parameters have been saved")
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
                
                Archivo_Variables = open(Ruta_Video + '/' + 'Config_' + Nombre_Archivo +'.txt','w')
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
        
        #%% Iniciar Track
        def Fun_Iniciar_Track():
            if Seleccion_Track == 0:
                messagebox.showinfo("Error", "Select a traking option")
            
            #%%Track Imagenes --- 1
            if Seleccion_Track == 1:
                
                #Seleccionar Archivo
                Direccion_Documento = filedialog.askopenfilename(initialdir = Dir_Proyecto,
                                                                       title = "Seleccionar archivo",
                                                                       filetypes = (("txt files","*.txt"),
                                                                                    ("all files","*.*")))
                
                def Ventana_Sesion():
                    Win_Cortar_Imagen.destroy()
                    #Variables
                    global Str_SesionT, Str_Sujeto, Str_Sesion, Str_Grupo
                    Str_SesionT = '0'
                    Str_Sujeto = '0'
                    Str_Sesion = '0'
                    Str_Grupo = '0'
                    
                    Main_Ses = tkinter.Tk()
                    Main_Ses.title('Run experiment')
                    Main_Ses.geometry(str(int(aux_width_monitor*8))+'x'+str(height_monitor-100)+'+0+0')
                    Main_Ses.configure(background=Fun_Rgb(C_Pal5))
                    
                    Main_Ses_Can = Canvas(Main_Ses, width=round(aux_width_monitor*8), height=round(height_monitor-100), bg=Fun_Rgb(C_Pal5))
                    Main_Ses_Can.create_rectangle(10, 10, aux_width_monitor*8 -10, height_monitor-110, outline=Fun_Rgb(C_Pal3), width=4)
                    Main_Ses_Can.create_rectangle(120, 250, 520, 650, fill=Fun_Rgb(C_Black), outline=Fun_Rgb(C_Pal6), width=2)
                    Main_Ses_Can.place(x=0,y=0) 
              
                    def Fun_Bnt_Next():
                        
                        global Str_SesionT, Str_Sujeto, Str_Sesion, Str_Grupo, Nombre_Archivo,  Ruta_Video, Ruta_Carpeta_Imagenes, Ruta_Carpeta_Imagenes, Ruta_Archivo_Parametros
                        
                        Str_Sujeto = Lbl_Sujeto_TextBox_1.get('1.0','end-1c')
                        Str_Sesion = Lbl_Sesion_TextBox_1.get('1.0','end-1c')
                        Str_Grupo = Lbl_Grupo_TextBox_1.get('1.0','end-1c')
                        
                        Ruta_Archivo_Parametros = Ruta_Video + '/Config_' + Nombre_Archivo+'.txt'
                        Ruta_Archivo_Frames = Ruta_Video + '/Frames.txt'
                        
                        def sorted_aphanumeric(data):
                                    convert = lambda text: int(text) if text.isdigit() else text.lower()
                                    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
                                    return sorted(data, key=alphanum_key)
                        List_Contenido = sorted_aphanumeric(os.listdir(Ruta_Carpeta_Imagenes))
                        
                        Dir_Archivo_Parametros =open(Ruta_Archivo_Parametros,'r')  
                        Arr_Parametros_Imagen = Dir_Archivo_Parametros.read().split('\n')    
                        Track_MinSize = float(Arr_Parametros_Imagen[14]) 
                        Dev_Espacio_Tamano = int(Arr_Parametros_Imagen[7])
                        number_subject = int(Arr_Parametros_Imagen[17])
                        Size_Proportion = int(Arr_Parametros_Imagen[15])
                        Dir_Archivo_Parametros.close()
                        
                        Dir_Archivo_Frames = open(Ruta_Archivo_Frames, 'r')
                        Temp_Int_Frame = Dir_Archivo_Frames.read().split('\n')
                        Temp_Int_Frame = str(Temp_Int_Frame)[2:-2]
                        Int_Frame, Int_Frame_2 = Temp_Int_Frame.split('_')
                        Dir_Archivo_Frames.close()
                                
                        global Mat_Datos
                        Int_Contador = 1
                        Int_Datos_Consecuencia = 0
                        Mat_Datos = np.zeros((9999999,6+(number_subject*2)))
                        
                        
                        if number_subject > 0: 
                            global Mat_Datos_X, Mat_Datos_Y, Mat_Datos_D, Mat_RGB 
                            Mat_Datos_X = np.zeros((9999999,16))
                            Mat_Datos_Y = np.zeros((9999999,16))
                            Mat_Datos_D = np.zeros((9999999,16))
                    
                            Mat_RGB = np.zeros((number_subject, 6))
                            aux_1 = 0
                            f = 0
                            for i in Arr_Parametros_Imagen:
                                b = i
                                aux_1 += 1
                                if aux_1 == 9:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][0] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 10:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][1] = e
                                        f += 1
                                    f = 0   
                                if aux_1 == 11:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][2] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 12:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][3] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 13:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][4] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 14:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][5] = e
                                        f += 1
                                    f = 0
                            
                        else:
                            Mat_RGB = ([int(Arr_Parametros_Imagen[8]), int(Arr_Parametros_Imagen[9]), int(Arr_Parametros_Imagen[10]),
                                        int(Arr_Parametros_Imagen[11]), float(Arr_Parametros_Imagen[12])])
                            Img_Filtro = int(Arr_Parametros_Imagen[13]) 
                        
                        def Fun_Distancia(x1,x2,y1,y2,DistanciaRelativa):
                            return math.sqrt((x2-x1)**2+(y2-y1)**2)*DistanciaRelativa
                        
                        if number_subject == 0:
    
                            for elemento in List_Contenido:
                                
                                ruta = Ruta_Carpeta_Imagenes
                                documento = ruta + elemento
                                Img_Original = imageio.imread(documento)/255.0
                                Img_Original = Image.open(documento)
                                Img_WebCam = np.copy(Img_Original)
                                
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
                        
                                try:
                                    Mat_Centroide = ndimage.label(Img_WebCam)[0]
                                    Centroide = scipy.ndimage.measurements.center_of_mass(Img_WebCam, Mat_Centroide, [1])
                                    Mat_Size = ndimage.label(Img_WebCam)[0]
                                    Size = np.sqrt(scipy.ndimage.measurements.sum(Img_WebCam, Mat_Size, [1]))
                                    MinSize = int(np.where(Size == np.min(Size[(Size >= Track_MinSize)]))[0])
                                    cv2.circle(Img_WebCam,(int(Centroide[MinSize][1]),int(Centroide[MinSize][0])),2,(0,0,255),5)
                                except:
                                    Img_WebCam = Img_WebCam
                                    
                                Img_WebCam = cv2.resize(Img_WebCam,(400, round((400/Img_WebCam.shape[1])*Img_WebCam.shape[1])))
                                cv2.putText(Img_WebCam,'T: ',(5,15),Font_CV, .5,(255,255,255),1)
                                cv2.putText(Img_WebCam,str(round(Mat_Datos[Int_Contador-1][0] ,2)),(20,15),Font_CV, .5,(255,255,255),1)
                                cv2.imshow('Tracking',Img_WebCam)
                                cv2.moveWindow('Tracking', 120,250);
                                cv2.waitKey(5)
                                
                                Mat_Datos[Int_Contador][0] = (int(elemento.replace('image_','').replace('.jpg',''))/int(Int_Frame_2)) * float(Int_Frame)  
                                try:
                                    Mat_Datos[Int_Contador][1] = int(Centroide[MinSize][1])
                                    Mat_Datos[Int_Contador][2] = int(Centroide[MinSize][0])
                                except:
                                    Mat_Datos[Int_Contador][1] = Mat_Datos[Int_Contador-1][1]
                                    Mat_Datos[Int_Contador][2] = Mat_Datos[Int_Contador-1][2]
                                Mat_Datos[Int_Contador][4] = Int_Datos_Consecuencia
                                Mat_Datos[Int_Contador][3] = (Fun_Distancia(Mat_Datos[Int_Contador-1][1],Mat_Datos[Int_Contador][1],Mat_Datos[Int_Contador-1][2],Mat_Datos[Int_Contador][2],Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])))
                                Mat_Datos[Int_Contador][5] = (Mat_Datos[Int_Contador][3]/100) / float(Int_Frame)
                                Int_Contador += 1 
                                
                            cv2.destroyAllWindows()
                            
                            Mat_Datos = np.delete(Mat_Datos,np.where(Mat_Datos[:,1] == 0), axis=0) 
                            Mat_Datos[0,3] = 0
                            Mat_Datos[0,5] = 0
                                                              
                            Nombre_Grafico =  filedialog.asksaveasfilename(initialdir = Dir_Datos,
                                                                                         title = "Save Data",
                                                                                         filetypes = (("all files","*.*"), ("txt files","*.txt"))) 
                            i = 1
                            Archivo_Mat_Datos = open(Nombre_Grafico + '.txt','w')
                            Archivo_Mat_Datos.write('Subject: ' + Str_Sujeto + '\n' +
                                                    'Session: ' + Str_Sesion + '\n' +
                                                    'Group: ' + Str_Grupo + '\n' +
                                                    'Time: '+ str(round(max(Mat_Datos[:,0]),3)) + '\n' +
                                                    '# Consecuences: ' + str(np.size(np.where(Mat_Datos[:,4] == 1))) + '\n' +
                                                    'Distance: ' + str(round(sum(Mat_Datos[:,3]),3)) + 'cm' + '\n' +
                                                    'Velocity: ' + str(round(sum(Mat_Datos[:,3])/max(Mat_Datos[:,0]),3)) + 'cm/seg' + '\n' +
                                                    'Mean Aceleration: ' + str(round(statistics.mean(Mat_Datos[:,5]),3)) + 'm/seg' + '\n' +
                                                    '\n' + 'Frame;Time;X;Y;Aceleration;Distance;Consecuences' + '\n')
                            for i in range(0,len(Mat_Datos)): 
                                Archivo_Mat_Datos.write(str(i) + ',' + str(round(Mat_Datos[i][0],3)) +
                                                                 ',' + str(round(Mat_Datos[i][1] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])),3)) +
                                                                 ',' + str(round(Mat_Datos[i][2] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[16])),3)) +
                                                                 ',' + str(round(Mat_Datos[i][5],3)) +
                                                                 ',' + str(round(Mat_Datos[i][3],3)) +
                                                                 ',' + str(Mat_Datos[i][4]) + '\n')
                            Archivo_Mat_Datos.close() 
                            if Seleccion_Track == 1:
                                messagebox.showinfo("Finalized", "Video has been traked")
                            Main_Ses.destroy()
                            
                            
                        else:
                            for elemento in List_Contenido:
                                ruta = Ruta_Carpeta_Imagenes
                                documento = ruta + elemento
                                
                                Img_Original = imageio.imread(documento)/255
                                Img_Original = Image.open(documento)
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
                        
                                    if Mat_RGB[i][5]==1:
                                        image_aux = ndimage.gaussian_filter(image_aux, sigma=3)
                                    elif Mat_RGB[i][5]==2:
                                        image_aux = ndimage.gaussian_filter(image_aux, sigma=5)
                                    elif Mat_RGB[i][5]==3:
                                        image_aux =ndimage.uniform_filter(image_aux, size=2)
                                    elif Mat_RGB[i][5]==4:
                                        image_aux =ndimage.uniform_filter(image_aux, size=11)
                                    elif Mat_RGB[i][5]==5:
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
                                    Mat_Datos_D[Int_Contador][i] = (Fun_Distancia(Mat_Datos_X[Int_Contador-1][i],Mat_Datos_X[Int_Contador][i],Mat_Datos_Y[Int_Contador-1][i],Mat_Datos_Y[Int_Contador][i],Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])))    
                                                                        
                                    image_total += image_aux
                                    if i == number_subject -1:
                                        j = 0
                                        for j in range(number_subject):
                                            cv2.putText(image_total,str(j+1),(int(Mat_Datos_X[Int_Contador][j])+10,int(Mat_Datos_Y[Int_Contador][j])),Font_CV, .5,(0,0,255),1)
                                        image_total = cv2.resize(image_total,(400, round((400/Img_WebCam.shape[1])*Img_WebCam.shape[1])))
                                        cv2.putText(image_total,'T: ',(5,15),Font_CV, .5,(255,255,255),1)
                                        cv2.putText(image_total,str(round(Mat_Datos[Int_Contador-1][0] ,2)),(20,15),Font_CV, .5,(255,255,255),1)
                                        cv2.imshow('Tracking',image_total)
                                        cv2.moveWindow('Tracking', 120,250);
                                        cv2.waitKey(5)
                                    
                                    Mat_Datos[Int_Contador][0] = (int(elemento.replace('image_','').replace('.jpg',''))/int(Int_Frame_2)) * float(Int_Frame)  
                                        
                                Mat_Datos[Int_Contador][4] = Int_Datos_Consecuencia
                                
                                if cv2.waitKey(1) & 0xFF == ord('q'):
                                    break  
                                
                                Int_Contador += 1   
                                
                            cv2.destroyAllWindows()
                            
                            Mat_Datos = np.delete(Mat_Datos,np.where(Mat_Datos[:,0] == 0), axis=0)
                            Mat_Datos_X = Mat_Datos_X[0:len(Mat_Datos),:]
                            Mat_Datos_Y = Mat_Datos_Y[0:len(Mat_Datos),:]
                            Mat_Datos_D = Mat_Datos_D[0:len(Mat_Datos),:]
                              
                        
                            Nombre_Grafico =  filedialog.asksaveasfilename(initialdir = Dir_Datos,
                                                                         title = "Save Data",
                                                                         filetypes = (("all files","*.*"), ("txt files","*.txt"))) 
    
                            j = 0
                            for j in range(number_subject):
                                Archivo_Mat_Datos = open(Nombre_Grafico +'_' + str(j+1) + '.txt','w')
                                Archivo_Mat_Datos.write('Subject: ' + Str_Sujeto + '_' + str(j+1) +'\n' +
                                                        'Session: ' + Str_Sesion + '\n' +
                                                        'Group: ' + Str_Grupo + '\n' +
                                                        'Time: '+ str(round(max(Mat_Datos[:,0]),3)) + '\n' +
                                                        '# Consecuences: ' + str(np.size(np.where(Mat_Datos[:,4] == 1))) + '\n' +
                                                        'Distance: ' + str(round(sum(Mat_Datos_D[:,j]),3)) + 'cm' + '\n' +
                                                        'Velocity: ' + str(round(sum((Mat_Datos_D[:,j]/100)/Mat_Datos[:,0]),3)) + 'cm/seg' + '\n' +
                                                        'Mean Aceleration: ' + str(round(statistics.mean((Mat_Datos_D[:,j]/100)/Mat_Datos[:,0]),3)) + 'm/seg' + '\n' +
                                                        '\n' + 'Frame;Time;X;Y;Aceleration;Distance;Consecuences' + '\n')
                                i = 1
                                for i in range(0,len(Mat_Datos)): 
                                    Archivo_Mat_Datos.write(str(i) + ';' + str(round(Mat_Datos[i][0],3)) +
                                                                     ';' + str(round(Mat_Datos_X[i][j] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])),3)) +
                                                                     ';' + str(round(Mat_Datos_Y[i][j] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[16])),3)) +
                                                                     ';' + str(round((Mat_Datos_D[i,j]/100)/float(Int_Frame),3)) +
                                                                     ';' + str(round(Mat_Datos_D[i][j],3)) +
                                                                     ';' + str(Mat_Datos[i][4]) + '\n')
    
                            if Seleccion_Track == 3:
                                messagebox.showinfo("Finalized", "Sesion has been traked")
                            Main_Ses.destroy()
                    
                    
                    Lbl_Sujeto_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Subject')
                    Lbl_Sujeto_Text_1.config(font = (Font_1,18))
                    Lbl_Sujeto_Text_1.place(x=30, y = 30)
                    
                    Lbl_Sujeto_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
                    Lbl_Sujeto_TextBox_1.config(font = (Font_1,15))
                    Lbl_Sujeto_TextBox_1.place(x=150, y = 35)
                    
                    Lbl_Sesion_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Session')
                    Lbl_Sesion_Text_1.config(font = (Font_1,18))
                    Lbl_Sesion_Text_1.place(x=30, y = 80)
                    
                    Lbl_Sesion_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
                    Lbl_Sesion_TextBox_1.config(font = (Font_1,15))
                    Lbl_Sesion_TextBox_1.place(x=150, y = 85)
                    
                    Lbl_Grupo_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Group')
                    Lbl_Grupo_Text_1.config(font = (Font_1,18))
                    Lbl_Grupo_Text_1.place(x=30, y = 130)
                    
                    Lbl_Grupo_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
                    Lbl_Grupo_TextBox_1.config(font = (Font_1,15))
                    Lbl_Grupo_TextBox_1.place(x=150, y = 135)
                    
                    Bnt_Next = tkinter.Button(Main_Ses, bd=0, fg = Fun_Rgb(C_Pal5),
                                      bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                      highlightbackground=Fun_Rgb(C_Pal5),
                                      text = '  Run  ', command = Fun_Bnt_Next)
                    Bnt_Next.config(font = (Font_1,25))
                    Bnt_Next.place(x=aux_width_monitor*6.1, y = aux_height_monitor*11)
    
                    
                    Main_Ses.mainloop()
    
                Ventana_Sesion()           
            
            #%%En vivo --- 2
            if Seleccion_Track == 2:
                messagebox.showinfo("Error", "Select Live project")               
                
                
            #%%Abrir en Vivo--- 3
            if Seleccion_Track == 3:
                
                Direccion_Documento = filedialog.askopenfilename(initialdir = Dir_Proyecto,
                                                               title = "Seleccionar archivo",
                                                               filetypes = (("txt files","*.txt"),
                                                                            ("all files","*.*")))
                def Ventana_Sesion():
                
                    global Str_SesionT, Str_Sujeto, Str_Sesion, Str_Grupo
                    Str_SesionT = '10'
                    Str_Sujeto = '0'
                    Str_Sesion = '0'
                    Str_Grupo = '0'
                    
                    Main_Ses = tkinter.Tk()
                    Main_Ses.title('Run experiment 3D')
                    Main_Ses.geometry(str(int(aux_width_monitor*13.2))+'x'+str(height_monitor-100)+'+0+0')
                    Main_Ses.configure(background=Fun_Rgb(C_Pal5))
                    
                    Main_Ses_Can = Canvas(Main_Ses, width=round(aux_width_monitor*14), height=round(height_monitor-100), bg=Fun_Rgb(C_Pal5))
                    Main_Ses_Can.create_rectangle(10, 10, aux_width_monitor*13.2 -10, height_monitor-110, outline=Fun_Rgb(C_Pal3), width=4)
                    Main_Ses_Can.create_rectangle(40, 250, 440, 650, fill=Fun_Rgb(C_Black), outline=Fun_Rgb(C_Pal6), width=2)
                    Main_Ses_Can.create_rectangle(490, 250, 890, 650, fill=Fun_Rgb(C_Black), outline=Fun_Rgb(C_Pal6), width=2)
                    Main_Ses_Can.place(x=0,y=0) 
                    
                    Win_Cortar_Imagen.destroy()
                    
                    def Fun_Bnt_Next():
                        
                        Dir_Archivo_Parametros =open(Direccion_Documento,'r')  
                        Arr_Parametros_Imagen = Dir_Archivo_Parametros.read().split('\n') 
                        Dir_Archivo_Parametros.close()
                        
                        global number_subject
                        X1 = float(Arr_Parametros_Imagen[2])
                        X2 = float(Arr_Parametros_Imagen[3])
                        Y1 = float(Arr_Parametros_Imagen[4])
                        Y2 = float(Arr_Parametros_Imagen[5])
                        Rotar = float(Arr_Parametros_Imagen[6])
                        Dev_Espacio_Tamano = int(Arr_Parametros_Imagen[7])
                        Track_MinSize = float(Arr_Parametros_Imagen[14])
                        number_subject = int(Arr_Parametros_Imagen[17])
                        Size_Proportion = int(Arr_Parametros_Imagen[15])
                        
                        X12 = float(Arr_Parametros_Imagen[2+18])
                        X22 = float(Arr_Parametros_Imagen[3+18])
                        Y12 = float(Arr_Parametros_Imagen[4+18])
                        Y22 = float(Arr_Parametros_Imagen[5+18])
                        Rotar2 = float(Arr_Parametros_Imagen[6+18])
                        Dev_Espacio_Tamano2 = int(Arr_Parametros_Imagen[7+18])
                        
                        if (int(Arr_Parametros_Imagen[0]) == 0):
                            Seleccion_Camara = 0
                            Seleccion_Camara2 = 1
                        elif (int(Arr_Parametros_Imagen[0]) == 1):
                            Seleccion_Camara = 1
                            Seleccion_Camara2 = 2
                        
                        Dev_WebCam_Resolution = int(Arr_Parametros_Imagen[1])
                        Dev_WebCam_Read = cv2.VideoCapture(Seleccion_Camara)
                        Dev_WebCam_Resolution2 = int(Arr_Parametros_Imagen[1])
                        Dev_WebCam_Read2 = cv2.VideoCapture(Seleccion_Camara2)
                        
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
                        
                        if Dev_WebCam_Resolution2 == 1:
                            Dev_WebCam_Resolution2=(320,200)
                        elif Dev_WebCam_Resolution2 == 2:
                            Dev_WebCam_Resolution2=(480,320)
                        elif Dev_WebCam_Resolution2 == 3:
                            Dev_WebCam_Resolution2=(600,480)
                        elif Dev_WebCam_Resolution2 == 4:
                            Dev_WebCam_Resolution2=(800,600)
                        elif Dev_WebCam_Resolution2 == 5:
                            Dev_WebCam_Resolution2=(1280,800)   
                        Dev_WebCam_Read2.set(3,Dev_WebCam_Resolution2[0])
                        Dev_WebCam_Read2.set(4,Dev_WebCam_Resolution2[1])
                        
                        global Str_SesionT, Str_Sujeto, Str_Sesion, Str_Grupo
                        Str_SesionT = Lbl_SesionT_TextBox_1.get('1.0','end-1c')
                        Str_Sujeto = Lbl_Sujeto_TextBox_1.get('1.0','end-1c')
                        Str_Sesion = Lbl_Sesion_TextBox_1.get('1.0','end-1c')
                        Str_Grupo = Lbl_Grupo_TextBox_1.get('1.0','end-1c')
                        Var_Save_video = Var_Radiobutton.get()
                        Tiempo_Sesion = int(Str_SesionT)
                        
                        if Var_Save_video != 1:
                            Var_Save_video = 0
                        
                        global Nombre_Archivo, Ruta_Video, Ruta_Carpeta_Imagenes
                        Nombre_Archivo = Str_SesionT
                        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
                        out = cv2.VideoWriter(Dir_Videos + Nombre_Archivo + '.mp4',fourcc, 30.0, (640,480))
                
                        global Mat_Datos
                        Int_Contador = 1
                        Int_Datos_Consecuencia = 0
                        Int_Contador_Distancia = 0
                        Arr_TiempoReal = np.zeros(4)
                        Mat_Datos = np.zeros((9999999,8))
                        Mat_Datos[:,0] = -1
                        
                        def Fun_Distancia(x1,x2,y1,y2,DistanciaRelativa):
                            return math.sqrt((x2-x1)**2+(y2-y1)**2)*DistanciaRelativa
                        
                        def Fun_Distancia2(x1,x2,y1,y2,z1,z2,DistanciaRelativa):
                            return math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)*DistanciaRelativa
                        
                        global Mat_RGB
                        
                        if number_subject >0:
                            global Mat_Datos_X, Mat_Datos_Y, Mat_Datos_D, Mat_RGB 
                            Mat_Datos_X = np.zeros((9999999,16))
                            Mat_Datos_Y = np.zeros((9999999,16))
                            Mat_Datos_D = np.zeros((9999999,16))
                            
                            Dir_Archivo_Parametros =open(Direccion_Documento,'r')  
                            Arr_Parametros_Imagen = Dir_Archivo_Parametros.read().split('\n')    
                            Track_MinSize = float(Arr_Parametros_Imagen[14]) 
                            Dev_Espacio_Tamano = int(Arr_Parametros_Imagen[7])
                            number_subject = int(Arr_Parametros_Imagen[17])
                            Dir_Archivo_Parametros.close()
                            Mat_RGB = np.zeros((number_subject, 6))
                            aux_1 = 0
                            f = 0
                            for i in Arr_Parametros_Imagen:
                                b = i
                                aux_1 += 1
                                if aux_1 == 9:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][0] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 10:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][1] = e
                                        f += 1
                                    f = 0   
                                if aux_1 == 11:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][2] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 12:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][3] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 13:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][4] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 14:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][5] = e
                                        f += 1
                                    f = 0
                        else:
                            
                            Mat_RGB = ([int(Arr_Parametros_Imagen[8]), int(Arr_Parametros_Imagen[9]), int(Arr_Parametros_Imagen[10]),
                                        int(Arr_Parametros_Imagen[11]), float(Arr_Parametros_Imagen[12])])
                            Img_Filtro = int(Arr_Parametros_Imagen[13])            
                                        
                        #%%Sesion_Sujetos=1            
                        if number_subject ==0:
                            Arr_TiempoReal[0]=time.time()
                            
                            while(Tiempo_Sesion >= Arr_TiempoReal[3]):
                                
                                ret, Img_WebCam = Dev_WebCam_Read.read()
                                ret2, Img_WebCam2 = Dev_WebCam_Read2.read()
                                
                                
                                if ret==True and Var_Save_video == 1:
                                    out.write(Img_WebCam)
                                    
    #                            num_rows, num_cols = Img_WebCam.shape[:2]
                                num_rows, num_cols = Dev_WebCam_Resolution[1],Dev_WebCam_Resolution[0]
                                Mat_Img_Rotada = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), Rotar, 1)
                                Img_WebCam  = cv2.warpAffine(Img_WebCam, Mat_Img_Rotada, (num_cols, num_rows))
                                Img_WebCam = Img_WebCam[round(Dev_WebCam_Resolution[1]*Y1):round(Dev_WebCam_Resolution[1]*Y2),
                                                round(Dev_WebCam_Resolution[0]*X1):round(Dev_WebCam_Resolution[0]*X2)]
                                
                                num_rows2, num_cols2 = Dev_WebCam_Resolution2[1],Dev_WebCam_Resolution2[0]
                                Mat_Img_Rotada2 = cv2.getRotationMatrix2D((num_cols2/2, num_rows2/2), Rotar2, 1)
                                Img_WebCam2  = cv2.warpAffine(Img_WebCam2, Mat_Img_Rotada2, (num_cols2, num_rows2))
                                Img_WebCam2 = Img_WebCam2[round(Dev_WebCam_Resolution2[1]*Y12):round(Dev_WebCam_Resolution2[1]*Y22),
                                                          round(Dev_WebCam_Resolution2[0]*X12):round(Dev_WebCam_Resolution2[0]*X22)]
                                
                                Mat_WebCam_RGB = np.zeros([Dev_WebCam_Resolution[1],Dev_WebCam_Resolution[0],3])
                                Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,2]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[0]+Mat_RGB[3])))[0]),
                                               (np.where((Img_WebCam[:,:,2]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[0]+Mat_RGB[3])))[1]),0] = 1
                                Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[0]),
                                               (np.where((Img_WebCam[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[1]),1] = 1
                                Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,0]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[2]+Mat_RGB[3])))[0]),
                                               (np.where((Img_WebCam[:,:,0]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[2]+Mat_RGB[3])))[1]),2] = 1          
                                Img_WebCam = Mat_WebCam_RGB  
                                
                                Mat_WebCam_RGB2 = np.zeros([Dev_WebCam_Resolution2[1],Dev_WebCam_Resolution2[0],3])
                                Mat_WebCam_RGB2[(np.where((Img_WebCam2[:,:,2]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam2[:,:,2]<=(Mat_RGB[0]+Mat_RGB[3])))[0]),
                                               (np.where((Img_WebCam2[:,:,2]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam2[:,:,2]<=(Mat_RGB[0]+Mat_RGB[3])))[1]),0] = 1
                                Mat_WebCam_RGB2[(np.where((Img_WebCam2[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam2[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[0]),
                                               (np.where((Img_WebCam2[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam2[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[1]),1] = 1
                                Mat_WebCam_RGB2[(np.where((Img_WebCam2[:,:,0]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam2[:,:,0]<=(Mat_RGB[2]+Mat_RGB[3])))[0]),
                                               (np.where((Img_WebCam2[:,:,0]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam2[:,:,0]<=(Mat_RGB[2]+Mat_RGB[3])))[1]),2] = 1          
                                Img_WebCam2 = Mat_WebCam_RGB2  
                                       
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
                                
                                if Img_Filtro==1:
                                    Img_WebCam2 = ndimage.gaussian_filter(Img_WebCam2, sigma=3)
                                elif Img_Filtro==2:
                                    Img_WebCam2 = ndimage.gaussian_filter(Img_WebCam2, sigma=5)
                                elif Img_Filtro==3:
                                    Img_WebCam2 =ndimage.uniform_filter(Img_WebCam2, size=2)
                                elif Img_Filtro==4:
                                    Img_WebCam2 =ndimage.uniform_filter(Img_WebCam2, size=11)
                                np.place(Img_WebCam2[:,:,:], Img_WebCam2[:,:,:]>=Mat_RGB[4], 1)
                                np.place(Img_WebCam2[:,:,:], Img_WebCam2[:,:,:]<Mat_RGB[4], 0)
                            
                                try:
                                    Mat_Centroide = ndimage.label(Img_WebCam)[0]
                                    Centroide = scipy.ndimage.measurements.center_of_mass(Img_WebCam, Mat_Centroide, [1,2,3])
                                    Mat_Size = ndimage.label(Img_WebCam)[0]
                                    Size = np.sqrt(scipy.ndimage.measurements.sum(Img_WebCam, Mat_Size, [1,2,3]))
                                    MinSize = int(np.where(Size == np.min(Size[(Size >= Track_MinSize)]))[0])
                                    cv2.circle(Img_WebCam,(int(Centroide[MinSize][1]),int(Centroide[MinSize][0])),2,(0,0,255),5)
                                except:
                                    Img_WebCam = Img_WebCam
                                    
                                try:
                                    Mat_Centroide2 = ndimage.label(Img_WebCam2)[0]
                                    Centroide2 = scipy.ndimage.measurements.center_of_mass(Img_WebCam2, Mat_Centroide2, [1,2,3])
                                    Mat_Size2 = ndimage.label(Img_WebCam2)[0]
                                    Size2 = np.sqrt(scipy.ndimage.measurements.sum(Img_WebCam2, Mat_Size2, [1,2,3]))
                                    MinSize2 = int(np.where(Size2 == np.min(Size2[(Size2 >= Track_MinSize)]))[0])
                                    cv2.circle(Img_WebCam2,(int(Centroide2[MinSize2][1]),int(Centroide2[MinSize2][0])),2,(0,255,0),5)
                                except:
                                    Img_WebCam2 = Img_WebCam2
                            
                                Img_WebCam = cv2.resize(Img_WebCam,(400, round((400/Dev_WebCam_Resolution[0])*Dev_WebCam_Resolution[0])))
                                cv2.putText(Img_WebCam,'Time: ',(5,15),Font_CV, .5,(255,255,255),1)
                                cv2.putText(Img_WebCam,str(round((Arr_TiempoReal[3]) ,2)),(65,15),Font_CV, .5,(255,255,255),1)
                                cv2.putText(Img_WebCam,'D: ',(5,35),Font_CV, .5,(255,255,255),1)
                                cv2.putText(Img_WebCam,str(round(Int_Contador_Distancia ,2)),(20,35),Font_CV, .5,(255,255,255),1)
                                cv2.putText(Img_WebCam,'P: ',(5,55),Font_CV, .5,(255,255,255),1)
                                cv2.putText(Img_WebCam,(str(round(Mat_Datos[Int_Contador-1][1] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])),3)) + ', ' +
                                                        str(round(Mat_Datos[Int_Contador-1][2] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])),3)) + ', ' +
                                                        str(round(Mat_Datos[Int_Contador-1][6] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])),3))), (20,55),Font_CV, .5,(255,255,255),1)
                                cv2.imshow('Tracking XY',Img_WebCam)
                                cv2.moveWindow('Tracking XY', 40,250);
                                
                                Img_WebCam2 = cv2.resize(Img_WebCam2,(400, round((400/Dev_WebCam_Resolution2[0])*Dev_WebCam_Resolution2[0])))
                                cv2.imshow('Tracking Z',Img_WebCam2)
                                cv2.moveWindow('Tracking Z', 490,250);
                                
                                
                                Mat_Datos[Int_Contador][0] = Arr_TiempoReal[3]
                                try:
                                    Mat_Datos[Int_Contador][1] = int(Centroide[MinSize][1])
                                    Mat_Datos[Int_Contador][2] = int(Centroide[MinSize][0])
                                    Mat_Datos[Int_Contador][6] = int(Centroide2[MinSize][0])
                                except:
                                    Mat_Datos[Int_Contador][1] = Mat_Datos[Int_Contador-1][1]
                                    Mat_Datos[Int_Contador][2] = Mat_Datos[Int_Contador-1][2]
    #                            Mat_Datos[Int_Contador][3] = (Fun_Distancia(Mat_Datos[Int_Contador-1][1],Mat_Datos[Int_Contador][1],Mat_Datos[Int_Contador-1][2],Mat_Datos[Int_Contador][2],Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])))
                                Mat_Datos[Int_Contador][3] = (Fun_Distancia2(Mat_Datos[Int_Contador-1][1],
                                                                             Mat_Datos[Int_Contador][1],
                                                                             Mat_Datos[Int_Contador-1][2],
                                                                             Mat_Datos[Int_Contador][2],
                                                                             Mat_Datos[Int_Contador-1][6],
                                                                             Mat_Datos[Int_Contador][6],
                                                                             Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])))
                                Mat_Datos[Int_Contador][4] = Int_Datos_Consecuencia
                                Int_Contador_Distancia += Mat_Datos[Int_Contador][3]
                                
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
                                    
                            
                            #Guardar_Datos
                            Nombre_Grafico =  filedialog.asksaveasfilename(initialdir = Dir_Datos,
                                                                         title = "Save Data",
                                                                         filetypes = (("all files","*.*"), ("txt files","*.txt"))) 
                                          
                            #Datos_Generales
                            Archivo_Mat_Datos = open(Nombre_Grafico + '.txt','w')
                            Archivo_Mat_Datos.write('Subject: ' + Str_Sujeto + '\n' +
                                                    'Session: ' + Str_Sesion + '\n' +
                                                    'Group: ' + Str_Grupo + '\n' +
                                                    'Time: '+ str(max(Mat_Datos[:,0])) + '\n' +
                                                    '# Consecuences: ' + str(np.size(np.where(Mat_Datos[:,4] == 1))) + '\n' +
                                                    'Distance: ' + str(round(sum(Mat_Datos[:,3]),3)) + 'cm' + '\n' +
                                                    'Velocity: ' + str(round(sum(Mat_Datos[:,3])/max(Mat_Datos[:,0]),3)) + 'cm/seg' + '\n' +
                                                    'Mean Aceleration: ' + str(round(statistics.mean(Mat_Datos[:,5]),3)) + 'm/seg' + '\n' +
                                                    '\n' + 'Frame,Time,X,Y,Z,Distance,Events,Aceleration' + '\n')
                            
                            #Datos_Matriz
                            i = 1
                            for i in range(0,len(Mat_Datos)): 
                                Archivo_Mat_Datos.write(str(i) + ',' + str(round(Mat_Datos[i][0],3)) +
                                                                 ',' + str(round(Mat_Datos[i][1] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])),3)) +
                                                                 ',' + str(round(Mat_Datos[i][2] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[16])),3)) +
                                                                 ',' + str(round(Mat_Datos[i][6] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[16])),3)) +
                                                                 ',' + str(round(Mat_Datos[i][3],3)) +
                                                                 ',' + str(Mat_Datos[i][4]) + ';' + str(Mat_Datos[i][6]) +
                                                                 ',' + str(round(Mat_Datos[i][5],3)) + '\n')
                            Archivo_Mat_Datos.close() 
                            
                            if Seleccion_Track == 3:
                                messagebox.showinfo("Finalized", "Sesion has been traked")
                            Main_Ses.destroy()
                            
                        #%%Sesion_Sujetos>1       
                        else:
                            Arr_TiempoReal[0]=time.time()
                            
                            while(Tiempo_Sesion >= Arr_TiempoReal[3]):
                                
                                ret, Img_WebCam = Dev_WebCam_Read.read()
                                if ret==True and Var_Save_video == 1:
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
                        
                                    if Mat_RGB[i][5]==1:
                                        image_aux = ndimage.gaussian_filter(image_aux, sigma=3)
                                    elif Mat_RGB[i][5]==2:
                                        image_aux = ndimage.gaussian_filter(image_aux, sigma=5)
                                    elif Mat_RGB[i][5]==3:
                                        image_aux =ndimage.uniform_filter(image_aux, size=2)
                                    elif Mat_RGB[i][5]==4:
                                        image_aux =ndimage.uniform_filter(image_aux, size=11)
                                    elif Mat_RGB[i][5]==5:
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
                                    Mat_Datos_D[Int_Contador][i] = (Fun_Distancia(Mat_Datos_X[Int_Contador-1][i],Mat_Datos_X[Int_Contador][i],Mat_Datos_Y[Int_Contador-1][i],Mat_Datos_Y[Int_Contador][i],Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])))  
                                    
                                    image_total += image_aux
                                    if i == number_subject -1:
                                        image_total = cv2.resize(image_total,(400, round((400/Img_WebCam.shape[1])*Img_WebCam.shape[1])))
                                        j = 0
                                        for j in range(number_subject):
                                            cv2.putText(image_total,str(j+1),(round(int(Mat_Datos_X[Int_Contador][j]) * 400/int(Arr_Parametros_Imagen[15])) + 10,
                                                                              round(int(Mat_Datos_Y[Int_Contador][j]) * 400/int(Arr_Parametros_Imagen[16]))),
                                                                              Font_CV, .5,(0,0,255),1)
                                            #cv2.putText(image_total,str(round(sum(Mat_Datos_D[:,j]),2)),(65*(j+1),35),Font_CV, .5,(255,255,255),1)    
                                        #cv2.putText(image_total,'D: ',(5,35),Font_CV, .5,(255,255,255),1)
                                        cv2.putText(image_total,'Time: ',(5,15),Font_CV, .5,(255,255,255),1)
                                        cv2.putText(image_total,str(round((Arr_TiempoReal[3]) ,2)),(65,15),Font_CV, .5,(255,255,255),1)
                                        cv2.imshow('Tracking',image_total)
                                        cv2.moveWindow('Tracking', 120,250);
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
                            
                            #Guardar_Datos
                            Nombre_Grafico =  filedialog.asksaveasfilename(initialdir = Dir_Datos,
                                                                         title = "Save Data",
                                                                         filetypes = (("all files","*.*"), ("txt files","*.txt"))) 
                                          
                            #Datos
                            j = 0
                            for j in range(number_subject):
                                #Datos_Generales
                                Archivo_Mat_Datos = open(Nombre_Grafico +'_' + str(j+1) + '.txt','w')
                                Archivo_Mat_Datos.write('Subject: ' + Str_Sujeto + '_' + str(j+1) +'\n' +
                                                        'Session: ' + Str_Sesion + '\n' +
                                                        'Group: ' + Str_Grupo + '\n' +
                                                        'Time: '+ str(max(Mat_Datos[:,0])) + '\n' +
                                                        '# Consecuences: ' + str(np.size(np.where(Mat_Datos[:,4] == 1))) + '\n' +
                                                        'Distance: ' + str(round(sum(Mat_Datos_D[:,j]),3)) + 'cm' + '\n' +
                                                        'Velocity: ' + str(round(sum(Mat_Datos_D[:,j])/max(Mat_Datos[:,0]),3)) + 'cm/seg' + '\n' +
                                                        'Mean Aceleration: ' + str(round(statistics.mean(Mat_Datos_D[:,j]/100)/statistics.mean(Mat_Datos[:,0]),3)) + 'm/seg' + '\n' +
                                                        '\n' + 'Frame;Time;X;Y;Aceleration;Distance;Consecuences' + '\n')
                                #Datos_Matriz
                                i = 1
                                for i in range(0,len(Mat_Datos)): 
                                    Archivo_Mat_Datos.write(str(i) + ';' + str(round(Mat_Datos[i][0],3)) +
                                                                     ';' + str(round(Mat_Datos_X[i][j] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])),3)) +
                                                                     ';' + str(round(Mat_Datos_Y[i][j] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[16])),3)) +
                                                                     ';' + str(round((Mat_Datos_D[i,j]/100)/Mat_Datos[i,0],3)) +
                                                                     ';' + str(round(Mat_Datos_D[i][j],3)) +
                                                                     ';' + '0' + '\n')
                                
                            
               
                            
                            if Seleccion_Track == 3:
                                messagebox.showinfo("Finalized", "Sesion has been traked")
                            Main_Ses.destroy()
                    
                    
                    #Tiempo
                    Lbl_SesionT_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Time')
                    Lbl_SesionT_Text_1.config(font = (Font_1,18))
                    Lbl_SesionT_Text_1.place(x=30, y = 30)
                    #Box
                    Lbl_SesionT_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
                    Lbl_SesionT_TextBox_1.config(font = (Font_1,15))
                    Lbl_SesionT_TextBox_1.place(x=150, y = 35)
                    
                    #Sujeto
                    Lbl_Sujeto_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Subject')
                    Lbl_Sujeto_Text_1.config(font = (Font_1,18))
                    Lbl_Sujeto_Text_1.place(x=30, y = 80)
                    #Box
                    Lbl_Sujeto_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
                    Lbl_Sujeto_TextBox_1.config(font = (Font_1,15))
                    Lbl_Sujeto_TextBox_1.place(x=150, y = 85)
                    
                    #Sesion
                    Lbl_Sesion_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Session')
                    Lbl_Sesion_Text_1.config(font = (Font_1,18))
                    Lbl_Sesion_Text_1.place(x=30, y = 130)
                    #Box
                    Lbl_Sesion_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
                    Lbl_Sesion_TextBox_1.config(font = (Font_1,15))
                    Lbl_Sesion_TextBox_1.place(x=150, y = 135)
                    
                    #Grupo
                    Lbl_Grupo_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Group')
                    Lbl_Grupo_Text_1.config(font = (Font_1,18))
                    Lbl_Grupo_Text_1.place(x=30, y = 180)
                    #Box
                    Lbl_Grupo_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
                    Lbl_Grupo_TextBox_1.config(font = (Font_1,15))
                    Lbl_Grupo_TextBox_1.place(x=150, y = 185)
                    
                    Lbl_Save_Text = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Save video')
                    Lbl_Save_Text.config(font = (Font_1,14))
                    Lbl_Save_Text.place(x=aux_width_monitor*11.1, y = aux_height_monitor*10.2)
            
                    Var_Radiobutton = tkinter.IntVar(Main_Ses)
                    radiobutton1 = tkinter.Radiobutton(Main_Ses, text='', bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), 
                                                       activebackground=Fun_Rgb(C_Pal4),
                                                       highlightbackground=Fun_Rgb(C_Pal5), variable=Var_Radiobutton, value=1)
                    radiobutton1.config(font = (Font_1,24))
                    radiobutton1.place(x=aux_width_monitor*12.2, y = aux_height_monitor*10.05)
                    Var_Radiobutton.get()
                    
                    #Bnt Next
                    Bnt_Next = tkinter.Button(Main_Ses, bd=0, fg = Fun_Rgb(C_Pal5),
                                              bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                              highlightbackground=Fun_Rgb(C_Pal5),
                                              text = '  Run  ', command = Fun_Bnt_Next)
                    Bnt_Next.config(font = (Font_1,25))
                    Bnt_Next.place(x=aux_width_monitor*11.1, y = aux_height_monitor*11)
                    
                    Main_Ses.mainloop()
        
                
                Ventana_Sesion()
                             
        #%%Next subject function
        def Fun_Next_Subject():
            
            if Seleccion_Track == 0:
                messagebox.showinfo("Error", "Select a traking option")
            
            aux_count = 0
            global number_subject, Mat_RGB
            Var_R = int(Slider_Rojo.get())
            Var_G = int(Slider_Verde.get())
            Var_B = int(Slider_Azul.get())
            Var_Des = int(Slider_Desviacion.get())
            Var_Umbral = float(Entr_Umbral.get())
            Img_Filtro = Var_Filtro.get()
        #    Mat_RGB2 = ([Var_R, Var_G, Var_B, Var_Des, 1, Img_Filtro])
            Mat_RGB2 = ([Var_R, Var_G, Var_B, Var_Des, Var_Umbral, Img_Filtro])
            
            global Lbl_Img_Original, Lbl_Img_Original_Aux
            Lbl_Img_Original.place_forget()
            Lbl_Img_Original_Aux.place_forget()
            
            #Direccion_nueva Imagen
            global Dialog_Video_File_Aux_2
            Dialog_Video_File_Aux_2 = Dialog_Video_File_Aux.replace('Aux_Image', 'Aux_Imagee')
            
            #Guardar Imagenes
            Img_Cortable = imageio.imread(Dialog_Video_File_Aux)
            Img_Cortable_Aux = Img_Cortable[:, :]
            imageio.imsave(Dialog_Video_File_Aux_2, Img_Cortable_Aux)
            
            Img_Original_2 = Image.open(Dialog_Video_File_Aux)
            if int(Img_Original_2.size[0])>Var_Tamaño_Lbl_X:
                Img_Original_2 = Img_Original_2.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original_2.size[0]))*int(Img_Original_2.size[1]))), 
                                Image.ANTIALIAS)
                if int(Img_Original_2.size[1]) > Var_Tamaño_Lbl_Y:
                    Img_Original_2 = Img_Original_2.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original_2.size[1]))*int(Img_Original_2.size[0])),Var_Tamaño_Lbl_Y), 
                                Image.ANTIALIAS)
            elif int(Img_Original_2.size[1])>Var_Tamaño_Lbl_Y:
                Img_Original_2 = Img_Original_2.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original_2.size[1]))*int(Img_Original_2.size[0])),Var_Tamaño_Lbl_Y), 
                                                Image.ANTIALIAS)
                if int(Img_Original_2.size[0]) > Var_Tamaño_Lbl_X:
                    Img_Original_2 = Img_Original_2.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original_2.size[0]))*int(Img_Original_2.size[1]))), 
                                                    Image.ANTIALIAS)
            
            #Mostrar Imagen
            Pho_Img_Cortable_Aux = ImageTk.PhotoImage(Img_Original_2)
            Lbl_Parametros_Aux = tkinter.Label(image=Pho_Img_Cortable_Aux, bg = Fun_Rgb(C_Pal5), bd = 0)
            Lbl_Parametros_Aux.image = Pho_Img_Cortable_Aux 
            Lbl_Parametros_Aux.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*1.5)+1)
           
            
            if aux_count == 0:
                Mat_RGB[number_subject][:]= Mat_RGB2
                number_subject += 1 
                
                Slider_Rojo.set(0)
                Slider_Verde.set(0)
                Slider_Azul.set(0)
                Slider_Desviacion.set(0)
                Entr_Umbral.set(.5)
                Var_Filtro.set(0)
                      
        #%%Widgets Cortar imagen
        
        Slider_X1 = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=0, to=.5, resolution=0.01,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*1.5,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal3), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal3),
                                  showvalue=1)
        Slider_X1.config(font=(Font_1,11))
        Slider_X1.place(x=int(aux_width_monitor*1.5), y=int(aux_height_monitor*.4))
        
        
        Slider_X2 = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=.51, to=1, resolution=0.01,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*1.5,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal3), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal3),
                                  showvalue=1)
        Slider_X2.config(font=(Font_1,11))
        Slider_X2.set(1)
        Slider_X2.place(x=aux_width_monitor*3.2, y=aux_height_monitor*.4)
    
        Slider_Y1 = tkinter.Scale(Win_Cortar_Imagen,
                                  from_=0, to=.5, resolution=0.01,
                                  orient=tkinter.VERTICAL, width = aux_height_monitor*.3,  length=aux_height_monitor*2.2,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal3), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal3),
                                  showvalue=1)
        Slider_Y1.config(font=(Font_1,11))
        Slider_Y1.place(x=aux_width_monitor*.7, y=aux_height_monitor*1.5)
    
        Slider_Y2 = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=.51, to=1, resolution=0.01,
                                  orient=tkinter.VERTICAL, width = aux_height_monitor*.3,  length=aux_height_monitor*2.2,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal3), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal3),
                                  showvalue=1)
        Slider_Y2.config(font=(Font_1,11))
        Slider_Y2.set(1)
        Slider_Y2.place(x=aux_width_monitor*.7, y=aux_height_monitor*4.1)
        
        
        Slider_Grados_Rotar = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=-90, to=90, resolution=1,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*2.5,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal3), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal3),
                                  showvalue=1)
        Slider_Grados_Rotar.config(font = (Font_1,11))
        Slider_Grados_Rotar.set(0)
        Slider_Grados_Rotar.place(x=aux_width_monitor*5, y=aux_height_monitor*2)
        Lbl_Slider_Grados_Rotar = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), 
                                     text = 'Image degrees')
        Lbl_Slider_Grados_Rotar.config(font=(Font_1,14))
        Lbl_Slider_Grados_Rotar.place(x=aux_width_monitor*5, y=aux_height_monitor*1.4)
        
        
        Etr_Tamano_Caja = tkinter.Entry(Win_Cortar_Imagen, width = 16)
        Etr_Tamano_Caja.config(font = (Font_1,18))
        Etr_Tamano_Caja.place(x=aux_width_monitor*5, y=aux_height_monitor*3.7)
        Etr_Tamano_Caja.insert(0,'1')
        Lbl_Etr_Tamano_Caja = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), 
                                     text = 'Image size')
        Lbl_Etr_Tamano_Caja.config(font=(Font_1,14))
        Lbl_Etr_Tamano_Caja.place(x=aux_width_monitor*5, y=aux_height_monitor*3.1)
        
    
               
        Btn_Cortar_Imagen = tkinter.Button(Win_Cortar_Imagen, bd=0, fg = Fun_Rgb(C_Pal5),
                                           highlightbackground=Fun_Rgb(C_Pal3), width=10, 
                                          bg = Fun_Rgb(C_Pal3), activebackground=Fun_Rgb(C_Pal5),
                                          text = 'Preview', command =Fun_Imagen)
        Btn_Cortar_Imagen.config(font = (Font_1,18))
        Btn_Cortar_Imagen.place(x=aux_width_monitor*5.8, y=aux_height_monitor*5.6)
        
        
        #%%Widgets Cortar imagen
        
        Slider2_X1 = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=0, to=.5, resolution=0.01,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*1.5,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal7), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal7),
                                  showvalue=1)
        Slider2_X1.config(font=(Font_1,11))
        Slider2_X1.place(x=int(aux_width_monitor*1.5), y=int(aux_height_monitor*6.5))
        
        
        Slider2_X2 = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=.51, to=1, resolution=0.01,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*1.5,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal7), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal7),
                                  showvalue=1)
        Slider2_X2.config(font=(Font_1,11))
        Slider2_X2.set(1)
        Slider2_X2.place(x=aux_width_monitor*3.2, y=aux_height_monitor*6.5)
    
        Slider2_Y1 = tkinter.Scale(Win_Cortar_Imagen,
                                  from_=0, to=.5, resolution=0.01,
                                  orient=tkinter.VERTICAL, width = aux_height_monitor*.3,  length=aux_height_monitor*2.2,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal7), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal7),
                                  showvalue=1)
        Slider2_Y1.config(font=(Font_1,11))
        Slider2_Y1.place(x=aux_width_monitor*.7, y=aux_height_monitor*7.6)
    
        Slider2_Y2 = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=.51, to=1, resolution=0.01,
                                  orient=tkinter.VERTICAL, width = aux_height_monitor*.3,  length=aux_height_monitor*2.2,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal7), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal7),
                                  showvalue=1)
        Slider2_Y2.config(font=(Font_1,11))
        Slider2_Y2.set(1)
        Slider2_Y2.place(x=aux_width_monitor*.7, y=aux_height_monitor*10.2)
        
        
        Slider2_Grados_Rotar = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=-90, to=90, resolution=1,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*2.5,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal7), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal7),
                                  showvalue=1)
        Slider2_Grados_Rotar.config(font = (Font_1,11))
        Slider2_Grados_Rotar.set(0)
        Slider2_Grados_Rotar.place(x=aux_width_monitor*5, y=aux_height_monitor*8.15)
        Lbl2_Slider_Grados_Rotar = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), 
                                     text = 'Image degrees')
        Lbl2_Slider_Grados_Rotar.config(font=(Font_1,14))
        Lbl2_Slider_Grados_Rotar.place(x=aux_width_monitor*5, y=aux_height_monitor*7.5)
        
        
        Etr2_Tamano_Caja = tkinter.Entry(Win_Cortar_Imagen, width = 16)
        Etr2_Tamano_Caja.config(font = (Font_1,18))
        Etr2_Tamano_Caja.place(x=aux_width_monitor*5, y=aux_height_monitor*9.85)
        Etr2_Tamano_Caja.insert(0,'1')
        Lbl2_Etr_Tamano_Caja = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), 
                                     text = 'Image size')
        Lbl2_Etr_Tamano_Caja.config(font=(Font_1,14))
        Lbl2_Etr_Tamano_Caja.place(x=aux_width_monitor*5, y=aux_height_monitor*9.2)
        
    
               
        Btn2_Cortar_Imagen = tkinter.Button(Win_Cortar_Imagen, bd=0, fg = Fun_Rgb(C_Pal5),
                                           highlightbackground=Fun_Rgb(C_Pal7), width=10, 
                                          bg = Fun_Rgb(C_Pal7), activebackground=Fun_Rgb(C_Pal5),
                                          text = 'Preview', command =Fun_Imagen2)
        Btn2_Cortar_Imagen.config(font = (Font_1,18))
        Btn2_Cortar_Imagen.place(x=aux_width_monitor*5.8, y=aux_height_monitor*11.8)
        
        #%%Widgets Edicion imagen  
        global arr_Color_Cuadro, arr_Color_Cuadro1, arr_Color_Cuadro2
        
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
      
        Lbl_Slider_1 = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal3), 
                                     text = 'Color')
        Lbl_Slider_1.config(font=(Font_1,20))
        Lbl_Slider_1.place(x=aux_width_monitor*7.8, y=aux_height_monitor*.7)
        
        #Slider 1
        Lbl_Slider_RojoText_1 = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), 
                                          fg = Fun_Rgb(C_Pal4), text = 'R')
        Lbl_Slider_RojoText_1.config(font = (Font_1,20))
        Lbl_Slider_RojoText_1.place(x=aux_width_monitor*7.8, y=aux_height_monitor*1.5)
        
        Slider_Rojo = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=0, to=255, resolution=1,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*2.5,
                                  fg=Fun_Rgb(C_Pal3), bg=Fun_Rgb(C_Pal4), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal5), troughcolor= Fun_Rgb(C_Pal5),
                                  highlightbackground=Fun_Rgb(C_Pal4),
                                  showvalue=1, command = Fun_Color_CuadroR)
        Slider_Rojo.set(255)
        Slider_Rojo.config(font = (Font_1,12))
        Slider_Rojo.place(x=aux_width_monitor*8.3, y=aux_height_monitor*1.5)
        
        
        #Slider 2
        Lbl_Slider_VerdeText_1 = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), 
                                           fg = Fun_Rgb(C_Pal4), text = 'G')
        Lbl_Slider_VerdeText_1.config(font = (Font_1,20))
        Lbl_Slider_VerdeText_1.place(x=aux_width_monitor*7.8, y=aux_height_monitor*2.7)
        Slider_Verde = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=0, to=255, resolution=1,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*2.5,
                                  fg=Fun_Rgb(C_Pal3), bg=Fun_Rgb(C_Pal4), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal5), troughcolor= Fun_Rgb(C_Pal5),
                                  highlightbackground=Fun_Rgb(C_Pal4),
                                  showvalue=1, command = Fun_Color_CuadroG )
        Slider_Verde.set(255)
        Slider_Verde.config(font = (Font_1,12))
        Slider_Verde.place(x=aux_width_monitor*8.3, y=aux_height_monitor*2.7)
        
        #Slider 3
        Lbl_Slider_AzulText_1 = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), 
                                          fg = Fun_Rgb(C_Pal4), text = 'B')
        Lbl_Slider_AzulText_1.config(font = (Font_1,20))
        Lbl_Slider_AzulText_1.place(x=aux_width_monitor*7.8, y=aux_height_monitor*3.9)
        Slider_Azul = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=0, to=255, resolution=1,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*2.5,
                                  fg=Fun_Rgb(C_Pal3), bg=Fun_Rgb(C_Pal4), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal5), troughcolor= Fun_Rgb(C_Pal5),
                                  highlightbackground=Fun_Rgb(C_Pal4),
                                  showvalue=1, command = Fun_Color_CuadroB )
        Slider_Azul.set(255)
        Slider_Azul.config(font = (Font_1,12))
        Slider_Azul.place(x=aux_width_monitor*8.3, y=aux_height_monitor*3.9)
        
        #Slider Desviación
        Lbl_Slider_Desviacio = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal4), 
                                     text = 'Range')
        Lbl_Slider_Desviacio.config(font=(Font_1,20))
        Lbl_Slider_Desviacio.place(x=aux_width_monitor*13.8, y=aux_height_monitor*.7)
        Slider_Desviacion = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=0, to=150, resolution=1,
                                  orient=tkinter.VERTICAL, width = aux_height_monitor*.4,  length= aux_width_monitor*2.4,
                                  fg=Fun_Rgb(C_Pal3), bg=Fun_Rgb(C_Pal4), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal5), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal4),
                                  showvalue=1, command = Fun_Color_Des)
        Slider_Desviacion.set(0)
        Slider_Desviacion.config(font = (Font_1,14))
        Slider_Desviacion.place(x=aux_width_monitor*13.9, y=aux_height_monitor*1.5)
        
        Rgb_Can = Canvas(Win_Cortar_Imagen, width=int(aux_width_monitor*2.4), highlightbackground = Fun_Rgb(C_Pal4),
                         height= int(aux_width_monitor*2.4), bg=Fun_Rgb(C_Black))
        Cuadro_Rgb2 =  Rgb_Can.create_rectangle(0, 0, aux_width_monitor*.8, aux_width_monitor*2.5, outline=Fun_Rgb(C_Black), width=0)
        Cuadro_Rgb1 =  Rgb_Can.create_rectangle(aux_width_monitor*.8, 0, aux_width_monitor*1.6, aux_width_monitor*2.5, outline=Fun_Rgb(C_Black), width=0)
        Cuadro_Rgb3 =  Rgb_Can.create_rectangle(aux_width_monitor*1.6, 0, aux_width_monitor*2.5, aux_width_monitor*2.5, outline=Fun_Rgb(C_Black), width=0)
        Rgb_Can.place(x=aux_width_monitor*11.15, y=aux_height_monitor*1.5)  
        
        
        #filtros
        Lbl_Filtro_1 = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), 
                                     fg = Fun_Rgb(C_Pal3), highlightbackground = Fun_Rgb(C_Pal5),
                                     text = 'Filter')
        Lbl_Filtro_1.config(font = (Font_1,20))
        Lbl_Filtro_1.place(x=aux_width_monitor*7.8, y=aux_height_monitor*5.5)
        
        Var_Filtro = tkinter.IntVar()
        RdBtn_1 = tkinter.Radiobutton(Win_Cortar_Imagen,bd=0, fg = Fun_Rgb(C_Pal3),
                                      bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal4), 
                                      highlightbackground = Fun_Rgb(C_Pal5),
                                      text="Black & White - Weak  ", variable=Var_Filtro, 
                                      value=1, indicatoron=0, width = 23)
        RdBtn_1.config(font = (Font_1,15))
        RdBtn_1.place(x=aux_width_monitor*7.8, y=aux_height_monitor*6.4)
        RdBtn_2 = tkinter.Radiobutton(Win_Cortar_Imagen,bd=0, fg = Fun_Rgb(C_Pal3),
                                      bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal4), 
                                      highlightbackground = Fun_Rgb(C_Pal5),
                                      text="Black & White - Strong", variable=Var_Filtro, 
                                      value=2, indicatoron=0, width = 23)
        RdBtn_2.config(font = (Font_1,15))
        RdBtn_2.place(x=aux_width_monitor*7.8, y=aux_height_monitor*7.2)
        RdBtn_3 = tkinter.Radiobutton(Win_Cortar_Imagen,bd=0, fg = Fun_Rgb(C_Pal3),
                                      bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal4), 
                                      highlightbackground = Fun_Rgb(C_Pal5),
                                      text="Uniform - Weak       ", variable=Var_Filtro, 
                                      value=3, indicatoron=0, width = 22)
        RdBtn_3.config(font = (Font_1,15))
        RdBtn_3.place(x=aux_width_monitor*11.4, y=aux_height_monitor*6.4)
        RdBtn_4 = tkinter.Radiobutton(Win_Cortar_Imagen,bd=0, fg = Fun_Rgb(C_Pal3),
                                      bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal4), 
                                      highlightbackground = Fun_Rgb(C_Pal5),
                                      text="Uniform - Strong     ", variable=Var_Filtro, 
                                      value=4, indicatoron=0, width = 22)
        RdBtn_4.config(font = (Font_1,15))
        RdBtn_4.place(x=aux_width_monitor*11.4, y=aux_height_monitor*7.2)
        RdBtn_5 = tkinter.Radiobutton(Win_Cortar_Imagen,bd=0, fg = Fun_Rgb(C_Pal3),
                                      bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal4),
                                      highlightbackground = Fun_Rgb(C_Pal5),
                                      text="No Filter             ", variable=Var_Filtro, 
                                      value=5, indicatoron=0, width = 23)
        RdBtn_5.config(font = (Font_1,15))
        RdBtn_5.place(x=aux_width_monitor*7.8, y=aux_height_monitor*8)
        
        Var_Filtro.get()
        
        #Otros
        Lbl_Filtro_2 = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal3), 
                                     text = 'Threshold')
        Lbl_Filtro_2.config(font = (Font_1,20))
        Lbl_Filtro_2.place(x=aux_width_monitor*7.8, y=aux_height_monitor*9.1)
        
        Entr_Umbral = tkinter.Scale(Win_Cortar_Imagen, 
                                    from_= 0, to=1, resolution=0.01,
                                    orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*3,
                                    fg=Fun_Rgb(C_Pal3), bg=Fun_Rgb(C_Pal4), bd = 0,
                                    activebackground=Fun_Rgb(C_Pal5), troughcolor= Fun_Rgb(C_Pal5), 
                                    highlightbackground=Fun_Rgb(C_Pal4),
                                    showvalue=1)
        Entr_Umbral.config(font = (Font_1,15))
        Entr_Umbral.set(.5)
        Entr_Umbral.place(x=aux_width_monitor*7.8, y=aux_height_monitor*10)
        
        Lbl_Filtro_3 = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal3), 
                                     text = 'Target size')
        Lbl_Filtro_3.config(font = (Font_1,20))
        Lbl_Filtro_3.place(x=aux_width_monitor*11.4, y=aux_height_monitor*9.1)        
        Entr_Valor_Minimo_Animal = tkinter.Scale(Win_Cortar_Imagen, 
                                    from_= 0, to=50, resolution=1,
                                    orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*3,
                                    fg=Fun_Rgb(C_Pal3), bg=Fun_Rgb(C_Pal4), bd = 0,
                                    activebackground=Fun_Rgb(C_Pal5), troughcolor= Fun_Rgb(C_Pal5), 
                                    highlightbackground=Fun_Rgb(C_Pal4),
                                    showvalue = 1)
        Entr_Valor_Minimo_Animal.config(font = (Font_1,15))
        Entr_Valor_Minimo_Animal.set(3)
        Entr_Valor_Minimo_Animal.place(x=aux_width_monitor*11.4, y=aux_height_monitor*10)
        
        
        
        #%%Bnt Funciones Ventana Cortar imagen
        
        Btn_Ver_Imagen = tkinter.Button(Win_Cortar_Imagen, bd=0, fg = Fun_Rgb(C_Pal3),
                                          bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal5),
                                          text = ' Preview ', highlightbackground = Fun_Rgb(C_Pal5), 
                                          command =Fun_Editar_Imagen)
        Btn_Ver_Imagen.config(font = (Font_1,20))
        Btn_Ver_Imagen.place(x=aux_width_monitor*7.8, y=aux_height_monitor*11.6)
        
        ########################
        Btn_Next_Subject = tkinter.Button(Win_Cortar_Imagen, bd=0, fg = Fun_Rgb(C_Pal3),
                                  bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal5),
                                  text = ' ', highlightbackground = Fun_Rgb(C_Pal5), 
                                  command =Fun_Next_Subject)
        Btn_Next_Subject.config(font = (Font_1,1))
        Btn_Next_Subject.place(x=aux_width_monitor*9.4, y=aux_height_monitor*11.6)
        ###########################3
        
        Btn_Cortar_Imagen = tkinter.Button(Win_Cortar_Imagen, bd=0, fg = Fun_Rgb(C_Pal3),
                                          bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal5),
                                          text = '   Save   ', highlightbackground = Fun_Rgb(C_Pal5), 
                                          command =Fun_Editar_Todas_Imagenes)
        Btn_Cortar_Imagen.config(font = (Font_1,20))
        Btn_Cortar_Imagen.place(x=aux_width_monitor*11.5, y=aux_height_monitor*11.6)
        
        Btn_Iniciar_Track = tkinter.Button(Win_Cortar_Imagen, bd=0, fg = Fun_Rgb(C_Pal3),
                                          bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal5),
                                          text = 'Tracking ', highlightbackground = Fun_Rgb(C_Pal5), 
                                          command =Fun_Iniciar_Track)
        Btn_Iniciar_Track.config(font = (Font_1,20))
        Btn_Iniciar_Track.place(x=aux_width_monitor*13.1, y=aux_height_monitor*11.6)
        
        Win_Cortar_Imagen.mainloop()
        
        ##############################
                
        
    def Fun_Track_Vivo_Y_Videos():
        ventanaMenuPrincipal.destroy()
        
        Win_Cortar_Imagen = tkinter.Tk()  
        Win_Cortar_Imagen.config(width=400, height=400)
        Win_Cortar_Imagen.geometry(str(width_monitor)+'x'+str(int(aux_height_monitor*13))+'+0+0') 
        Win_Cortar_Imagen.title('Projects')
        Win_Cortar_Imagen.config(bg = Fun_Rgb(C_Pal5))
        
        Win_Cortar_Imagen_Can = Canvas(width=int(width_monitor), height=int(aux_height_monitor*14), bg=Fun_Rgb(C_Pal5))#(Win_Cortar_Imagen, width=1280, height=800, bg=Fun_Rgb(C_Pal5))
        Win_Cortar_Imagen_Can.create_rectangle(aux_width_monitor*.1, aux_height_monitor*.1, aux_width_monitor*14.9, aux_height_monitor*12.9,
                                               outline=Fun_Rgb(C_Pal3), width=4)
        Win_Cortar_Imagen_Can.create_rectangle(int(aux_width_monitor*1.5), int(aux_height_monitor*1.5), width_monitor-(width_monitor/2)+1, (height_monitor/3)*2.2 +1, fill=Fun_Rgb(C_Pal6), outline=Fun_Rgb(C_Pal3), width=2)
        Win_Cortar_Imagen_Can.place(x=0,y=0)  
              
        def Fun_Ayuda():
            messagebox.showinfo("Help","")
            
        def Fun_Cam_Frontal():
            global Seleccion_Camara
            Seleccion_Camara = 0
            return(Seleccion_Camara)
        def Fun_Otra_Camara():
            global Seleccion_Camara
            Seleccion_Camara = 1
            return(Seleccion_Camara)  
            
        def Fun_Res_320x200():
            global Seleccion_Resolucion
            Seleccion_Resolucion = 1
            return(Seleccion_Resolucion)
        def Fun_Res_480x320():
            global Seleccion_Resolucion
            Seleccion_Resolucion = 2
            return(Seleccion_Resolucion)
        def Fun_Res_600x480():
            global Seleccion_Resolucion
            Seleccion_Resolucion = 3
            return(Seleccion_Resolucion)
        def Fun_Res_800x600():
            global Seleccion_Resolucion
            Seleccion_Resolucion = 4
            return(Seleccion_Resolucion)
        def Fun_Res_1280x800():
            global Seleccion_Resolucion
            Seleccion_Resolucion = 5
            return(Seleccion_Resolucion)
            
        def Fun_Open_Video(): 
            Ruta_Video = filedialog.askopenfilename(initialdir = Dir_Videos,
                                                    title = "Select Video",
                                                    filetypes = (("mp4 files","*.mp4"),
                                                    ("all files","*.*")))
        
            cap = cv2.VideoCapture(Ruta_Video)
            Arr_TiempoReal = np.zeros(4)    
            
            while(cap.isOpened()):
                Arr_TiempoReal[0]=time.time() 
                ret, frame = cap.read()
                if ret ==False:
                    break
            
                cv2.imshow('Video',frame)
                cv2.moveWindow('Video', int(aux_width_monitor*1.5), int(aux_height_monitor*1.5))
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                Arr_TiempoReal[1]=time.time()
                time.sleep(.03)
                Arr_TiempoReal[2]=Arr_TiempoReal[1]-Arr_TiempoReal[0] 
                Arr_TiempoReal[3]+= Arr_TiempoReal[2]
                
            cap.release()
            cv2.destroyAllWindows()
            
        def Fun_Take_video():
            global Name_Video, Seleccion_Camara
            Name_Video = filedialog.asksaveasfilename(initialdir = Dir_Videos,
                                                        title = "Video name",
                                                        filetypes = (("all files","*.*"),
                                                        ("jpeg files","*.jpg")))
            
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
            
            Str_SesionT = askstring('Duration', 'Insert the video duration (min)')
            Tiempo_Sesion = int(Str_SesionT)*60
            
            Arr_TiempoReal = np.zeros(4)
            
            fourcc = cv2.VideoWriter_fourcc(*'MP4V')
            out = cv2.VideoWriter(Name_Video + '.mp4',fourcc, 30.0, (640,480))
            
            
            while(Tiempo_Sesion >= Arr_TiempoReal[3]):
                Arr_TiempoReal[0]=time.time() 
                ret, Img_WebCam = Dev_WebCam_Read.read()
                
                if ret==True:
                    out.write(Img_WebCam)
                    
                    cv2.imshow('Video',Img_WebCam)
                    cv2.moveWindow('Video', int(aux_width_monitor*1.5), int(aux_height_monitor*1.5))
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
                
                Arr_TiempoReal[1]=time.time()
                Arr_TiempoReal[2]=Arr_TiempoReal[1]-Arr_TiempoReal[0] 
                Arr_TiempoReal[3]+= Arr_TiempoReal[2]
                    
        
            Dev_WebCam_Read.release()
            out.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Finalized", "Video has been saved")
        
        def Fun_Cut_Video():
            global Dir_Proyecto
            Ruta_Video = filedialog.askopenfilename(initialdir = Dir_Videos,
                                                    title = "Select Video",
                                                    filetypes = (("mp4 files","*.mp4"),
                                                    ("all files","*.*")))
            
            Ruta_Carpeta_Proyecto =  filedialog.asksaveasfilename(initialdir = Dir_Proyecto,
                                                                                title = "Save image project",
                                                                                filetypes = (("all files","*.*"),
                                                                                ("jpeg files","*.jpg")))
            
            Ruta_Carpeta_Proyecto = Ruta_Carpeta_Proyecto
            Carpeta_Imagenes = '/Images/'
            
            if os.path.exists(Ruta_Carpeta_Proyecto):
                os.path.exists(Ruta_Carpeta_Proyecto)
                os.mkdir(Ruta_Carpeta_Proyecto+Carpeta_Imagenes)
            else:
                os.mkdir(Ruta_Carpeta_Proyecto)
                os.mkdir(Ruta_Carpeta_Proyecto+Carpeta_Imagenes)
                
            Captura_Video = cv2.VideoCapture(Ruta_Video)    
            Rate_Video = round(Captura_Video.get(5))

            Win_Establecer_Rate = tkinter.Tk()
            Win_Establecer_Rate.config(width=400, height=400)
            Win_Establecer_Rate.geometry('700x230+0+0') 
            Win_Establecer_Rate.title('Video Capture')
            Win_Establecer_Rate.config(bg = Fun_Rgb(C_Pal5))
            
            Win_Establecer_Rate_Can = Canvas(Win_Establecer_Rate, width=700, height=230, bg=Fun_Rgb(C_Pal5))
            Win_Establecer_Rate_Can.create_rectangle(10, 10, 690, 220, outline=Fun_Rgb(C_Pal3), width=2)
            Win_Establecer_Rate_Can.create_rectangle(40, 40, 530, 95, outline=Fun_Rgb(C_Pal3), width=2)
            Win_Establecer_Rate_Can.create_rectangle(40, 130, 530, 200, outline=Fun_Rgb(C_Pal3), width=2)
            Win_Establecer_Rate_Can.place(x=0,y=0) 

            Lbl_Win_Establecer_Text_1 = tkinter.Label(Win_Establecer_Rate, bg = Fun_Rgb(C_Pal5), 
                                                      fg = Fun_Rgb(C_Pal2), text = 'Frames per second in the video:  ' + str(Rate_Video))
            Lbl_Win_Establecer_Text_1.config(font = (Font_1,16))
            Lbl_Win_Establecer_Text_1.place(x=60, y = 50)
            
            Lbl_Win_Establecer_Text_2 = tkinter.Label(Win_Establecer_Rate, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Select the number of frames per\n'+' second you want to analyze: ')
            Lbl_Win_Establecer_Text_2.config(font = (Font_1,16))
            Lbl_Win_Establecer_Text_2.place(x=60, y = 140)

            def Fun_Cortar():         
                if int(Lbl_Win_Establecer_TextBox_1.get('1.0','end-1c')) > int(Rate_Video):
                    messagebox.showerror("Error", "Frames per second must not exceed original video frames")
                    Win_Establecer_Rate.destroy()
                else:
                    Aux_Ent_Frame = round(Rate_Video/int(Lbl_Win_Establecer_TextBox_1.get('1.0','end-1c')))
                    Aux_Ent_Frame_2 = int(Lbl_Win_Establecer_TextBox_1.get('1.0','end-1c'))
                    Aux_Contador = 1
                    while(Captura_Video.isOpened()):
                        Id_Frame = Captura_Video.get(1)
                        ret, Frame = Captura_Video.read()
                        if (Aux_Contador == Aux_Ent_Frame):
                            Ruta_Frame = Ruta_Carpeta_Proyecto + Carpeta_Imagenes+ "/image_" +  str(int(Id_Frame)) + ".jpg"
                            cv2.imwrite(Ruta_Frame, Frame)
                            Aux_Contador = 1
                            if (ret != True):
                                break
                        else:
                            Aux_Contador += 1
                            if (ret != True):
                                break
                    Captura_Video.release()
                    def sorted_aphanumeric(data):
                            convert = lambda text: int(text) if text.isdigit() else text.lower()
                            alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
                            return sorted(data, key=alphanum_key)
            
                    List_Contenido = sorted_aphanumeric(os.listdir(Ruta_Carpeta_Proyecto+Carpeta_Imagenes))
                    i = len(List_Contenido)-1
                    Ultimo_Archivo_List_Contenido=List_Contenido[i]
                    os.remove(Ruta_Carpeta_Proyecto+Carpeta_Imagenes+Ultimo_Archivo_List_Contenido)
                    Win_Establecer_Rate.destroy()
                    
                    Archivo_Frames = open(Ruta_Carpeta_Proyecto + "/Frames" + '.txt','w')
                    Archivo_Frames.write(str(1/Aux_Ent_Frame) + '_' + str(Aux_Ent_Frame_2))
                    Archivo_Frames.close()
                    messagebox.showinfo("Finalized", "Video has been cut")
                
            Lbl_Win_Establecer_TextBox_1 = tkinter.Text(Win_Establecer_Rate,width = 5, height = 1)
            Lbl_Win_Establecer_TextBox_1.config(font = (Font_1,18))
            Lbl_Win_Establecer_TextBox_1.place(x=450, y = 151.5)    
            Lbl_Win_Establecer_TextBox_1.insert('end',str(round(Rate_Video/30)))  
            
            Btn_Win_Establecer = tkinter.Button(Win_Establecer_Rate,  bd=0, fg = Fun_Rgb(C_Pal5),
                                              bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                              highlightbackground=Fun_Rgb(C_Pal5),
                                              text = 'Accept', command = Fun_Cortar)
            Btn_Win_Establecer.config(font = (Font_1,20))
            Btn_Win_Establecer.place(x=570, y=151.5)
            
            Win_Establecer_Rate.mainloop()
        
            
        def Fun_Get_RGB():
            global Dir_Proyecto
            Main_Dir_Image = filedialog.askopenfilename(initialdir = Dir_Proyecto,
                                                        title = "Select Image",
                                                        filetypes = (("jpg files","*.jpg"),
                                                                      ("all files","*.*"))) 
            Get_Image = mpimg.imread(Main_Dir_Image)
            imgplot = plt.imshow(Get_Image)
#            imgplot.window.setGeometry(10,10,250, 250)
            plt.show()
            

        def Fun_Track_Video():
            
            global Seleccion_Track, Ruta_Imagen, Dialog_Video_File_Aux, Ruta_Proyecto, Ruta_Video, Carpeta_Imagenes, Ruta_Carpeta_Imagenes, Nombre_Archivo, Img_Original_2
            
            Seleccion_Track = 1
            
            Ruta_Imagen = filedialog.askopenfilename(initialdir=Dir_Proyecto,
                                                     title="Select Image",
                                                     filetypes=(("jpg files","*.jpg"),
                                                     ("all files","*.*")))
            
            Dialog_Video_File_Aux = Ruta_Imagen.replace(Ruta_Imagen.split('/')[(np.size(Ruta_Imagen.split('/')))-1], 'Aux_Image.jpg')
            Ruta_Proyecto = Dir_Proyecto
            Len_Ruta_Proyecto = len(Ruta_Proyecto)
            posicionCarpeta = (Ruta_Imagen[Len_Ruta_Proyecto:].find('/'))
            Ruta_Video = Ruta_Imagen[:Len_Ruta_Proyecto+posicionCarpeta]
            Carpeta_Imagenes ='/Images/'
            Ruta_Carpeta_Imagenes = Ruta_Video + Carpeta_Imagenes
            Nombre_Archivo = Ruta_Imagen.split('/')[(np.size(Ruta_Imagen.split('/')))-3]
            
            Img_Original= Image.open(Ruta_Imagen)
            if int(Img_Original.size[0])>=Var_Tamaño_Lbl_X:
                Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))), 
                                Image.ANTIALIAS)
                if int(Img_Original_2.size[1]) >= Var_Tamaño_Lbl_Y:
                    Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y), 
                                Image.ANTIALIAS)
            elif int(Img_Original.size[1])>=Var_Tamaño_Lbl_Y:
                Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y), 
                                                Image.ANTIALIAS)
                if int(Img_Original_2.size[0]) >= Var_Tamaño_Lbl_X:
                    Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))), 
                                                    Image.ANTIALIAS)
            else:
                Img_Original_2 = Img_Original
                    
            global Lbl_Img_Original, Lbl_Img_Original_Aux
            Photo_Img_Original = ImageTk.PhotoImage(Img_Original_2)
            Lbl_Img_Original = tkinter.Label(Win_Cortar_Imagen_Can, image=Photo_Img_Original, bg = Fun_Rgb(C_Pal5), bd = 0)
            Lbl_Img_Original.image = Photo_Img_Original 
            Lbl_Img_Original.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*1.5)+1)
            Lbl_Img_Original_Aux = tkinter.Label()
            
        def Fun_Nuevo_Proyecto_Vivo():
            
            global Seleccion_Track, Dialog_Video_File, Ruta_Proyecto, Ruta_Video, Carpeta_Imagenes, Ruta_Carpeta_Imagenes, Nombre_Archivo, Ruta_Imagen
            
            Seleccion_Track = 2
            
            Dialog_Video_File = filedialog.asksaveasfilename(initialdir = Dir_Proyecto,
                                                             title = "Guardar archivo",
                                                             filetypes = (("all files","*.*"), ("jpeg files","*.jpg")))
            Ruta_Proyecto = Dir_Proyecto
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
            
            Img_Original= Image.open(Ruta_Imagen)
            if int(Img_Original.size[0])>Var_Tamaño_Lbl_X:
                Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))), 
                                Image.ANTIALIAS)
                if int(Img_Original_2.size[1]) > Var_Tamaño_Lbl_Y:
                    Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y), 
                                Image.ANTIALIAS)
            elif int(Img_Original.size[1])>Var_Tamaño_Lbl_Y:
                Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y), 
                                                Image.ANTIALIAS)
                if int(Img_Original_2.size[0]) > Var_Tamaño_Lbl_X:
                    Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))), 
                                                    Image.ANTIALIAS)
            else:
                Img_Original_2 = Img_Original        
            
            photo = ImageTk.PhotoImage(Img_Original_2)
            global Lbl_Img_Original, Lbl_Img_Original_Aux
            Lbl_Img_Original_Aux = tkinter.Label()
            Lbl_Img_Original = tkinter.Label(image=photo, bg = Fun_Rgb(C_Pal5), bd = 0)
            Lbl_Img_Original.image = photo
            Lbl_Img_Original.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*1.5)+1)
            
            def Fun_Borrar_Y_Tomar_Nueva():
                os.remove(Ruta_Carpeta_Imagenes+'Image_1.jpg')
                global Lbl_Img_Original, Lbl_Img_Original_Aux
                Lbl_Img_Original_Aux.place_forget()
                
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
                
                Img_Original= Image.open(Ruta_Imagen)
                if int(Img_Original.size[0])>Var_Tamaño_Lbl_X:
                    Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))), 
                                    Image.ANTIALIAS)
                    if int(Img_Original_2.size[1]) > Var_Tamaño_Lbl_Y:
                        Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y), 
                                    Image.ANTIALIAS)
                elif int(Img_Original.size[1])>Var_Tamaño_Lbl_Y:
                    Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y), 
                                                    Image.ANTIALIAS)
                    if int(Img_Original_2.size[0]) > Var_Tamaño_Lbl_X:
                        Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))), 
                                                        Image.ANTIALIAS)
                else:
                    Img_Original_2 = Img_Original         
                
                photo = ImageTk.PhotoImage(Img_Original_2)
                Lbl_Img_Original_Aux = tkinter.Label()
                Lbl_Img_Original = tkinter.Label(image=photo, bg = Fun_Rgb(C_Pal5), bd = 0)
                Lbl_Img_Original.image = photo
                Lbl_Img_Original.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*1.5)+1)
                
                mensaje1 =messagebox.askyesno(message= 'Take another picture?', title="Picture")
                if mensaje1==True:
                    Lbl_Img_Original_Aux.place_forget()
                    Lbl_Img_Original.place_forget()
                    Fun_Borrar_Y_Tomar_Nueva()
             
            mensaje1 =messagebox.askyesno(message="Take another picture?", title="Picture")
            if mensaje1==True:
                Lbl_Img_Original_Aux.place_forget()
                Lbl_Img_Original.place_forget()
                Fun_Borrar_Y_Tomar_Nueva()
                
        def Fun_Abrir_Proyecto_Vivo():
            global Seleccion_Track
            Seleccion_Track = 3
            Fun_Iniciar_Track()
          
        Menu_Informacion = tkinter.Menu(Win_Cortar_Imagen)
        
        Submenu_Archivo = tkinter.Menu(Menu_Informacion, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                                       activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Black),
                                       tearoff=0)
        Submenu_Archivo.add_command(label='Open video', command = Fun_Open_Video)
        Submenu_Archivo.add_command(label='Record video', command = Fun_Take_video)
        Submenu_Archivo.add_command(label='Video to Frames', command = Fun_Cut_Video)
        Submenu_Archivo.add_command(label='Video project', command = Fun_Track_Video)
        Submenu_Archivo.add_command(label='Live set up', command = Fun_Nuevo_Proyecto_Vivo)
        Submenu_Archivo.add_command(label='Live project', command = Fun_Abrir_Proyecto_Vivo)
        Submenu_Archivo.add_command(label='RGB', command = Fun_Get_RGB)
        Menu_Informacion.add_cascade(label='File', menu=Submenu_Archivo)
         
        Submenu_Configuracion = tkinter.Menu(Menu_Informacion, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                                             activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Black),
                                             tearoff=0)
        
        Submenu_Camara = tkinter.Menu(Submenu_Configuracion, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                                      activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Black),
                                      tearoff=0)
        Submenu_Camara.add_command(label="WebCam 1", command = Fun_Cam_Frontal)
        Submenu_Camara.add_command(label="WebCam 2", command = Fun_Otra_Camara)
        Submenu_Configuracion.add_cascade(label='Select', menu=Submenu_Camara)
        
        Submenu_Resolucion = tkinter.Menu(Submenu_Configuracion, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                                          activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Black),
                                          tearoff=0)
        Submenu_Resolucion.add_command(label="320x200", command = Fun_Res_320x200)
        Submenu_Resolucion.add_command(label="480x320", command = Fun_Res_480x320)
        Submenu_Resolucion.add_command(label="600x480", command = Fun_Res_600x480)
        Submenu_Resolucion.add_command(label="800x600", command = Fun_Res_800x600)
        Submenu_Resolucion.add_command(label="1280x800", command = Fun_Res_1280x800)
        Submenu_Configuracion.add_cascade(label='Resolution', menu=Submenu_Resolucion)
        
        Menu_Informacion.add_cascade(label="WebCam", menu=Submenu_Configuracion)
         
        #Menu_Informacion.add_command(label="Help", command=Fun_Ayuda)
        
        Win_Cortar_Imagen.config(menu=Menu_Informacion)
    
        def Fun_Imagen():
            
            if Seleccion_Track == 0:
                messagebox.showinfo("Error", "Select a traking option")

            X1 = Slider_X1.get()
            X2 = Slider_X2.get()
            Y1 = Slider_Y1.get()
            Y2 = Slider_Y2.get()
            Rotar = Slider_Grados_Rotar.get()
            
            global Lbl_Img_Original, Lbl_Img_Original_Aux, Dialog_Video_File_Aux_2
            Lbl_Img_Original.place_forget()
            Lbl_Img_Original_Aux.place_forget()
            
            Img_Original = imageio.imread(Ruta_Imagen)
            Img_Original = Img_Original[round(Img_Original.shape[0]*Y1):round(Img_Original.shape[0]*Y2),
                                        round(Img_Original.shape[1]*X1):round(Img_Original.shape[1]*X2)]
        
            imageio.imsave(Dialog_Video_File_Aux, Img_Original)
            Img_Aux = Image.open(Dialog_Video_File_Aux).rotate(Rotar)
            
            Img_Original_2 = Img_Aux
            if int(Img_Aux.size[0])>Var_Tamaño_Lbl_X:
                Img_Original_2 = Img_Aux.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Aux.size[0]))*int(Img_Aux.size[1]))), 
                                Image.ANTIALIAS)
                if int(Img_Original_2.size[1]) > Var_Tamaño_Lbl_Y:
                    Img_Original_2 = Img_Aux.resize((round((Var_Tamaño_Lbl_Y/int(Img_Aux.size[1]))*int(Img_Aux.size[0])),Var_Tamaño_Lbl_Y), 
                                Image.ANTIALIAS)
            elif int(Img_Aux.size[1])>Var_Tamaño_Lbl_Y:
                Img_Original_2 = Img_Aux.resize((round((Var_Tamaño_Lbl_Y/int(Img_Aux.size[1]))*int(Img_Aux.size[0])),Var_Tamaño_Lbl_Y), 
                                                Image.ANTIALIAS)
                if int(Img_Original_2.size[0]) > Var_Tamaño_Lbl_X:
                    Img_Original_2 = Img_Aux.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Aux.size[0]))*int(Img_Aux.size[1]))), 
                                                    Image.ANTIALIAS)
                    
            Img_Aux.save(Dialog_Video_File_Aux)
            
            Photo_Img_Aux = ImageTk.PhotoImage(Img_Original_2)
            Lbl_Img_Original_Aux = tkinter.Label(image=Photo_Img_Aux, bg = Fun_Rgb(C_Pal5), bd = 0)
            Lbl_Img_Original_Aux.image = Photo_Img_Aux 
            Lbl_Img_Original_Aux.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*1.5)+1)
        
        def Fun_Editar_Imagen():
            
            if Seleccion_Track == 0:
                messagebox.showinfo("Error", "Select a traking option")
            
            Var_R = Slider_Rojo.get()
            Var_G = Slider_Verde.get()
            Var_B = Slider_Azul.get()
            Var_Des = Slider_Desviacion.get()
            Var_Umbral = float(Entr_Umbral.get())
            Mat_RGB = ([Var_R, Var_G, Var_B, Var_Des, Var_Umbral])
            Img_Filtro = Var_Filtro.get()
            Track_MinSize = float(Entr_Valor_Minimo_Animal.get())
            
            global Lbl_Img_Original, Lbl_Img_Original_Aux
            Lbl_Img_Original.place_forget()
            Lbl_Img_Original_Aux.place_forget()
            
            global Dialog_Video_File_Aux_2
            Dialog_Video_File_Aux_2 = Dialog_Video_File_Aux.replace('Aux_Image', 'Aux_Imagee')
            
            Img_Cortable = imageio.imread(Dialog_Video_File_Aux)
            Img_Cortable_Aux = Img_Cortable[:, :]
            imageio.imsave(Dialog_Video_File_Aux_2, Img_Cortable_Aux)
            Img_WebCam = np.copy(Img_Cortable_Aux)
            
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

            imageio.imsave(Dialog_Video_File_Aux_2, Img_WebCam)
            Img_Cortable_Aux = Image.open(Dialog_Video_File_Aux_2)
            
            Img_Original_2 = Image.open(Dialog_Video_File_Aux_2)
            if int(Img_Cortable_Aux.size[0])>Var_Tamaño_Lbl_X:
                Img_Original_2 = Img_Cortable_Aux.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Cortable_Aux.size[0]))*int(Img_Cortable_Aux.size[1]))), 
                                Image.ANTIALIAS)
                if int(Img_Original_2.size[1]) > Var_Tamaño_Lbl_Y:
                    Img_Original_2 = Img_Cortable_Aux.resize((round((Var_Tamaño_Lbl_Y/int(Img_Cortable_Aux.size[1]))*int(Img_Cortable_Aux.size[0])),Var_Tamaño_Lbl_Y), 
                                Image.ANTIALIAS)
            elif int(Img_Cortable_Aux.size[1])>Var_Tamaño_Lbl_Y:
                Img_Original_2 = Img_Cortable_Aux.resize((round((Var_Tamaño_Lbl_Y/int(Img_Cortable_Aux.size[1]))*int(Img_Cortable_Aux.size[0])),Var_Tamaño_Lbl_Y), 
                                                Image.ANTIALIAS)
                if int(Img_Original_2.size[0]) > Var_Tamaño_Lbl_X:
                    Img_Original_2 = Img_Cortable_Aux.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Cortable_Aux.size[0]))*int(Img_Cortable_Aux.size[1]))), 
                                                    Image.ANTIALIAS)
            
            #Guardar_Axuliar_2
            Img_Cortable_Aux.save(Dialog_Video_File_Aux_2)   
            
            #Mostrar Imagen
            Pho_Img_Cortable_Aux = ImageTk.PhotoImage(Img_Original_2)
            Lbl_Parametros_Aux = tkinter.Label(image=Pho_Img_Cortable_Aux, bg = Fun_Rgb(C_Pal5), bd = 0)
            Lbl_Parametros_Aux.image = Pho_Img_Cortable_Aux 
            Lbl_Parametros_Aux.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*1.5)+1)
       
        #%% Fun_Editar_Todas_Imagenes
        def Fun_Editar_Todas_Imagenes():
            
            if Seleccion_Track == 0:
                messagebox.showinfo("Error", "Select a traking option")
            
            global Mat_RGB, number_subject
            
            plt.rcParams['image.cmap'] = 'gray'
            X1 = Slider_X1.get()
            X2 = Slider_X2.get()
            Y1 = Slider_Y1.get()
            Y2 = Slider_Y2.get()
            Rotar = Slider_Grados_Rotar.get()
            Dev_Espacio_Tamano = Etr_Tamano_Caja.get()
            Img_Filtro = Var_Filtro.get()
            Track_MinSize = float(Entr_Valor_Minimo_Animal.get())
            os.remove(Dialog_Video_File_Aux)
            os.remove(Dialog_Video_File_Aux_2)
            
            if number_subject == 0:
                Var_R = Slider_Rojo.get()
                Var_G = Slider_Verde.get()
                Var_B = Slider_Azul.get()
                Var_Des = Slider_Desviacion.get()
                Var_Umbral = float(Entr_Umbral.get())
                Mat_RGB = ([Var_R, Var_G, Var_B, Var_Des, Var_Umbral])
            
            #Imagenes
            def sorted_aphanumeric(data):
                convert = lambda text: int(text) if text.isdigit() else text.lower()
                alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
                return sorted(data, key=alphanum_key)
            List_Contenido = sorted_aphanumeric(os.listdir(Ruta_Carpeta_Imagenes))
           
            if number_subject == 0:
                #Remplazar Imagenes
                for elemento in List_Contenido:
                    ruta = Ruta_Carpeta_Imagenes
                    documento = ruta + elemento
                    
                    Img_Original = imageio.imread(documento)/255.0
                    Img_Original = Img_Original[round(Img_Original.shape[0]*Y1):round(Img_Original.shape[0]*Y2),
                                    round(Img_Original.shape[1]*X1):round(Img_Original.shape[1]*X2)]
                    imageio.imsave(documento, Img_Original)
                    Img_Original = Image.open(documento).rotate(Rotar)
            
                    Img_WebCam = np.copy(Img_Original)
                    imageio.imsave(documento, Img_WebCam)
                
                if Seleccion_Track == 1:
                    messagebox.showinfo("Finalized", "Images have been edited")
                elif Seleccion_Track == 2:
                    messagebox.showinfo("Finalized", "Parameters have been saved")
                elif Seleccion_Track == 3:
                    messagebox.showinfo("Finalized", "Open Parameters")
                
                #Guardar txt
                Arr_Variables = [str(Seleccion_Camara), str(Seleccion_Resolucion),
                                 str(X1), str(X2), str(Y1), str(Y2), str(Rotar), 
                                 str(Dev_Espacio_Tamano), str(Var_R), str(Var_G), str(Var_B),
                                 str(Var_Des), str(Var_Umbral), str(Img_Filtro), 
                                 str(Track_MinSize), 
                                 str(Img_WebCam.shape[1]),str(Img_WebCam.shape[0]), str(number_subject)]      
                
                Archivo_Variables = open(Ruta_Video + '/' + 'Config_' + Nombre_Archivo +'.txt','w')
                for i in Arr_Variables:
                    Archivo_Variables.write(i +'\n')
                Archivo_Variables.close()
           
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
                    ruta = Ruta_Carpeta_Imagenes
                    documento = ruta + elemento
                    
                    Img_Original = imageio.imread(documento)/255.0
                    Img_Original = Img_Original[round(Img_Original.shape[0]*Y1):round(Img_Original.shape[0]*Y2),
                                    round(Img_Original.shape[1]*X1):round(Img_Original.shape[1]*X2)]
                    imageio.imsave(documento, Img_Original)
                    Img_Original = Image.open(documento).rotate(Rotar)
            
                    Img_WebCam = np.copy(Img_Original)
                    imageio.imsave(documento, Img_WebCam)
                
                if Seleccion_Track == 1:
                    messagebox.showinfo("Finalized", "Images have been edited")
                elif Seleccion_Track == 2:
                    messagebox.showinfo("Finalized", "Parameters have been saved")
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
                
                Archivo_Variables = open(Ruta_Video + '/' + 'Config_' + Nombre_Archivo +'.txt','w')
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
        
        #%% Iniciar Track
        def Fun_Iniciar_Track():
            if Seleccion_Track == 0:
                messagebox.showinfo("Error", "Select a traking option")
            
            #%%Track Imagenes --- 1
            if Seleccion_Track == 1:
                
                #Seleccionar Archivo
                Direccion_Documento = filedialog.askopenfilename(initialdir = Dir_Proyecto,
                                                                       title = "Seleccionar archivo",
                                                                       filetypes = (("txt files","*.txt"),
                                                                                    ("all files","*.*")))
                
                def Ventana_Sesion():
                    Win_Cortar_Imagen.destroy()
                    #Variables
                    global Str_SesionT, Str_Sujeto, Str_Sesion, Str_Grupo
                    Str_SesionT = '0'
                    Str_Sujeto = '0'
                    Str_Sesion = '0'
                    Str_Grupo = '0'
                    
                    Main_Ses = tkinter.Tk()
                    Main_Ses.title('Run experiment')
                    Main_Ses.geometry(str(int(aux_width_monitor*8))+'x'+str(height_monitor-100)+'+0+0')
                    Main_Ses.configure(background=Fun_Rgb(C_Pal5))
                    
                    Main_Ses_Can = Canvas(Main_Ses, width=round(aux_width_monitor*8), height=round(height_monitor-100), bg=Fun_Rgb(C_Pal5))
                    Main_Ses_Can.create_rectangle(10, 10, aux_width_monitor*8 -10, height_monitor-110, outline=Fun_Rgb(C_Pal3), width=4)
                    Main_Ses_Can.create_rectangle(120, 250, 520, 650, fill=Fun_Rgb(C_Black), outline=Fun_Rgb(C_Pal6), width=2)
                    Main_Ses_Can.place(x=0,y=0) 
              
                    def Fun_Bnt_Next():
                        
                        global Str_SesionT, Str_Sujeto, Str_Sesion, Str_Grupo, Nombre_Archivo,  Ruta_Video, Ruta_Carpeta_Imagenes, Ruta_Carpeta_Imagenes, Ruta_Archivo_Parametros
                        
                        Str_Sujeto = Lbl_Sujeto_TextBox_1.get('1.0','end-1c')
                        Str_Sesion = Lbl_Sesion_TextBox_1.get('1.0','end-1c')
                        Str_Grupo = Lbl_Grupo_TextBox_1.get('1.0','end-1c')
                        
                        Ruta_Archivo_Parametros = Ruta_Video + '/Config_' + Nombre_Archivo+'.txt'
                        Ruta_Archivo_Frames = Ruta_Video + '/Frames.txt'
                        
                        def sorted_aphanumeric(data):
                                    convert = lambda text: int(text) if text.isdigit() else text.lower()
                                    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
                                    return sorted(data, key=alphanum_key)
                        List_Contenido = sorted_aphanumeric(os.listdir(Ruta_Carpeta_Imagenes))
                        
                        Dir_Archivo_Parametros =open(Ruta_Archivo_Parametros,'r')  
                        Arr_Parametros_Imagen = Dir_Archivo_Parametros.read().split('\n')    
                        Track_MinSize = float(Arr_Parametros_Imagen[14]) 
                        Dev_Espacio_Tamano = int(Arr_Parametros_Imagen[7])
                        number_subject = int(Arr_Parametros_Imagen[17])
                        Size_Proportion = int(Arr_Parametros_Imagen[15])
                        Dir_Archivo_Parametros.close()
                        
                        Dir_Archivo_Frames = open(Ruta_Archivo_Frames, 'r')
                        Temp_Int_Frame = Dir_Archivo_Frames.read().split('\n')
                        Temp_Int_Frame = str(Temp_Int_Frame)[2:-2]
                        Int_Frame, Int_Frame_2 = Temp_Int_Frame.split('_')
                        Dir_Archivo_Frames.close()
                                
                        global Mat_Datos
                        Int_Contador = 1
                        Int_Datos_Consecuencia = 0
                        Mat_Datos = np.zeros((9999999,6+(number_subject*2)))
                        
                        
                        if number_subject > 0: 
                            global Mat_Datos_X, Mat_Datos_Y, Mat_Datos_D, Mat_RGB 
                            Mat_Datos_X = np.zeros((9999999,16))
                            Mat_Datos_Y = np.zeros((9999999,16))
                            Mat_Datos_D = np.zeros((9999999,16))
                    
                            Mat_RGB = np.zeros((number_subject, 6))
                            aux_1 = 0
                            f = 0
                            for i in Arr_Parametros_Imagen:
                                b = i
                                aux_1 += 1
                                if aux_1 == 9:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][0] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 10:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][1] = e
                                        f += 1
                                    f = 0   
                                if aux_1 == 11:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][2] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 12:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][3] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 13:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][4] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 14:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][5] = e
                                        f += 1
                                    f = 0
                            
                        else:
                            Mat_RGB = ([int(Arr_Parametros_Imagen[8]), int(Arr_Parametros_Imagen[9]), int(Arr_Parametros_Imagen[10]),
                                        int(Arr_Parametros_Imagen[11]), float(Arr_Parametros_Imagen[12])])
                            Img_Filtro = int(Arr_Parametros_Imagen[13]) 
                        
                        def Fun_Distancia(x1,x2,y1,y2,DistanciaRelativa):
                            return math.sqrt((x2-x1)**2+(y2-y1)**2)*DistanciaRelativa
                        
                        if number_subject == 0:

                            for elemento in List_Contenido:
                                
                                ruta = Ruta_Carpeta_Imagenes
                                documento = ruta + elemento
                                Img_Original = imageio.imread(documento)/255.0
                                Img_Original = Image.open(documento)
                                Img_WebCam = np.copy(Img_Original)
                                
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
                        
                                try:
                                    Mat_Centroide = ndimage.label(Img_WebCam)[0]
                                    Centroide = scipy.ndimage.measurements.center_of_mass(Img_WebCam, Mat_Centroide, [1])
                                    Mat_Size = ndimage.label(Img_WebCam)[0]
                                    Size = np.sqrt(scipy.ndimage.measurements.sum(Img_WebCam, Mat_Size, [1]))
                                    MinSize = int(np.where(Size == np.min(Size[(Size >= Track_MinSize)]))[0])
                                    cv2.circle(Img_WebCam,(int(Centroide[MinSize][1]),int(Centroide[MinSize][0])),2,(0,0,255),5)
                                except:
                                    Img_WebCam = Img_WebCam
                                    
                                Img_WebCam = cv2.resize(Img_WebCam,(400, round((400/Img_WebCam.shape[1])*Img_WebCam.shape[1])))
                                cv2.putText(Img_WebCam,'T: ',(5,15),Font_CV, .5,(255,255,255),1)
                                cv2.putText(Img_WebCam,str(round(Mat_Datos[Int_Contador-1][0] ,2)),(20,15),Font_CV, .5,(255,255,255),1)
                                cv2.imshow('Tracking',Img_WebCam)
                                cv2.moveWindow('Tracking', 120,250);
                                cv2.waitKey(5)
                                
                                Mat_Datos[Int_Contador][0] = (int(elemento.replace('image_','').replace('.jpg',''))/int(Int_Frame_2)) * float(Int_Frame)  
                                try:
                                    Mat_Datos[Int_Contador][1] = int(Centroide[MinSize][1])
                                    Mat_Datos[Int_Contador][2] = int(Centroide[MinSize][0])
                                except:
                                    Mat_Datos[Int_Contador][1] = Mat_Datos[Int_Contador-1][1]
                                    Mat_Datos[Int_Contador][2] = Mat_Datos[Int_Contador-1][2]
                                Mat_Datos[Int_Contador][4] = Int_Datos_Consecuencia
                                Mat_Datos[Int_Contador][3] = (Fun_Distancia(Mat_Datos[Int_Contador-1][1],Mat_Datos[Int_Contador][1],Mat_Datos[Int_Contador-1][2],Mat_Datos[Int_Contador][2],Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])))
                                Mat_Datos[Int_Contador][5] = (Mat_Datos[Int_Contador][3]/100) / float(Int_Frame)
                                Int_Contador += 1 
                                
                            cv2.destroyAllWindows()
                            
                            Mat_Datos = np.delete(Mat_Datos,np.where(Mat_Datos[:,1] == 0), axis=0) 
                            Mat_Datos[0,3] = 0
                            Mat_Datos[0,5] = 0
                                                              
                            Nombre_Grafico =  filedialog.asksaveasfilename(initialdir = Dir_Datos,
                                                                                         title = "Save Data",
                                                                                         filetypes = (("all files","*.*"), ("txt files","*.txt"))) 
                            i = 1
                            Archivo_Mat_Datos = open(Nombre_Grafico + '.txt','w')
                            Archivo_Mat_Datos.write('Subject: ' + Str_Sujeto + '\n' +
                                                    'Session: ' + Str_Sesion + '\n' +
                                                    'Group: ' + Str_Grupo + '\n' +
                                                    'Time: '+ str(round(max(Mat_Datos[:,0]),3)) + '\n' +
                                                    '# Consecuences: ' + str(np.size(np.where(Mat_Datos[:,4] == 1))) + '\n' +
                                                    'Distance: ' + str(round(sum(Mat_Datos[:,3]),3)) + 'cm' + '\n' +
                                                    'Velocity: ' + str(round(sum(Mat_Datos[:,3])/max(Mat_Datos[:,0]),3)) + 'cm/seg' + '\n' +
                                                    'Mean Aceleration: ' + str(round(statistics.mean(Mat_Datos[:,5]),3)) + 'm/seg' + '\n' +
                                                    '\n' + 'Frame;Time;X;Y;Aceleration;Distance;Consecuences' + '\n')
                            for i in range(0,len(Mat_Datos)): 
                                Archivo_Mat_Datos.write(str(i) + ',' + str(round(Mat_Datos[i][0],3)) +
                                                                 ',' + str(round(Mat_Datos[i][1] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])),3)) +
                                                                 ',' + str(round(Mat_Datos[i][2] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[16])),3)) +
                                                                 ',' + str(round(Mat_Datos[i][5],3)) +
                                                                 ',' + str(round(Mat_Datos[i][3],3)) +
                                                                 ',' + str(Mat_Datos[i][4]) + '\n')
                            Archivo_Mat_Datos.close() 
                            if Seleccion_Track == 1:
                                messagebox.showinfo("Finalized", "Video has been traked")
                            Main_Ses.destroy()
                            
                            
                        else:
                            for elemento in List_Contenido:
                                ruta = Ruta_Carpeta_Imagenes
                                documento = ruta + elemento
                                
                                Img_Original = imageio.imread(documento)/255
                                Img_Original = Image.open(documento)
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
                        
                                    if Mat_RGB[i][5]==1:
                                        image_aux = ndimage.gaussian_filter(image_aux, sigma=3)
                                    elif Mat_RGB[i][5]==2:
                                        image_aux = ndimage.gaussian_filter(image_aux, sigma=5)
                                    elif Mat_RGB[i][5]==3:
                                        image_aux =ndimage.uniform_filter(image_aux, size=2)
                                    elif Mat_RGB[i][5]==4:
                                        image_aux =ndimage.uniform_filter(image_aux, size=11)
                                    elif Mat_RGB[i][5]==5:
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
                                    Mat_Datos_D[Int_Contador][i] = (Fun_Distancia(Mat_Datos_X[Int_Contador-1][i],Mat_Datos_X[Int_Contador][i],Mat_Datos_Y[Int_Contador-1][i],Mat_Datos_Y[Int_Contador][i],Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])))    
                                                                        
                                    image_total += image_aux
                                    if i == number_subject -1:
                                        j = 0
                                        for j in range(number_subject):
                                            cv2.putText(image_total,str(j+1),(int(Mat_Datos_X[Int_Contador][j])+10,int(Mat_Datos_Y[Int_Contador][j])),Font_CV, .5,(0,0,255),1)
                                        image_total = cv2.resize(image_total,(400, round((400/Img_WebCam.shape[1])*Img_WebCam.shape[1])))
                                        cv2.putText(image_total,'T: ',(5,15),Font_CV, .5,(255,255,255),1)
                                        cv2.putText(image_total,str(round(Mat_Datos[Int_Contador-1][0] ,2)),(20,15),Font_CV, .5,(255,255,255),1)
                                        cv2.imshow('Tracking',image_total)
                                        cv2.moveWindow('Tracking', 120,250);
                                        cv2.waitKey(5)
                                    
                                    Mat_Datos[Int_Contador][0] = (int(elemento.replace('image_','').replace('.jpg',''))/int(Int_Frame_2)) * float(Int_Frame)  
                                        
                                Mat_Datos[Int_Contador][4] = Int_Datos_Consecuencia
                                
                                if cv2.waitKey(1) & 0xFF == ord('q'):
                                    break  
                                
                                Int_Contador += 1   
                                
                            cv2.destroyAllWindows()
                            
                            Mat_Datos = np.delete(Mat_Datos,np.where(Mat_Datos[:,0] == 0), axis=0)
                            Mat_Datos_X = Mat_Datos_X[0:len(Mat_Datos),:]
                            Mat_Datos_Y = Mat_Datos_Y[0:len(Mat_Datos),:]
                            Mat_Datos_D = Mat_Datos_D[0:len(Mat_Datos),:]
                              
                        
                            Nombre_Grafico =  filedialog.asksaveasfilename(initialdir = Dir_Datos,
                                                                         title = "Save Data",
                                                                         filetypes = (("all files","*.*"), ("txt files","*.txt"))) 

                            j = 0
                            for j in range(number_subject):
                                Archivo_Mat_Datos = open(Nombre_Grafico +'_' + str(j+1) + '.txt','w')
                                Archivo_Mat_Datos.write('Subject: ' + Str_Sujeto + '_' + str(j+1) +'\n' +
                                                        'Session: ' + Str_Sesion + '\n' +
                                                        'Group: ' + Str_Grupo + '\n' +
                                                        'Time: '+ str(round(max(Mat_Datos[:,0]),3)) + '\n' +
                                                        '# Consecuences: ' + str(np.size(np.where(Mat_Datos[:,4] == 1))) + '\n' +
                                                        'Distance: ' + str(round(sum(Mat_Datos_D[:,j]),3)) + 'cm' + '\n' +
                                                        'Velocity: ' + str(round(sum((Mat_Datos_D[:,j]/100)/Mat_Datos[:,0]),3)) + 'cm/seg' + '\n' +
                                                        'Mean Aceleration: ' + str(round(statistics.mean((Mat_Datos_D[:,j]/100)/Mat_Datos[:,0]),3)) + 'm/seg' + '\n' +
                                                        '\n' + 'Frame;Time;X;Y;Aceleration;Distance;Consecuences' + '\n')
                                i = 1
                                for i in range(0,len(Mat_Datos)): 
                                    Archivo_Mat_Datos.write(str(i) + ';' + str(round(Mat_Datos[i][0],3)) +
                                                                     ';' + str(round(Mat_Datos_X[i][j] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])),3)) +
                                                                     ';' + str(round(Mat_Datos_Y[i][j] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[16])),3)) +
                                                                     ';' + str(round((Mat_Datos_D[i,j]/100)/float(Int_Frame),3)) +
                                                                     ';' + str(round(Mat_Datos_D[i][j],3)) +
                                                                     ';' + str(Mat_Datos[i][4]) + '\n')

                            if Seleccion_Track == 3:
                                messagebox.showinfo("Finalized", "Sesion has been traked")
                            Main_Ses.destroy()
                    
                    
                    Lbl_Sujeto_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Subject')
                    Lbl_Sujeto_Text_1.config(font = (Font_1,18))
                    Lbl_Sujeto_Text_1.place(x=30, y = 30)
                    
                    Lbl_Sujeto_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
                    Lbl_Sujeto_TextBox_1.config(font = (Font_1,15))
                    Lbl_Sujeto_TextBox_1.place(x=150, y = 35)
                    
                    Lbl_Sesion_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Session')
                    Lbl_Sesion_Text_1.config(font = (Font_1,18))
                    Lbl_Sesion_Text_1.place(x=30, y = 80)
                    
                    Lbl_Sesion_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
                    Lbl_Sesion_TextBox_1.config(font = (Font_1,15))
                    Lbl_Sesion_TextBox_1.place(x=150, y = 85)
                    
                    Lbl_Grupo_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Group')
                    Lbl_Grupo_Text_1.config(font = (Font_1,18))
                    Lbl_Grupo_Text_1.place(x=30, y = 130)
                    
                    Lbl_Grupo_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
                    Lbl_Grupo_TextBox_1.config(font = (Font_1,15))
                    Lbl_Grupo_TextBox_1.place(x=150, y = 135)
                    
                    Bnt_Next = tkinter.Button(Main_Ses, bd=0, fg = Fun_Rgb(C_Pal5),
                                      bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                      highlightbackground=Fun_Rgb(C_Pal5),
                                      text = '  Run  ', command = Fun_Bnt_Next)
                    Bnt_Next.config(font = (Font_1,25))
                    Bnt_Next.place(x=aux_width_monitor*6.1, y = aux_height_monitor*11)

                    
                    Main_Ses.mainloop()

                Ventana_Sesion()           
            
            #%%En vivo --- 2
            if Seleccion_Track == 2:
                messagebox.showinfo("Error", "Select Live project")               
                
                
            #%%Abrir en Vivo--- 3
            if Seleccion_Track == 3:
                
                Direccion_Documento = filedialog.askopenfilename(initialdir = Dir_Proyecto,
                                                               title = "Seleccionar archivo",
                                                               filetypes = (("txt files","*.txt"),
                                                                            ("all files","*.*")))
                def Ventana_Sesion():
                
                    global Str_SesionT, Str_Sujeto, Str_Sesion, Str_Grupo
                    Str_SesionT = '10'
                    Str_Sujeto = '0'
                    Str_Sesion = '0'
                    Str_Grupo = '0'
                    
                    Main_Ses = tkinter.Tk()
                    Main_Ses.title('Run experiment')
                    Main_Ses.geometry(str(int(aux_width_monitor*8))+'x'+str(height_monitor-100)+'+0+0')
                    Main_Ses.configure(background=Fun_Rgb(C_Pal5))
                    
                    Main_Ses_Can = Canvas(Main_Ses, width=round(aux_width_monitor*8), height=round(height_monitor-100), bg=Fun_Rgb(C_Pal5))
                    Main_Ses_Can.create_rectangle(10, 10, aux_width_monitor*8 -10, height_monitor-110, outline=Fun_Rgb(C_Pal3), width=4)
                    Main_Ses_Can.create_rectangle(120, 250, 520, 650, fill=Fun_Rgb(C_Black), outline=Fun_Rgb(C_Pal6), width=2)
                    Main_Ses_Can.place(x=0,y=0) 
                    
                    Win_Cortar_Imagen.destroy()
                    
                    def Fun_Bnt_Next():
                        
                        Dir_Archivo_Parametros =open(Direccion_Documento,'r')  
                        Arr_Parametros_Imagen = Dir_Archivo_Parametros.read().split('\n') 
                        Dir_Archivo_Parametros.close()
                        
                        global number_subject
                        X1 = float(Arr_Parametros_Imagen[2])
                        X2 = float(Arr_Parametros_Imagen[3])
                        Y1 = float(Arr_Parametros_Imagen[4])
                        Y2 = float(Arr_Parametros_Imagen[5])
                        Rotar = float(Arr_Parametros_Imagen[6])
                        Dev_Espacio_Tamano = int(Arr_Parametros_Imagen[7])
                        Track_MinSize = float(Arr_Parametros_Imagen[14])
                        number_subject = int(Arr_Parametros_Imagen[17])
                        Size_Proportion = int(Arr_Parametros_Imagen[15])
                        
                        Dev_WebCam_Resolution = int(Arr_Parametros_Imagen[1])
                        Dev_WebCam_Read = cv2.VideoCapture(int(Arr_Parametros_Imagen[0]))
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
                      
                        global Str_SesionT, Str_Sujeto, Str_Sesion, Str_Grupo
                        Str_SesionT = Lbl_SesionT_TextBox_1.get('1.0','end-1c')
                        Str_Sujeto = Lbl_Sujeto_TextBox_1.get('1.0','end-1c')
                        Str_Sesion = Lbl_Sesion_TextBox_1.get('1.0','end-1c')
                        Str_Grupo = Lbl_Grupo_TextBox_1.get('1.0','end-1c')
                        Var_Save_video = Var_Radiobutton.get()
                        Tiempo_Sesion = int(Str_SesionT)
                        
                        if Var_Save_video != 1:
                            Var_Save_video = 0
                        
                        global Nombre_Archivo, Ruta_Video, Ruta_Carpeta_Imagenes
                        Nombre_Archivo = Str_SesionT
                        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
                        out = cv2.VideoWriter(Dir_Videos + Nombre_Archivo + '.mp4',fourcc, 30.0, (640,480))
                
                        global Mat_Datos
                        Int_Contador = 1
                        Int_Datos_Consecuencia = 0
                        Int_Contador_Distancia = 0
                        Arr_TiempoReal = np.zeros(4)
                        Mat_Datos = np.zeros((9999999,7))
                        Mat_Datos[:,0] = -1
                        
                        def Fun_Distancia(x1,x2,y1,y2,DistanciaRelativa):
                            return math.sqrt((x2-x1)**2+(y2-y1)**2)*DistanciaRelativa
                        
                        global Mat_RGB
                        
                        if number_subject >0:
                            global Mat_Datos_X, Mat_Datos_Y, Mat_Datos_D, Mat_RGB 
                            Mat_Datos_X = np.zeros((9999999,16))
                            Mat_Datos_Y = np.zeros((9999999,16))
                            Mat_Datos_D = np.zeros((9999999,16))
                            
                            Dir_Archivo_Parametros =open(Direccion_Documento,'r')  
                            Arr_Parametros_Imagen = Dir_Archivo_Parametros.read().split('\n')    
                            Track_MinSize = float(Arr_Parametros_Imagen[14]) 
                            Dev_Espacio_Tamano = int(Arr_Parametros_Imagen[7])
                            number_subject = int(Arr_Parametros_Imagen[17])
                            Dir_Archivo_Parametros.close()
                            Mat_RGB = np.zeros((number_subject, 6))
                            aux_1 = 0
                            f = 0
                            for i in Arr_Parametros_Imagen:
                                b = i
                                aux_1 += 1
                                if aux_1 == 9:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][0] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 10:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][1] = e
                                        f += 1
                                    f = 0   
                                if aux_1 == 11:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][2] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 12:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][3] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 13:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][4] = e
                                        f += 1
                                    f = 0
                                if aux_1 == 14:
                                    list_aux = b
                                    c = list_aux.split(';')
                                    c = c[:-1]
                                    for e in c:
                                        Mat_RGB[f][5] = e
                                        f += 1
                                    f = 0
                        else:
                            Mat_RGB = ([int(Arr_Parametros_Imagen[8]), int(Arr_Parametros_Imagen[9]), int(Arr_Parametros_Imagen[10]),
                                        int(Arr_Parametros_Imagen[11]), float(Arr_Parametros_Imagen[12])])
                            Img_Filtro = int(Arr_Parametros_Imagen[13])            
                                        
                        #%%Sesion_Sujetos=1            
                        if number_subject ==0:
                            Arr_TiempoReal[0]=time.time()
                            
                            while(Tiempo_Sesion >= Arr_TiempoReal[3]):
                                
                                ret, Img_WebCam = Dev_WebCam_Read.read()
                                if ret==True and Var_Save_video == 1:
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
                            
                                Img_WebCam = cv2.resize(Img_WebCam,(400, round((400/Img_WebCam.shape[1])*Img_WebCam.shape[1])))
                                cv2.putText(Img_WebCam,'Time: ',(5,15),Font_CV, .5,(255,255,255),1)
                                cv2.putText(Img_WebCam,str(round((Arr_TiempoReal[3]) ,2)),(65,15),Font_CV, .5,(255,255,255),1)
                                cv2.putText(Img_WebCam,'D: ',(5,35),Font_CV, .5,(255,255,255),1)
                                cv2.putText(Img_WebCam,str(round(Int_Contador_Distancia ,2)),(20,35),Font_CV, .5,(255,255,255),1)
                                cv2.imshow('Tracking',Img_WebCam)
                                cv2.moveWindow('Tracking', 120,250);
                                
                                
                                Mat_Datos[Int_Contador][0] = Arr_TiempoReal[3]
                                try:
                                    Mat_Datos[Int_Contador][1] = int(Centroide[MinSize][1])
                                    Mat_Datos[Int_Contador][2] = int(Centroide[MinSize][0])
                                except:
                                    Mat_Datos[Int_Contador][1] = Mat_Datos[Int_Contador-1][1]
                                    Mat_Datos[Int_Contador][2] = Mat_Datos[Int_Contador-1][2]
                                Mat_Datos[Int_Contador][3] = (Fun_Distancia(Mat_Datos[Int_Contador-1][1],Mat_Datos[Int_Contador][1],Mat_Datos[Int_Contador-1][2],Mat_Datos[Int_Contador][2],Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])))
                                Mat_Datos[Int_Contador][4] = Int_Datos_Consecuencia
                                Int_Contador_Distancia += Mat_Datos[Int_Contador][3]
                                
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
                                    
                            
                            #Guardar_Datos
                            Nombre_Grafico =  filedialog.asksaveasfilename(initialdir = Dir_Datos,
                                                                         title = "Save Data",
                                                                         filetypes = (("all files","*.*"), ("txt files","*.txt"))) 
                                          
                            #Datos_Generales
                            Archivo_Mat_Datos = open(Nombre_Grafico + '.txt','w')
                            Archivo_Mat_Datos.write('Subject: ' + Str_Sujeto + '\n' +
                                                    'Session: ' + Str_Sesion + '\n' +
                                                    'Group: ' + Str_Grupo + '\n' +
                                                    'Time: '+ str(max(Mat_Datos[:,0])) + '\n' +
                                                    '# Consecuences: ' + str(np.size(np.where(Mat_Datos[:,4] == 1))) + '\n' +
                                                    'Distance: ' + str(round(sum(Mat_Datos[:,3]),3)) + 'cm' + '\n' +
                                                    'Velocity: ' + str(round(sum(Mat_Datos[:,3])/max(Mat_Datos[:,0]),3)) + 'cm/seg' + '\n' +
                                                    'Mean Aceleration: ' + str(round(statistics.mean(Mat_Datos[:,5]),3)) + 'm/seg' + '\n' +
                                                    '\n' + 'Frame,Time,X,Y,Distance,Events,Aceleration' + '\n')
                            
                            #Datos_Matriz
                            i = 1
                            for i in range(0,len(Mat_Datos)): 
                                Archivo_Mat_Datos.write(str(i) + ',' + str(round(Mat_Datos[i][0],3)) +
                                                                 ',' + str(round(Mat_Datos[i][1] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])),3)) +
                                                                 ',' + str(round(Mat_Datos[i][2] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[16])),3)) +
                                                                 ',' + str(round(Mat_Datos[i][3],3)) +
                                                                 ',' + str(Mat_Datos[i][4]) + ';' + str(Mat_Datos[i][6]) +
                                                                 ',' + str(round(Mat_Datos[i][5],3)) + '\n')
                            Archivo_Mat_Datos.close() 
                            
                            if Seleccion_Track == 3:
                                messagebox.showinfo("Finalized", "Sesion has been traked")
                            Main_Ses.destroy()
                            
                        #%%Sesion_Sujetos>1       
                        else:
                            Arr_TiempoReal[0]=time.time()
                            
                            while(Tiempo_Sesion >= Arr_TiempoReal[3]):
                                
                                ret, Img_WebCam = Dev_WebCam_Read.read()
                                if ret==True and Var_Save_video == 1:
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
                        
                                    if Mat_RGB[i][5]==1:
                                        image_aux = ndimage.gaussian_filter(image_aux, sigma=3)
                                    elif Mat_RGB[i][5]==2:
                                        image_aux = ndimage.gaussian_filter(image_aux, sigma=5)
                                    elif Mat_RGB[i][5]==3:
                                        image_aux =ndimage.uniform_filter(image_aux, size=2)
                                    elif Mat_RGB[i][5]==4:
                                        image_aux =ndimage.uniform_filter(image_aux, size=11)
                                    elif Mat_RGB[i][5]==5:
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
                                    Mat_Datos_D[Int_Contador][i] = (Fun_Distancia(Mat_Datos_X[Int_Contador-1][i],Mat_Datos_X[Int_Contador][i],Mat_Datos_Y[Int_Contador-1][i],Mat_Datos_Y[Int_Contador][i],Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])))  
                                    
                                    image_total += image_aux
                                    if i == number_subject -1:
                                        image_total = cv2.resize(image_total,(400, round((400/Img_WebCam.shape[1])*Img_WebCam.shape[1])))
                                        j = 0
                                        for j in range(number_subject):
                                            cv2.putText(image_total,str(j+1),(round(int(Mat_Datos_X[Int_Contador][j]) * 400/int(Arr_Parametros_Imagen[15])) + 10,
                                                                              round(int(Mat_Datos_Y[Int_Contador][j]) * 400/int(Arr_Parametros_Imagen[16]))),
                                                                              Font_CV, .5,(0,0,255),1)
                                            #cv2.putText(image_total,str(round(sum(Mat_Datos_D[:,j]),2)),(65*(j+1),35),Font_CV, .5,(255,255,255),1)    
                                        #cv2.putText(image_total,'D: ',(5,35),Font_CV, .5,(255,255,255),1)
                                        cv2.putText(image_total,'Time: ',(5,15),Font_CV, .5,(255,255,255),1)
                                        cv2.putText(image_total,str(round((Arr_TiempoReal[3]) ,2)),(65,15),Font_CV, .5,(255,255,255),1)
                                        cv2.imshow('Tracking',image_total)
                                        cv2.moveWindow('Tracking', 120,250);
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
                            
                            #Guardar_Datos
                            Nombre_Grafico =  filedialog.asksaveasfilename(initialdir = Dir_Datos,
                                                                         title = "Save Data",
                                                                         filetypes = (("all files","*.*"), ("txt files","*.txt"))) 
                                          
                            #Datos
                            j = 0
                            for j in range(number_subject):
                                #Datos_Generales
                                Archivo_Mat_Datos = open(Nombre_Grafico +'_' + str(j+1) + '.txt','w')
                                Archivo_Mat_Datos.write('Subject: ' + Str_Sujeto + '_' + str(j+1) +'\n' +
                                                        'Session: ' + Str_Sesion + '\n' +
                                                        'Group: ' + Str_Grupo + '\n' +
                                                        'Time: '+ str(max(Mat_Datos[:,0])) + '\n' +
                                                        '# Consecuences: ' + str(np.size(np.where(Mat_Datos[:,4] == 1))) + '\n' +
                                                        'Distance: ' + str(round(sum(Mat_Datos_D[:,j]),3)) + 'cm' + '\n' +
                                                        'Velocity: ' + str(round(sum(Mat_Datos_D[:,j])/max(Mat_Datos[:,0]),3)) + 'cm/seg' + '\n' +
                                                        'Mean Aceleration: ' + str(round(statistics.mean(Mat_Datos_D[:,j]/100)/statistics.mean(Mat_Datos[:,0]),3)) + 'm/seg' + '\n' +
                                                        '\n' + 'Frame;Time;X;Y;Aceleration;Distance;Consecuences' + '\n')
                                #Datos_Matriz
                                i = 1
                                for i in range(0,len(Mat_Datos)): 
                                    Archivo_Mat_Datos.write(str(i) + ';' + str(round(Mat_Datos[i][0],3)) +
                                                                     ';' + str(round(Mat_Datos_X[i][j] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[15])),3)) +
                                                                     ';' + str(round(Mat_Datos_Y[i][j] * (Dev_Espacio_Tamano/int(Arr_Parametros_Imagen[16])),3)) +
                                                                     ';' + str(round((Mat_Datos_D[i,j]/100)/Mat_Datos[i,0],3)) +
                                                                     ';' + str(round(Mat_Datos_D[i][j],3)) +
                                                                     ';' + '0' + '\n')
                                
                            
               
                            
                            if Seleccion_Track == 3:
                                messagebox.showinfo("Finalized", "Sesion has been traked")
                            Main_Ses.destroy()
                    
                    
                    #Tiempo
                    Lbl_SesionT_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Time')
                    Lbl_SesionT_Text_1.config(font = (Font_1,18))
                    Lbl_SesionT_Text_1.place(x=30, y = 30)
                    #Box
                    Lbl_SesionT_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
                    Lbl_SesionT_TextBox_1.config(font = (Font_1,15))
                    Lbl_SesionT_TextBox_1.place(x=150, y = 35)
                    
                    #Sujeto
                    Lbl_Sujeto_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Subject')
                    Lbl_Sujeto_Text_1.config(font = (Font_1,18))
                    Lbl_Sujeto_Text_1.place(x=30, y = 80)
                    #Box
                    Lbl_Sujeto_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
                    Lbl_Sujeto_TextBox_1.config(font = (Font_1,15))
                    Lbl_Sujeto_TextBox_1.place(x=150, y = 85)
                    
                    #Sesion
                    Lbl_Sesion_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Session')
                    Lbl_Sesion_Text_1.config(font = (Font_1,18))
                    Lbl_Sesion_Text_1.place(x=30, y = 130)
                    #Box
                    Lbl_Sesion_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
                    Lbl_Sesion_TextBox_1.config(font = (Font_1,15))
                    Lbl_Sesion_TextBox_1.place(x=150, y = 135)
                    
                    #Grupo
                    Lbl_Grupo_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Group')
                    Lbl_Grupo_Text_1.config(font = (Font_1,18))
                    Lbl_Grupo_Text_1.place(x=30, y = 180)
                    #Box
                    Lbl_Grupo_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
                    Lbl_Grupo_TextBox_1.config(font = (Font_1,15))
                    Lbl_Grupo_TextBox_1.place(x=150, y = 185)
                    
                    Lbl_Save_Text = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Save video')
                    Lbl_Save_Text.config(font = (Font_1,14))
                    Lbl_Save_Text.place(x=aux_width_monitor*6.1, y = aux_height_monitor*10.2)
            
                    Var_Radiobutton = tkinter.IntVar(Main_Ses)
                    radiobutton1 = tkinter.Radiobutton(Main_Ses, text='', bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), 
                                                       activebackground=Fun_Rgb(C_Pal4),
                                                       highlightbackground=Fun_Rgb(C_Pal5), variable=Var_Radiobutton, value=1)
                    radiobutton1.config(font = (Font_1,24))
                    radiobutton1.place(x=aux_width_monitor*7.2, y = aux_height_monitor*10.05)
                    Var_Radiobutton.get()
                    
                    #Bnt Next
                    Bnt_Next = tkinter.Button(Main_Ses, bd=0, fg = Fun_Rgb(C_Pal5),
                                              bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                              highlightbackground=Fun_Rgb(C_Pal5),
                                              text = '  Run  ', command = Fun_Bnt_Next)
                    Bnt_Next.config(font = (Font_1,25))
                    Bnt_Next.place(x=aux_width_monitor*6.1, y = aux_height_monitor*11)
                    
                    Main_Ses.mainloop()
        
                
                Ventana_Sesion()
                             
        #%%Next subject function
        def Fun_Next_Subject():
            
            if Seleccion_Track == 0:
                messagebox.showinfo("Error", "Select a traking option")
            
            aux_count = 0
            global number_subject, Mat_RGB
            Var_R = int(Slider_Rojo.get())
            Var_G = int(Slider_Verde.get())
            Var_B = int(Slider_Azul.get())
            Var_Des = int(Slider_Desviacion.get())
            Var_Umbral = float(Entr_Umbral.get())
            Img_Filtro = Var_Filtro.get()
        #    Mat_RGB2 = ([Var_R, Var_G, Var_B, Var_Des, 1, Img_Filtro])
            Mat_RGB2 = ([Var_R, Var_G, Var_B, Var_Des, Var_Umbral, Img_Filtro])
            
            global Lbl_Img_Original, Lbl_Img_Original_Aux
            Lbl_Img_Original.place_forget()
            Lbl_Img_Original_Aux.place_forget()
            
            #Direccion_nueva Imagen
            global Dialog_Video_File_Aux_2
            Dialog_Video_File_Aux_2 = Dialog_Video_File_Aux.replace('Aux_Image', 'Aux_Imagee')
            
            #Guardar Imagenes
            Img_Cortable = imageio.imread(Dialog_Video_File_Aux)
            Img_Cortable_Aux = Img_Cortable[:, :]
            imageio.imsave(Dialog_Video_File_Aux_2, Img_Cortable_Aux)
            
            Img_Original_2 = Image.open(Dialog_Video_File_Aux)
            if int(Img_Original_2.size[0])>Var_Tamaño_Lbl_X:
                Img_Original_2 = Img_Original_2.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original_2.size[0]))*int(Img_Original_2.size[1]))), 
                                Image.ANTIALIAS)
                if int(Img_Original_2.size[1]) > Var_Tamaño_Lbl_Y:
                    Img_Original_2 = Img_Original_2.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original_2.size[1]))*int(Img_Original_2.size[0])),Var_Tamaño_Lbl_Y), 
                                Image.ANTIALIAS)
            elif int(Img_Original_2.size[1])>Var_Tamaño_Lbl_Y:
                Img_Original_2 = Img_Original_2.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original_2.size[1]))*int(Img_Original_2.size[0])),Var_Tamaño_Lbl_Y), 
                                                Image.ANTIALIAS)
                if int(Img_Original_2.size[0]) > Var_Tamaño_Lbl_X:
                    Img_Original_2 = Img_Original_2.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original_2.size[0]))*int(Img_Original_2.size[1]))), 
                                                    Image.ANTIALIAS)
            
            #Mostrar Imagen
            Pho_Img_Cortable_Aux = ImageTk.PhotoImage(Img_Original_2)
            Lbl_Parametros_Aux = tkinter.Label(image=Pho_Img_Cortable_Aux, bg = Fun_Rgb(C_Pal5), bd = 0)
            Lbl_Parametros_Aux.image = Pho_Img_Cortable_Aux 
            Lbl_Parametros_Aux.place(x = (aux_width_monitor*1.5)+1, y = (aux_height_monitor*1.5)+1)
           
            
            if aux_count == 0:
                Mat_RGB[number_subject][:]= Mat_RGB2
                number_subject += 1 
                
                Slider_Rojo.set(0)
                Slider_Verde.set(0)
                Slider_Azul.set(0)
                Slider_Desviacion.set(0)
                Entr_Umbral.set(.5)
                Var_Filtro.set(0)
                      
        #%%Widgets Cortar imagen
        
        Slider_X1 = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=0, to=.5, resolution=0.01,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*2.8,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal3), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal3),
                                  showvalue=1)
        Slider_X1.config(font=(Font_1,11))
        Slider_X1.place(x=int(aux_width_monitor*1.5), y=int(aux_height_monitor*.4))
        
        
        Slider_X2 = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=.51, to=1, resolution=0.01,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*2.8,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal3), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal3),
                                  showvalue=1)
        Slider_X2.config(font=(Font_1,11))
        Slider_X2.set(1)
        Slider_X2.place(x=aux_width_monitor*4.7, y=aux_height_monitor*.4)

        Slider_Y1 = tkinter.Scale(Win_Cortar_Imagen,
                                  from_=0, to=.5, resolution=0.01,
                                  orient=tkinter.VERTICAL, width = aux_height_monitor*.3,  length=aux_height_monitor*4.5,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal3), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal3),
                                  showvalue=1)
        Slider_Y1.config(font=(Font_1,11))
        Slider_Y1.place(x=aux_width_monitor*.7, y=aux_height_monitor*1.5)

        Slider_Y2 = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=.51, to=1, resolution=0.01,
                                  orient=tkinter.VERTICAL, width = aux_height_monitor*.3,  length=aux_height_monitor*4.5,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal3), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal3),
                                  showvalue=1)
        Slider_Y2.config(font=(Font_1,11))
        Slider_Y2.set(1)
        Slider_Y2.place(x=aux_width_monitor*.7, y=aux_height_monitor*6.5)
        
        
        Slider_Grados_Rotar = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=-90, to=90, resolution=1,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*2.5,
                                  fg=Fun_Rgb(C_Pal5), bg=Fun_Rgb(C_Pal3), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal4), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal3),
                                  showvalue=1)
        Slider_Grados_Rotar.config(font = (Font_1,11))
        Slider_Grados_Rotar.set(0)
        Slider_Grados_Rotar.place(x=aux_width_monitor*1.5, y=aux_height_monitor*11.8)
        Lbl_Slider_Grados_Rotar = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), 
                                     text = 'Image degrees')
        Lbl_Slider_Grados_Rotar.config(font=(Font_1,14))
        Lbl_Slider_Grados_Rotar.place(x=aux_width_monitor*1.5, y=aux_height_monitor*11.15)
        
        
        Etr_Tamano_Caja = tkinter.Entry(Win_Cortar_Imagen, width = 9)
        Etr_Tamano_Caja.config(font = (Font_1,18))
        Etr_Tamano_Caja.place(x=aux_width_monitor*4.2, y=aux_height_monitor*11.9)
        Etr_Tamano_Caja.insert(0,'1')
        Lbl_Etr_Tamano_Caja = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), 
                                     text = 'Image size')
        Lbl_Etr_Tamano_Caja.config(font=(Font_1,14))
        Lbl_Etr_Tamano_Caja.place(x=aux_width_monitor*4.15, y=aux_height_monitor*11.2)
        

               
        Btn_Cortar_Imagen = tkinter.Button(Win_Cortar_Imagen, bd=0, fg = Fun_Rgb(C_Pal5),
                                           highlightbackground=Fun_Rgb(C_Pal3), width=10, 
                                          bg = Fun_Rgb(C_Pal3), activebackground=Fun_Rgb(C_Pal5),
                                          text = 'Preview', command =Fun_Imagen)
        Btn_Cortar_Imagen.config(font = (Font_1,18))
        Btn_Cortar_Imagen.place(x=aux_width_monitor*5.8, y=aux_height_monitor*11.8)
        
        #%%Widgets Edicion imagen  
        global arr_Color_Cuadro, arr_Color_Cuadro1, arr_Color_Cuadro2
        
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
      
        Lbl_Slider_1 = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal3), 
                                     text = 'Color')
        Lbl_Slider_1.config(font=(Font_1,20))
        Lbl_Slider_1.place(x=aux_width_monitor*7.8, y=aux_height_monitor*.7)
        
        #Slider 1
        Lbl_Slider_RojoText_1 = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), 
                                          fg = Fun_Rgb(C_Pal4), text = 'R')
        Lbl_Slider_RojoText_1.config(font = (Font_1,20))
        Lbl_Slider_RojoText_1.place(x=aux_width_monitor*7.8, y=aux_height_monitor*1.5)
        
        Slider_Rojo = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=0, to=255, resolution=1,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*2.5,
                                  fg=Fun_Rgb(C_Pal3), bg=Fun_Rgb(C_Pal4), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal5), troughcolor= Fun_Rgb(C_Pal5),
                                  highlightbackground=Fun_Rgb(C_Pal4),
                                  showvalue=1, command = Fun_Color_CuadroR)
        Slider_Rojo.set(255)
        Slider_Rojo.config(font = (Font_1,12))
        Slider_Rojo.place(x=aux_width_monitor*8.3, y=aux_height_monitor*1.5)
        
        
        #Slider 2
        Lbl_Slider_VerdeText_1 = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), 
                                           fg = Fun_Rgb(C_Pal4), text = 'G')
        Lbl_Slider_VerdeText_1.config(font = (Font_1,20))
        Lbl_Slider_VerdeText_1.place(x=aux_width_monitor*7.8, y=aux_height_monitor*2.7)
        Slider_Verde = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=0, to=255, resolution=1,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*2.5,
                                  fg=Fun_Rgb(C_Pal3), bg=Fun_Rgb(C_Pal4), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal5), troughcolor= Fun_Rgb(C_Pal5),
                                  highlightbackground=Fun_Rgb(C_Pal4),
                                  showvalue=1, command = Fun_Color_CuadroG )
        Slider_Verde.set(255)
        Slider_Verde.config(font = (Font_1,12))
        Slider_Verde.place(x=aux_width_monitor*8.3, y=aux_height_monitor*2.7)
        
        #Slider 3
        Lbl_Slider_AzulText_1 = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), 
                                          fg = Fun_Rgb(C_Pal4), text = 'B')
        Lbl_Slider_AzulText_1.config(font = (Font_1,20))
        Lbl_Slider_AzulText_1.place(x=aux_width_monitor*7.8, y=aux_height_monitor*3.9)
        Slider_Azul = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=0, to=255, resolution=1,
                                  orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*2.5,
                                  fg=Fun_Rgb(C_Pal3), bg=Fun_Rgb(C_Pal4), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal5), troughcolor= Fun_Rgb(C_Pal5),
                                  highlightbackground=Fun_Rgb(C_Pal4),
                                  showvalue=1, command = Fun_Color_CuadroB )
        Slider_Azul.set(255)
        Slider_Azul.config(font = (Font_1,12))
        Slider_Azul.place(x=aux_width_monitor*8.3, y=aux_height_monitor*3.9)
        
        #Slider Desviación
        Lbl_Slider_Desviacio = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal4), 
                                     text = 'Range')
        Lbl_Slider_Desviacio.config(font=(Font_1,20))
        Lbl_Slider_Desviacio.place(x=aux_width_monitor*13.8, y=aux_height_monitor*.7)
        Slider_Desviacion = tkinter.Scale(Win_Cortar_Imagen, 
                                  from_=0, to=150, resolution=1,
                                  orient=tkinter.VERTICAL, width = aux_height_monitor*.4,  length= aux_width_monitor*2.4,
                                  fg=Fun_Rgb(C_Pal3), bg=Fun_Rgb(C_Pal4), bd = 0,
                                  activebackground=Fun_Rgb(C_Pal5), troughcolor= Fun_Rgb(C_Pal5), 
                                  highlightbackground=Fun_Rgb(C_Pal4),
                                  showvalue=1, command = Fun_Color_Des)
        Slider_Desviacion.set(0)
        Slider_Desviacion.config(font = (Font_1,14))
        Slider_Desviacion.place(x=aux_width_monitor*13.9, y=aux_height_monitor*1.5)
        
        Rgb_Can = Canvas(Win_Cortar_Imagen, width=int(aux_width_monitor*2.4), highlightbackground = Fun_Rgb(C_Pal4),
                         height= int(aux_width_monitor*2.4), bg=Fun_Rgb(C_Black))
        Cuadro_Rgb2 =  Rgb_Can.create_rectangle(0, 0, aux_width_monitor*.8, aux_width_monitor*2.5, outline=Fun_Rgb(C_Black), width=0)
        Cuadro_Rgb1 =  Rgb_Can.create_rectangle(aux_width_monitor*.8, 0, aux_width_monitor*1.6, aux_width_monitor*2.5, outline=Fun_Rgb(C_Black), width=0)
        Cuadro_Rgb3 =  Rgb_Can.create_rectangle(aux_width_monitor*1.6, 0, aux_width_monitor*2.5, aux_width_monitor*2.5, outline=Fun_Rgb(C_Black), width=0)
        Rgb_Can.place(x=aux_width_monitor*11.15, y=aux_height_monitor*1.5)  
        
        
        #filtros
        Lbl_Filtro_1 = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), 
                                     fg = Fun_Rgb(C_Pal3), highlightbackground = Fun_Rgb(C_Pal5),
                                     text = 'Filter')
        Lbl_Filtro_1.config(font = (Font_1,20))
        Lbl_Filtro_1.place(x=aux_width_monitor*7.8, y=aux_height_monitor*5.5)
        
        Var_Filtro = tkinter.IntVar()
        RdBtn_1 = tkinter.Radiobutton(Win_Cortar_Imagen,bd=0, fg = Fun_Rgb(C_Pal3),
                                      bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal4), 
                                      highlightbackground = Fun_Rgb(C_Pal5),
                                      text="Black & White - Weak  ", variable=Var_Filtro, 
                                      value=1, indicatoron=0, width = 23)
        RdBtn_1.config(font = (Font_1,15))
        RdBtn_1.place(x=aux_width_monitor*7.8, y=aux_height_monitor*6.4)
        RdBtn_2 = tkinter.Radiobutton(Win_Cortar_Imagen,bd=0, fg = Fun_Rgb(C_Pal3),
                                      bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal4), 
                                      highlightbackground = Fun_Rgb(C_Pal5),
                                      text="Black & White - Strong", variable=Var_Filtro, 
                                      value=2, indicatoron=0, width = 23)
        RdBtn_2.config(font = (Font_1,15))
        RdBtn_2.place(x=aux_width_monitor*7.8, y=aux_height_monitor*7.2)
        RdBtn_3 = tkinter.Radiobutton(Win_Cortar_Imagen,bd=0, fg = Fun_Rgb(C_Pal3),
                                      bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal4), 
                                      highlightbackground = Fun_Rgb(C_Pal5),
                                      text="Uniform - Weak       ", variable=Var_Filtro, 
                                      value=3, indicatoron=0, width = 22)
        RdBtn_3.config(font = (Font_1,15))
        RdBtn_3.place(x=aux_width_monitor*11.4, y=aux_height_monitor*6.4)
        RdBtn_4 = tkinter.Radiobutton(Win_Cortar_Imagen,bd=0, fg = Fun_Rgb(C_Pal3),
                                      bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal4), 
                                      highlightbackground = Fun_Rgb(C_Pal5),
                                      text="Uniform - Strong     ", variable=Var_Filtro, 
                                      value=4, indicatoron=0, width = 22)
        RdBtn_4.config(font = (Font_1,15))
        RdBtn_4.place(x=aux_width_monitor*11.4, y=aux_height_monitor*7.2)
        RdBtn_5 = tkinter.Radiobutton(Win_Cortar_Imagen,bd=0, fg = Fun_Rgb(C_Pal3),
                                      bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal4),
                                      highlightbackground = Fun_Rgb(C_Pal5),
                                      text="No Filter             ", variable=Var_Filtro, 
                                      value=5, indicatoron=0, width = 23)
        RdBtn_5.config(font = (Font_1,15))
        RdBtn_5.place(x=aux_width_monitor*7.8, y=aux_height_monitor*8)
        
        Var_Filtro.get()
        
        #Otros
        Lbl_Filtro_2 = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal3), 
                                     text = 'Threshold')
        Lbl_Filtro_2.config(font = (Font_1,20))
        Lbl_Filtro_2.place(x=aux_width_monitor*7.8, y=aux_height_monitor*9.1)
        
        Entr_Umbral = tkinter.Scale(Win_Cortar_Imagen, 
                                    from_= 0, to=1, resolution=0.01,
                                    orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*3,
                                    fg=Fun_Rgb(C_Pal3), bg=Fun_Rgb(C_Pal4), bd = 0,
                                    activebackground=Fun_Rgb(C_Pal5), troughcolor= Fun_Rgb(C_Pal5), 
                                    highlightbackground=Fun_Rgb(C_Pal4),
                                    showvalue=1)
        Entr_Umbral.config(font = (Font_1,15))
        Entr_Umbral.set(.5)
        Entr_Umbral.place(x=aux_width_monitor*7.8, y=aux_height_monitor*10)
        
        Lbl_Filtro_3 = tkinter.Label(Win_Cortar_Imagen, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal3), 
                                     text = 'Target size')
        Lbl_Filtro_3.config(font = (Font_1,20))
        Lbl_Filtro_3.place(x=aux_width_monitor*11.4, y=aux_height_monitor*9.1)        
        Entr_Valor_Minimo_Animal = tkinter.Scale(Win_Cortar_Imagen, 
                                    from_= 0, to=50, resolution=1,
                                    orient=tkinter.HORIZONTAL, width = aux_height_monitor*.4,  length=aux_width_monitor*3,
                                    fg=Fun_Rgb(C_Pal3), bg=Fun_Rgb(C_Pal4), bd = 0,
                                    activebackground=Fun_Rgb(C_Pal5), troughcolor= Fun_Rgb(C_Pal5), 
                                    highlightbackground=Fun_Rgb(C_Pal4),
                                    showvalue = 1)
        Entr_Valor_Minimo_Animal.config(font = (Font_1,15))
        Entr_Valor_Minimo_Animal.set(3)
        Entr_Valor_Minimo_Animal.place(x=aux_width_monitor*11.4, y=aux_height_monitor*10)
        
        
        
        #%%Bnt Funciones Ventana Cortar imagen
        
        Btn_Ver_Imagen = tkinter.Button(Win_Cortar_Imagen, bd=0, fg = Fun_Rgb(C_Pal3),
                                          bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal5),
                                          text = ' Preview ', highlightbackground = Fun_Rgb(C_Pal5), 
                                          command =Fun_Editar_Imagen)
        Btn_Ver_Imagen.config(font = (Font_1,20))
        Btn_Ver_Imagen.place(x=aux_width_monitor*7.8, y=aux_height_monitor*11.6)
        
        Btn_Next_Subject = tkinter.Button(Win_Cortar_Imagen, bd=0, fg = Fun_Rgb(C_Pal3),
                                  bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal5),
                                  text = 'Add subject', highlightbackground = Fun_Rgb(C_Pal5), 
                                  command =Fun_Next_Subject)
        Btn_Next_Subject.config(font = (Font_1,20))
        Btn_Next_Subject.place(x=aux_width_monitor*9.4, y=aux_height_monitor*11.6)
        
        Btn_Cortar_Imagen = tkinter.Button(Win_Cortar_Imagen, bd=0, fg = Fun_Rgb(C_Pal3),
                                          bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal5),
                                          text = '   Save   ', highlightbackground = Fun_Rgb(C_Pal5), 
                                          command =Fun_Editar_Todas_Imagenes)
        Btn_Cortar_Imagen.config(font = (Font_1,20))
        Btn_Cortar_Imagen.place(x=aux_width_monitor*11.5, y=aux_height_monitor*11.6)
        
        Btn_Iniciar_Track = tkinter.Button(Win_Cortar_Imagen, bd=0, fg = Fun_Rgb(C_Pal3),
                                          bg = Fun_Rgb(C_Pal4), activebackground=Fun_Rgb(C_Pal5),
                                          text = 'Tracking ', highlightbackground = Fun_Rgb(C_Pal5), 
                                          command =Fun_Iniciar_Track)
        Btn_Iniciar_Track.config(font = (Font_1,20))
        Btn_Iniciar_Track.place(x=aux_width_monitor*13.1, y=aux_height_monitor*11.6)
        
        Win_Cortar_Imagen.mainloop()    
        
    #%%Programas Reforzamiento
    def Fun_Programas_Ref():
        ventanaMenuPrincipal.destroy()
        
        #Configuracion
        global Dir_Archivo_Parametros, Arr_Parametros_track, Arr_Parametros_Pref, Dir_Archivo_Datos
        Txt_Imagen = open(Dir_Archivo_Parametros +'Image.txt','r')
        Arr_Parametros_track = Txt_Imagen.read().split('\n')
        Txt_Imagen.close()
        Txt_Pref = open(Dir_Archivo_Parametros +'PRef.txt','r')
        Arr_Parametros_Pref = Txt_Pref.read().split('\n')
        Txt_Pref.close()
        
        #rogramas Reforzamiento
        global PRef_Tipo_Programa, Pref_Intervalo, Pref_Senalar_Intervalo, Pref_Distancia, Pref_Senalar_Distancia, Pref_Cuadrante_Intervalo, Pref_Senalar_Cuadrante, Pref_Cuadrante, Pref_Tiempo_Consecuencia, Tiempo_Sesion
        PRef_Tipo_Programa = int(Arr_Parametros_Pref[0])
        Pref_Intervalo = literal_eval(Arr_Parametros_Pref[1])
        Pref_Senalar_Intervalo = int(Arr_Parametros_Pref[2])
        Pref_Distancia = literal_eval(Arr_Parametros_Pref[3])
        Pref_Senalar_Distancia = int(Arr_Parametros_Pref[4])
        Pref_Cuadrante_Intervalo = literal_eval(Arr_Parametros_Pref[5])
        Pref_Senalar_Cuadrante = int(Arr_Parametros_Pref[6])
        Pref_Cuadrante = literal_eval(Arr_Parametros_Pref[7])
        Pref_Tiempo_Consecuencia = literal_eval(Arr_Parametros_Pref[8])
        Tiempo_Sesion = int(Arr_Parametros_Pref[9])
        
        #magen + traking
        global Dev_WebCam, Dev_WebCam_Resolution, Arr_ImgConfig,  Mat_RGB, Img_Filtro, Track_MinSize, Size_Proportion, Dev_Espacio_Tamano
        Dev_WebCam = int(Arr_Parametros_track[0])
        Dev_WebCam_Resolution = int(Arr_Parametros_track[1])
        Arr_ImgConfig = (float(Arr_Parametros_track[2]),float(Arr_Parametros_track[3]),float(Arr_Parametros_track[4]),float(Arr_Parametros_track[5]),int(Arr_Parametros_track[6]),0,1) #X1,X2,Y1,Y2,Grados,AaumentarReducir,Porcentaje
        Dev_Espacio_Tamano = int(Arr_Parametros_track[7])
        Size_Proportion = int(Arr_Parametros_track[15])
        Mat_RGB = ([int(Arr_Parametros_track[8]),int(Arr_Parametros_track[9]),int(Arr_Parametros_track[10]),int(Arr_Parametros_track[11]),float(Arr_Parametros_track[12])])
        Img_Filtro = int(Arr_Parametros_track[13])
        Track_MinSize = float(Arr_Parametros_track[14])
        
        #Arduino
        global Arduino_Com
        Arduino_Com = Arr_Parametros_Pref[10]
        
        #Sesion
        global Str_Sujeto, Str_Sesion, Str_Grupo, Str_Notas
        Str_Sujeto = ' '
        Str_Sesion = ' '
        Str_Grupo = ' '
        Str_Notas = ' '
        
        #Save programas reforzamiento
        global Arr_Variables_Pref
        
        
        
        #%%Funciones
        
        def Fun_Rgb(RGB):
            return "#%02x%02x%02x" % RGB  
         
        def Fun_Size(img, size):
            img = Image.open(img)
            size_1 = img.size
            width = int(size_1[0]*size)
            height = int(size_1[1]*size)
            img = img.resize((width, height),Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            return img
        

        
        #%%Menu Save programas reforzamiento
        def Fun_Save_PRef():
            global Arr_Variables_Pref, Tiempo_Sesion, PRef_Tipo_Programa, Pref_Intervalo, Pref_Senalar_Intervalo, Pref_Distancia, Pref_Senalar_Distancia, Pref_Cuadrante_Intervalo, Pref_Senalar_Cuadrante, Pref_Cuadrante, Pref_Tiempo_Consecuencia
            if PRef_Tipo_Programa == 1:
                Pref_Intervalo = Lbl_Programa1_TextBox_1.get('1.0','end-1c')
                Pref_Distancia = '(0,)'
                Pref_Senalar_Distancia = '0'
                Pref_Cuadrante_Intervalo = '(0,)'
                Pref_Senalar_Cuadrante = '0'
                Pref_Cuadrante = '(0,0,0,0)'
            elif PRef_Tipo_Programa == 2:
                Pref_Distancia = Lbl_Programa2_TextBox_1.get('1.0','end-1c')
                Pref_Intervalo = '(0,)'
                Pref_Senalar_Intervalo = '0'
                Pref_Cuadrante_Intervalo = '(0,)'
                Pref_Senalar_Cuadrante = '0'
                Pref_Cuadrante = '(0,0,0,0)'
            elif PRef_Tipo_Programa == 3:
                Pref_Intervalo = Lbl_Programa3_TextBox_1.get('1.0','end-1c')
                Pref_Distancia = Lbl_Programa3_TextBox_2.get('1.0','end-1c')
                Pref_Cuadrante_Intervalo = '(0,)'
                Pref_Senalar_Cuadrante = '0'
                Pref_Cuadrante = '(0,0,0,0)'
            elif PRef_Tipo_Programa == 4:
                Pref_Intervalo = Lbl_Programa4_TextBox_2.get('1.0','end-1c')
                Pref_Distancia = Lbl_Programa4_TextBox_1.get('1.0','end-1c')
                Pref_Cuadrante_Intervalo = '(0,)'
                Pref_Senalar_Cuadrante = '0'
                Pref_Cuadrante = '(0,0,0,0)'
            elif PRef_Tipo_Programa == 5:
                Pref_Cuadrante_Intervalo = Lbl_Programa5_TextBox_1.get('1.0','end-1c')
                Pref_Cuadrante = Lbl_Programa5_TextBox_2.get('1.0','end-1c')
                Pref_Distancia = '(0,)'
                Pref_Senalar_Distancia = '0'
                Pref_Intervalo = '(0,)'
                Pref_Senalar_Intervalo = '0'
            Pref_Tiempo_Consecuencia = (int(Lbl_Consecuencia_TextBox_1.get('1.0','end-1c')),0,0,0,0)
            Tiempo_Sesion = Lbl_TSesion_TextBox_1.get('1.0','end-1c')
            global Arr_Variables_Pref
            
            Arr_Variables_Pref = [str(PRef_Tipo_Programa),
                                  str(Pref_Intervalo), str(Pref_Senalar_Intervalo),
                                  str(Pref_Distancia),str(Pref_Senalar_Distancia),
                                  str(Pref_Cuadrante_Intervalo),str(Pref_Senalar_Cuadrante),str(Pref_Cuadrante),
                                  str(Pref_Tiempo_Consecuencia), str(Tiempo_Sesion), Arduino_Com, Temp_Txt_Image]
            
            
            Main.Ruta_Carpeta_Proyecto =  filedialog.asksaveasfilename(initialdir = Dir_Archivo_PRef,
                                                                       title = "Save file",
                                                                       filetypes = (("all files","*.*"), ("txt","*.txt")))
            
            Archivo_Vaariables = open(Main.Ruta_Carpeta_Proyecto + '.txt','w')
            for i in Arr_Variables_Pref:
                Archivo_Vaariables.write(i +'\n')            
            Archivo_Vaariables.close()
            
            
            
        #%%Menu Open programas reforzamiento    
        def Fun_Open_PRef():
            
            #Reset Values
            global Arr_Variables_Pref, Tiempo_Sesion, PRef_Tipo_Programa, Pref_Intervalo, Pref_Senalar_Intervalo, Pref_Distancia, Pref_Senalar_Distancia, Pref_Cuadrante_Intervalo, Pref_Senalar_Cuadrante, Pref_Cuadrante, Pref_Tiempo_Consecuencia
            Pref_Senalar_Intervalo = '(0,)'
            Pref_Distancia = '(0,)'
            Pref_Senalar_Intervalo = '0'
            Pref_Senalar_Distancia = '0'
            Pref_Cuadrante_Intervalo = '(0,)'
            Pref_Senalar_Cuadrante = '0'
            Pref_Cuadrante = '(0,0,0,0)'
            Pref_Senalar_Intervalo = 0
            Pref_Senalar_Distancia = 0
            Pref_Senalar_Cuadrante = 0
            PRef_Tipo_Programa = 0
                
            global Dir_Archivo_Parametros, Arr_Parametros_Pref, Arduino_Com
            Main.Txt_Pref = filedialog.askopenfilename(initialdir = Dir_Archivo_PRef,
                                                    title = "Select file",
                                                    filetypes = (("txt","*.txt"),
                                                    ("all files","*.*")))
            Dir_Archivo_Parametros = open(Main.Txt_Pref, 'r')
            Arr_Parametros_Pref = Dir_Archivo_Parametros.read().split('\n')
            
            Lbl_Consecuencia_TextBox_1.delete('1.0', 'end')
            Lbl_TSesion_TextBox_1.delete('1.0', 'end')
            
            global Tiempo_Sesion, Final_Sesion, C_Final_Sesion, Consecuencias_Sesion
            try:
                if Arr_Parametros_Pref[9].split(',')[1] == '-1':
                    Tiempo_Sesion = 0
                    Consecuencias_Sesion = int(Arr_Parametros_Pref[9].split(',')[0])
                    C_Final_Sesion = 1
            except:
                Tiempo_Sesion = int(Arr_Parametros_Pref[9])
                Consecuencias_Sesion = 0
                C_Final_Sesion = 0
            PRef_Tipo_Programa = int(Arr_Parametros_Pref[0])
            Pref_Intervalo = literal_eval(Arr_Parametros_Pref[1])
            Pref_Senalar_Intervalo = int(Arr_Parametros_Pref[2])
            Pref_Distancia = literal_eval(Arr_Parametros_Pref[3])
            Pref_Senalar_Distancia = int(Arr_Parametros_Pref[4])
            Pref_Cuadrante_Intervalo = literal_eval(Arr_Parametros_Pref[5])
            Pref_Senalar_Cuadrante = int(Arr_Parametros_Pref[6])
            Pref_Cuadrante = literal_eval(Arr_Parametros_Pref[7])
            Pref_Tiempo_Consecuencia = literal_eval(Arr_Parametros_Pref[8])
            Arduino_Com = Arr_Parametros_Pref[10]
            
            if Pref_Senalar_Intervalo == 1:
               Bnt_Senalar1.config(text = '1',bg = Fun_Rgb(C_Pal2))
               Lbl_Senalar1_Text_1.config(bg = Fun_Rgb(C_Pal2),fg = Fun_Rgb(C_Pal5))
            else:
                Bnt_Senalar1.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Senalar1_Text_1.config(bg = Fun_Rgb(C_Pal5),fg = Fun_Rgb(C_Pal2))
            if Pref_Senalar_Distancia == 1:
               Bnt_Senalar2.config(text = '1',bg = Fun_Rgb(C_Pal2))
               Lbl_Senalar2_Text_1.config(bg = Fun_Rgb(C_Pal2),fg = Fun_Rgb(C_Pal5))
            else:
                Bnt_Senalar2.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Senalar2_Text_1.config(bg = Fun_Rgb(C_Pal5),fg = Fun_Rgb(C_Pal2))
            if Pref_Senalar_Cuadrante == 1:
               Bnt_Senalar3.config(text = '1',bg = Fun_Rgb(C_Pal2))
               Lbl_Senalar3_Text_1.config(bg = Fun_Rgb(C_Pal2),fg = Fun_Rgb(C_Pal5))
            else:
                Bnt_Senalar3.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Senalar3_Text_1.config(bg = Fun_Rgb(C_Pal5),fg = Fun_Rgb(C_Pal2))
            Lbl_Consecuencia_TextBox_1.insert('end',str(Pref_Tiempo_Consecuencia[0]))
            Lbl_TSesion_TextBox_1.insert('end',str(Tiempo_Sesion))
            
            if PRef_Tipo_Programa == 1:
                Fun_Bnt_Pro1()    
            elif PRef_Tipo_Programa == 2:
                Fun_Bnt_Pro2()    
            elif PRef_Tipo_Programa == 3:
                Fun_Bnt_Pro3()    
            elif PRef_Tipo_Programa == 4:
                Fun_Bnt_Pro4()    
            elif PRef_Tipo_Programa == 5:
                Fun_Bnt_Pro5()
            else:
                Lbl_Programa2_TextBox_1.delete('1.0', 'end')
                Lbl_Programa2_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_2.delete('1.0', 'end')
                Lbl_Programa4_TextBox_1.delete('1.0', 'end')
                Lbl_Programa4_TextBox_2.delete('1.0', 'end')
                Lbl_Programa5_TextBox_1.delete('1.0', 'end')
                Lbl_Programa5_TextBox_2.delete('1.0', 'end')
                
            
            global Arr_Parametros_track
            
            Dir_Archivo_Parametros = open(Arr_Parametros_Pref[11], 'r')
            Arr_Parametros_track = Dir_Archivo_Parametros.read().split('\n')
            #Dispositivos
            global Dev_WebCam, Dev_WebCam_Resolution
            Dev_WebCam = int(Arr_Parametros_track[0])
            Dev_WebCam_Resolution = int(Arr_Parametros_track[1])
            #Imagen
            global Arr_ImgConfig
            Arr_ImgConfig = (float(Arr_Parametros_track[2]),float(Arr_Parametros_track[3]),float(Arr_Parametros_track[4]),float(Arr_Parametros_track[5]),int(Arr_Parametros_track[6]),0,1) #X1,X2,Y1,Y2,Grados,AaumentarReducir,Porcentaje
            #Traking
            global Mat_RGB, Img_Filtro, Track_MinSize, Dev_Espacio_Tamano, Size_Proportion
            Mat_RGB = ([int(Arr_Parametros_track[8]),int(Arr_Parametros_track[9]),int(Arr_Parametros_track[10]),int(Arr_Parametros_track[11]),float(Arr_Parametros_track[12])])
            Img_Filtro = int(Arr_Parametros_track[13])
            Track_MinSize = float(Arr_Parametros_track[14])
            Dev_Espacio_Tamano = int(Arr_Parametros_track[7])
            Size_Proportion = int(Arr_Parametros_track[15])
                    
            
            
            
            
            
        #%%Menu Open traking parameters
        def Fun_O_ImageParameters():
            global Dir_Archivo_Parametros, Arr_Parametros_track, Temp_Txt_Image
            Main.Txt_Imagen = filedialog.askopenfilename(initialdir = Dir_Proyecto,
                                                    title = "Select file",
                                                    filetypes = (("txt","*.txt"),
                                                    ("all files","*.*")))
            Temp_Txt_Image = Main.Txt_Imagen
            Dir_Archivo_Parametros = open(Main.Txt_Imagen, 'r')
            Arr_Parametros_track = Dir_Archivo_Parametros.read().split('\n')
            #Dispositivos
            global Dev_WebCam, Dev_WebCam_Resolution
            Dev_WebCam = int(Arr_Parametros_track[0])
            Dev_WebCam_Resolution = int(Arr_Parametros_track[1])
            #Imagen
            global Arr_ImgConfig
            Arr_ImgConfig = (float(Arr_Parametros_track[2]),float(Arr_Parametros_track[3]),float(Arr_Parametros_track[4]),float(Arr_Parametros_track[5]),int(Arr_Parametros_track[6]),0,1) #X1,X2,Y1,Y2,Grados,AaumentarReducir,Porcentaje
            #Traking
            global Mat_RGB, Img_Filtro, Track_MinSize, Dev_Espacio_Tamano, Size_Proportion
            Mat_RGB = ([int(Arr_Parametros_track[8]),int(Arr_Parametros_track[9]),int(Arr_Parametros_track[10]),int(Arr_Parametros_track[11]),float(Arr_Parametros_track[12])])
            Img_Filtro = int(Arr_Parametros_track[13])
            Track_MinSize = float(Arr_Parametros_track[14])
            Dev_Espacio_Tamano = int(Arr_Parametros_track[7])
            Size_Proportion = int(Arr_Parametros_track[15])
            
            
                
        #%%Main
        Main = tkinter.Tk()
        Main.title('Reinforcement Schedules 1.0')
        Main.geometry(str(width_monitor)+'x'+str(height_monitor-100)+'+0+0')
        Main.configure(background=Fun_Rgb(C_Pal5))
        #Fondo
        Main_Can = Canvas(width=width_monitor, height=height_monitor-110, bg=Fun_Rgb(C_Pal5))
        Main_Can.create_rectangle(10, 10, width_monitor-10, height_monitor-120, outline=Fun_Rgb(C_Pal3), width=4)
        Main_Can.place(x=0,y=0)  
        
        
        
        #%%Control Menu
        Main_Menu = tkinter.Menu(Main)
        Main.config(menu=Main_Menu)
        #File
        Main_Menu_Opc1 = tkinter.Menu(Main_Menu, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                                     activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Pal2),
                                     tearoff=0)                         
        Main_Menu.add_cascade(label="File", menu=Main_Menu_Opc1)
        Main_Menu_Opc1.add_command(label='Save Schedule', command=Fun_Save_PRef)
        Main_Menu_Opc1.add_command(label='Open schedule', command=Fun_Open_PRef)   
        #Preferences
        Main_Menu_Opc2 = tkinter.Menu(Main_Menu, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                                     activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Pal2),
                                     tearoff=0)                           
        Main_Menu.add_cascade(label='Preferences', menu=Main_Menu_Opc2)
        Main_Menu_Opc2.add_command(label='Image', command=Fun_O_ImageParameters)
        #Com
        Main_Menu_Opc3 = tkinter.Menu(Main_Menu_Opc2, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                                     activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Pal2),
                                     tearoff=0)              
                    
        Main_Menu_Opc2.add_cascade(label='Serial Port', menu=Main_Menu_Opc3) 
        
        Serial_Port = list(serial.tools.list_ports.comports())
        
        def Fun_GetSerial(PortCom):
            global Arduino_Com
            Arduino_Com = Port_String[PortCom]
        
        
        Port_String = list(('','','','',''))
        for i in range(0,len(Serial_Port)):
            Port_String[i] = Serial_Port[i].device
            Port_String_Des = Serial_Port[i].description
            Main_Menu_Opc3.add_command(label=(Port_String_Des),command=lambda PortCom=i: Fun_GetSerial(PortCom))
            
            
            
        #%%Programas Reforzamiento Widgets
            
        #-String
        Lbl_PRef_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Reinforment Schedules 1.0')
        Lbl_PRef_Text_1.config(font = (Font_1,30))
        Lbl_PRef_Text_1.place(x=aux_width_monitor*.5, y = aux_height_monitor *.5)
        
        #Tiempo
        #img
        #Img_TSesion_Img_1 = Fun_Size(Dir_Images + '/' +'interfaz-11.1.png',.18)
        #Lbl_TSesion_Img_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), image = Img_TSesion_Img_1)
        #Lbl_TSesion_Img_1.place(x=25,y=120)
        #String
        Lbl_TSesion_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal3), text = 'Session Time')
        Lbl_TSesion_Text_1.config(font = (Font_1,20))
        Lbl_TSesion_Text_1.place(x=aux_width_monitor*.75, y = aux_height_monitor *1.8)
        #Box
        Lbl_TSesion_TextBox_1 = tkinter.Text(Main,width = 15, height = 1)
        Lbl_TSesion_TextBox_1.config(font = (Font_1,15))
        Lbl_TSesion_TextBox_1.place(x=aux_width_monitor*3, y = aux_height_monitor *1.9)
        Lbl_TSesion_TextBox_1.insert('end',str(Tiempo_Sesion))
        #String2
        Lbl_TSesion_Text_2 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal3), text = 'sec.')
        Lbl_TSesion_Text_2.config(font = (Font_1,20))
        Lbl_TSesion_Text_2.place(x=aux_width_monitor*5.2, y = aux_height_monitor *1.8)
        
        #%%Programas
        
        #%%Tiempo
        #Accion
        def Fun_Bnt_Pro1():
            if Bnt_Programa1.cget('text') == '0':
                Bnt_Programa1.config(text = '1',bg = Fun_Rgb(C_Pal4))
                Bnt_Programa2.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa3.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa4.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa5.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Lbl_Programa1_TextBox_1.insert('end',str(Pref_Intervalo))
                Lbl_Programa2_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_2.delete('1.0', 'end')
                Lbl_Programa4_TextBox_1.delete('1.0', 'end')
                Lbl_Programa4_TextBox_2.delete('1.0', 'end')
                Lbl_Programa5_TextBox_1.delete('1.0', 'end')
                Lbl_Programa5_TextBox_2.delete('1.0', 'end')
                global PRef_Tipo_Programa
                PRef_Tipo_Programa = 1
            else:
                Bnt_Programa1.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Lbl_Programa1_TextBox_1.delete('1.0', 'end')
        #Imgo
        Img_Programa1 = Fun_Size(Dir_Images + '/' +'interfaz-03.1.png',.2)
        Bnt_Programa1 = tkinter.Button(Main,image = Img_Programa1,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_Pro1)
        Bnt_Programa1.place(x=aux_width_monitor*.75, y = aux_height_monitor *3)
        #String1
        Lbl_Programa1_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Time')
        Lbl_Programa1_Text_1.config(font = (Font_1,20))
        Lbl_Programa1_Text_1.place(x=aux_width_monitor*1.65, y = aux_height_monitor *3.1)
        #Box
        Lbl_Programa1_TextBox_1 = tkinter.Text(Main,width = 40, height = 1)
        Lbl_Programa1_TextBox_1.config(font = (Font_1,20))
        Lbl_Programa1_TextBox_1.place(x=aux_width_monitor*4.25, y = aux_height_monitor *3)
        #String2
        Lbl_Programa1_Text_2 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'seg.')
        Lbl_Programa1_Text_2.config(font = (Font_1,15))
        Lbl_Programa1_Text_2.place(x=aux_width_monitor*11.5, y = aux_height_monitor *3.1)
        
        #%%Distancia
        #Accion
        def Fun_Bnt_Pro2():
            if Bnt_Programa2.cget('text') == '0':
                Bnt_Programa2.config(text = '1',bg = Fun_Rgb(C_Pal4))
                Bnt_Programa1.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa3.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa4.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa5.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Lbl_Programa2_TextBox_1.insert('end',str(Pref_Distancia))
                Lbl_Programa1_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_2.delete('1.0', 'end')
                Lbl_Programa4_TextBox_1.delete('1.0', 'end')
                Lbl_Programa4_TextBox_2.delete('1.0', 'end')
                Lbl_Programa5_TextBox_1.delete('1.0', 'end')
                Lbl_Programa5_TextBox_2.delete('1.0', 'end')
                global PRef_Tipo_Programa
                PRef_Tipo_Programa = 2
            else:
                Bnt_Programa2.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Lbl_Programa2_TextBox_1.delete('1.0', 'end')  
        #Img
        Img_Programa2 = Fun_Size(Dir_Images + '/' +'interfaz-03.1.png',.2)
        Bnt_Programa2 = tkinter.Button(Main,image = Img_Programa2,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_Pro2)
        Bnt_Programa2.place(x=aux_width_monitor*.75, y = aux_height_monitor *4.5)
        #String1
        Lbl_Programa2_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Distance')
        Lbl_Programa2_Text_1.config(font = (Font_1,20))
        Lbl_Programa2_Text_1.place(x=aux_width_monitor*1.65, y = aux_height_monitor *4.6)
        #Box
        Lbl_Programa2_TextBox_1 = tkinter.Text(Main,width = 40, height = 1)
        Lbl_Programa2_TextBox_1.config(font = (Font_1,20))
        Lbl_Programa2_TextBox_1.place(x=aux_width_monitor*4.25, y = aux_height_monitor *4.5)
        #String2
        Lbl_Programa2_Text_2 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'cm.')
        Lbl_Programa2_Text_2.config(font = (Font_1,15))
        Lbl_Programa2_Text_2.place(x=aux_width_monitor*11.5, y = aux_height_monitor *4.6)
        
        #%%Tiempo Distancia
        #Accion
        def Fun_Bnt_Pro3():
            if Bnt_Programa3.cget('text') == '0':
                Bnt_Programa3.config(text = '1',bg = Fun_Rgb(C_Pal4))
                Bnt_Programa1.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa2.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa4.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa5.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Lbl_Programa3_TextBox_1.insert('end',str(Pref_Intervalo))
                Lbl_Programa3_TextBox_2.insert('end',str(Pref_Distancia))
                Lbl_Programa1_TextBox_1.delete('1.0', 'end')
                Lbl_Programa2_TextBox_1.delete('1.0', 'end')
                Lbl_Programa4_TextBox_1.delete('1.0', 'end')
                Lbl_Programa4_TextBox_2.delete('1.0', 'end')
                Lbl_Programa5_TextBox_1.delete('1.0', 'end')
                Lbl_Programa5_TextBox_2.delete('1.0', 'end')
                global PRef_Tipo_Programa
                PRef_Tipo_Programa = 3
            else:
                Bnt_Programa3.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Programa3_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_2.delete('1.0', 'end')
        #Img
        Img_Programa3 = Fun_Size(Dir_Images + '/' +'interfaz-03.1.png',.2)
        Bnt_Programa3 = tkinter.Button(Main,image = Img_Programa3,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_Pro3)
        Bnt_Programa3.place(x=aux_width_monitor*.75, y = aux_height_monitor *6)
        #String1
        Lbl_Programa3_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Time-Distance')
        Lbl_Programa3_Text_1.config(font = (Font_1,20))
        Lbl_Programa3_Text_1.place(x=aux_width_monitor*1.65, y = aux_height_monitor *6.1)
        #Box
        Lbl_Programa3_TextBox_1 = tkinter.Text(Main,width = 18, height = 1)
        Lbl_Programa3_TextBox_1.config(font = (Font_1,20))
        Lbl_Programa3_TextBox_1.place(x=aux_width_monitor*4.25, y = aux_height_monitor *6)
        #String2
        Lbl_Programa3_Text_2 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'seg.')
        Lbl_Programa3_Text_2.config(font = (Font_1,15))
        Lbl_Programa3_Text_2.place(x=aux_width_monitor*7.55, y = aux_height_monitor *6.1)
        #Box
        Lbl_Programa3_TextBox_2 = tkinter.Text(Main,width = 18, height = 1)
        Lbl_Programa3_TextBox_2.config(font = (Font_1,20))
        Lbl_Programa3_TextBox_2.place(x=aux_width_monitor*8.15, y = aux_height_monitor *6)
        #String2
        Lbl_Programa3_Text_3 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'cm.')
        Lbl_Programa3_Text_3.config(font = (Font_1,15))
        Lbl_Programa3_Text_3.place(x=aux_width_monitor*11.5, y = aux_height_monitor *6.1)
        
        
        #%%Distancia Tiempo
        #Accion
        def Fun_Bnt_Pro4():
            if Bnt_Programa4.cget('text') == '0':
                Bnt_Programa4.config(text = '1',bg = Fun_Rgb(C_Pal4))
                Bnt_Programa1.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa2.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa3.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa5.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Lbl_Programa4_TextBox_2.insert('end',str(Pref_Intervalo))
                Lbl_Programa4_TextBox_1.insert('end',str(Pref_Distancia))
                Lbl_Programa1_TextBox_1.delete('1.0', 'end')
                Lbl_Programa2_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_2.delete('1.0', 'end')
                Lbl_Programa5_TextBox_1.delete('1.0', 'end')
                Lbl_Programa5_TextBox_2.delete('1.0', 'end')
                global PRef_Tipo_Programa
                PRef_Tipo_Programa = 4
            else:
                Bnt_Programa4.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Programa4_TextBox_2.delete('1.0', 'end')
                Lbl_Programa4_TextBox_1.delete('1.0', 'end')
        #Img
        Img_Programa4 = Fun_Size(Dir_Images + '/' +'interfaz-03.1.png',.2)
        Bnt_Programa4 = tkinter.Button(Main,image = Img_Programa4,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_Pro4)
        Bnt_Programa4.place(x=aux_width_monitor*.75, y = aux_height_monitor *7.5)
        #String1
        Lbl_Programa4_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Distance-Time')
        Lbl_Programa4_Text_1.config(font = (Font_1,20))
        Lbl_Programa4_Text_1.place(x=aux_width_monitor*1.65, y = aux_height_monitor *7.6)
        #Box
        Lbl_Programa4_TextBox_1 = tkinter.Text(Main,width = 18, height = 1)
        Lbl_Programa4_TextBox_1.config(font = (Font_1,20))
        Lbl_Programa4_TextBox_1.place(x=aux_width_monitor*4.25, y = aux_height_monitor *7.5)
        #String2
        Lbl_Programa4_Text_2 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'cm.')
        Lbl_Programa4_Text_2.config(font = (Font_1,15))
        Lbl_Programa4_Text_2.place(x=aux_width_monitor*7.55, y = aux_height_monitor *7.6)
        #Box
        Lbl_Programa4_TextBox_2 = tkinter.Text(Main,width = 18, height = 1)
        Lbl_Programa4_TextBox_2.config(font = (Font_1,20))
        Lbl_Programa4_TextBox_2.place(x=aux_width_monitor*8.15, y = aux_height_monitor *7.5)
        #String2
        Lbl_Programa3_Text_4 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'seg.')
        Lbl_Programa3_Text_4.config(font = (Font_1,15))
        Lbl_Programa3_Text_4.place(x=aux_width_monitor*11.5, y = aux_height_monitor *7.6)
        
        #%%Place
        #Accion
        def Fun_Bnt_Pro5():
            if Bnt_Programa5.cget('text') == '0':
                Bnt_Programa5.config(text = '1',bg = Fun_Rgb(C_Pal4))
                Bnt_Programa1.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa2.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa3.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa4.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Lbl_Programa5_TextBox_1.insert('end',str(Pref_Cuadrante_Intervalo))
                Lbl_Programa5_TextBox_2.insert('end',str(Pref_Cuadrante))
                Lbl_Programa1_TextBox_1.delete('1.0', 'end')
                Lbl_Programa2_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_2.delete('1.0', 'end')
                Lbl_Programa4_TextBox_1.delete('1.0', 'end')
                Lbl_Programa4_TextBox_2.delete('1.0', 'end')
                global PRef_Tipo_Programa
                PRef_Tipo_Programa = 5
            else:
                Bnt_Programa5.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Programa5_TextBox_2.delete('1.0', 'end')
                Lbl_Programa5_TextBox_1.delete('1.0', 'end')
        #Img
        Img_Programa5 = Fun_Size(Dir_Images + '/' +'interfaz-03.1.png',.2)
        Bnt_Programa5 = tkinter.Button(Main,image = Img_Programa5,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_Pro5)
        Bnt_Programa5.place(x=aux_width_monitor*.75, y = aux_height_monitor *9)
        #String1
        Lbl_Programa5_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Time-Place')
        Lbl_Programa5_Text_1.config(font = (Font_1,20))
        Lbl_Programa5_Text_1.place(x=aux_width_monitor*1.65, y = aux_height_monitor *9.1)
        #Box
        Lbl_Programa5_TextBox_1 = tkinter.Text(Main,width = 18, height = 1)
        Lbl_Programa5_TextBox_1.config(font = (Font_1,20))
        Lbl_Programa5_TextBox_1.place(x=aux_width_monitor*4.25, y = aux_height_monitor *9)
        #String2
        Lbl_Programa5_Text_2 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'seg.')
        Lbl_Programa5_Text_2.config(font = (Font_1,15))
        Lbl_Programa5_Text_2.place(x=aux_width_monitor*7.55, y = aux_height_monitor *9.1)
        #Box
        Lbl_Programa5_TextBox_2 = tkinter.Text(Main,width = 18, height = 1)
        Lbl_Programa5_TextBox_2.config(font = (Font_1,20))
        Lbl_Programa5_TextBox_2.place(x=aux_width_monitor*8.15, y = aux_height_monitor *9)
        #String2
        Lbl_Programa5_Text_4 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'xy.')
        Lbl_Programa5_Text_4.config(font = (Font_1,15))
        Lbl_Programa5_Text_4.place(x=aux_width_monitor*11.5, y = aux_height_monitor *9.1)
        #Posions-
        #P1
        def Fun_Bnt_P1():
            Lbl_Programa5_TextBox_2.delete('1.0', 'end')
            Lbl_Programa5_TextBox_2.insert('end',str((0,0,.5,.5)))
            global Pref_Cuadrante
            Pref_Cuadrante = (0,0,.5,.5)
        Img_Programa5_P1 = Fun_Size(Dir_Images + '/' +'interfaz-12.P1.png',.25)
        Bnt_Programa5_P1 = tkinter.Button(Main,image = Img_Programa5_P1,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2),
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_P1)
        Bnt_Programa5_P1.place(x=aux_width_monitor*8.05,y = aux_height_monitor *10.5)
        #P2
        def Fun_Bnt_P2():
            Lbl_Programa5_TextBox_2.delete('1.0', 'end')
            Lbl_Programa5_TextBox_2.insert('end',str((.5,0,1,.5)))
            global Pref_Cuadrante
            Pref_Cuadrante = (.5,0,1,.5)
        Img_Programa5_P2 = Fun_Size(Dir_Images + '/' +'interfaz-12.P2.png',.25)
        Bnt_Programa5_P2 = tkinter.Button(Main,image = Img_Programa5_P2,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_P2)
        Bnt_Programa5_P2.place(x=aux_width_monitor*8.95,y = aux_height_monitor *10.5)
        #P3
        def Fun_Bnt_P3():
            Lbl_Programa5_TextBox_2.delete('1.0', 'end')
            Lbl_Programa5_TextBox_2.insert('end',str((.5,.5,1,1)))
            global Pref_Cuadrante
            Pref_Cuadrante = (.5,.5,1,1)
        Img_Programa5_P3 = Fun_Size(Dir_Images + '/' +'interfaz-12.P3.png',.25)
        Bnt_Programa5_P3 = tkinter.Button(Main,image = Img_Programa5_P3,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_P3)
        Bnt_Programa5_P3.place(x=aux_width_monitor*9.85,y = aux_height_monitor *10.5)
        #P4
        def Fun_Bnt_P4():
            Lbl_Programa5_TextBox_2.delete('1.0', 'end')
            Lbl_Programa5_TextBox_2.insert('end',str((0,.5,.5,1)))
            global Pref_Cuadrante
            Pref_Cuadrante = (0,.5,.5,1)
        Img_Programa5_P4 = Fun_Size(Dir_Images + '/' +'interfaz-12.P4.png',.25)
        Bnt_Programa5_P4 = tkinter.Button(Main,image = Img_Programa5_P4,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_P4)
        Bnt_Programa5_P4.place(x=aux_width_monitor*10.75,y = aux_height_monitor *10.5)
        #P5
        def Fun_Bnt_P5():
            Lbl_Programa5_TextBox_2.delete('1.0', 'end')
            Lbl_Programa5_TextBox_2.insert('end',str((.25,.25,.75,.75)))
            global Pref_Cuadrante
            Pref_Cuadrante = (.25,.25,.75,.75)
        Img_Programa5_P5 = Fun_Size(Dir_Images + '/' +'interfaz-11.1.png',.25)
        Bnt_Programa5_P5 = tkinter.Button(Main,image = Img_Programa5_P5,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2),
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_P5)
        Bnt_Programa5_P5.place(x=aux_width_monitor*7.15,y = aux_height_monitor *10.5)
        
        #%% Consecuencia
        #Img
        Img_Consecuencia = Fun_Size(Dir_Images + '/' +'interfaz-18.1.png',.18)
        Bnt_Consecuencia = tkinter.Button(Main,image = Img_Consecuencia,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0')
        Bnt_Consecuencia.place(x=aux_width_monitor*.75, y = aux_height_monitor *10.5)
        #String
        Lbl_Consecuencia_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Consequence')
        Lbl_Consecuencia_Text_1.config(font = (Font_1,20))
        Lbl_Consecuencia_Text_1.place(x=aux_width_monitor*1.65, y = aux_height_monitor *10.6)
        #Box
        Lbl_Consecuencia_TextBox_1 = tkinter.Text(Main,width = 10, height = 1)
        Lbl_Consecuencia_TextBox_1.config(font = (Font_1,20))
        Lbl_Consecuencia_TextBox_1.place(x=aux_width_monitor*4.25, y = aux_height_monitor *10.5)
        #String2
        Lbl_Consecuencia_Text_2 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'seg.')
        Lbl_Consecuencia_Text_2.config(font = (Font_1,15))
        Lbl_Consecuencia_Text_2.place(x=aux_width_monitor*6.25, y = aux_height_monitor *10.6)
        #%%Senalar1
        def Fun_Bnt_S1():
            global Pref_Senalar_Intervalo
            if Bnt_Senalar1.cget('text') == '0':
               Bnt_Senalar1.config(text = '1',bg = Fun_Rgb(C_Pal6))
               Lbl_Senalar1_Text_1.config(bg = Fun_Rgb(C_Pal6),fg = Fun_Rgb(C_Pal2))
               Pref_Senalar_Intervalo = 1
            else:
                Bnt_Senalar1.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Senalar1_Text_1.config(bg = Fun_Rgb(C_Pal5),fg = Fun_Rgb(C_Pal2))
                Pref_Senalar_Intervalo = 0
                
        ##Img
        Img_Senalar1 = Fun_Size(Dir_Images + '/' +'interfaz-02.2.png',aux_size-.35)
        Bnt_Senalar1 = tkinter.Button(Main,image = Img_Senalar1,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal5), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_S1)
        Bnt_Senalar1.place(x=aux_width_monitor*12.5, y = aux_height_monitor *3)
        #-String
        Lbl_Senalar1_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'S1')
        Lbl_Senalar1_Text_1.config(font = (Font_1,11))
        Lbl_Senalar1_Text_1.place(x=aux_width_monitor*13.75, y = aux_height_monitor *4.85) 
        
        #Senalar2
        def Fun_Bnt_S2():
            global Pref_Senalar_Distancia
            if Bnt_Senalar2.cget('text') == '0':
               Bnt_Senalar2.config(text = '1',bg = Fun_Rgb(C_Pal6))
               Lbl_Senalar2_Text_1.config(bg = Fun_Rgb(C_Pal6),fg = Fun_Rgb(C_Pal2))
               Pref_Senalar_Distancia = 1
            else:
                Bnt_Senalar2.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Senalar2_Text_1.config(bg = Fun_Rgb(C_Pal5),fg = Fun_Rgb(C_Pal2))
                Pref_Senalar_Distancia = 0
        ##Img
        Bnt_Senalar2 = tkinter.Button(Main,image = Img_Senalar1,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal6),
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_S2)
        Bnt_Senalar2.place(x=aux_width_monitor*12.5, y = aux_height_monitor *5.5)
        #String1
        Lbl_Senalar2_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'S2')
        Lbl_Senalar2_Text_1.config(font = (Font_1,11))
        Lbl_Senalar2_Text_1.place(x=aux_width_monitor*13.75, y = aux_height_monitor *7.25) 
        #Senalar3
        def Fun_Bnt_S3():
            global Pref_Senalar_Cuadrante
            if Bnt_Senalar3.cget('text') == '0':
               Bnt_Senalar3.config(text = '1',bg = Fun_Rgb(C_Pal6))
               Lbl_Senalar3_Text_1.config(bg = Fun_Rgb(C_Pal6),fg = Fun_Rgb(C_Pal2),)
               Pref_Senalar_Cuadrante = 1
            else:
                Bnt_Senalar3.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Senalar3_Text_1.config(bg = Fun_Rgb(C_Pal5),fg = Fun_Rgb(C_Pal2),)
                Pref_Senalar_Cuadrante = 0
        #Img
        Bnt_Senalar3 = tkinter.Button(Main,image = Img_Senalar1,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal6), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_S3)
        Bnt_Senalar3.place(x=aux_width_monitor*12.5, y = aux_height_monitor *8)
        #String1
        Lbl_Senalar3_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'P1')
        Lbl_Senalar3_Text_1.config(font = (Font_1,11))
        Lbl_Senalar3_Text_1.place(x=aux_width_monitor*13.75, y = aux_height_monitor *9.85) 
        #%% Fcambio de ventana
        def onCloseOtherFrame(otherFrame):
            otherFrame.destroy()
            show()
         
        def show():
            Main.update()
            Main.deiconify()       
        
        #%% Sesion nueva
        def Fun_Bnt_Next():
            Main.destroy()
            def Fun_Size(img, size):
                img = Image.open(img)
                size_1 = img.size
                width = int(size_1[0]*size)
                height = int(size_1[1]*size)
                img = img.resize((width, height),Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                return img
            
            global Dir_Images
            
            global Arr_Parametros_track
            
            #Tkinter
            Main_Ses = tkinter.Tk()
            Main_Ses.title('Run experiment')
            Main_Ses.geometry(str(int(aux_width_monitor*8))+'x'+str(height_monitor-100)+'+0+0')
            Main_Ses.configure(background=Fun_Rgb(C_Pal5))
            #canvaz
            Main_Ses_Can = Canvas(Main_Ses, width=round(aux_width_monitor*8), height=round(height_monitor-110), bg=Fun_Rgb(C_Pal5))
            Main_Ses_Can.create_rectangle(10, 10, aux_width_monitor*8 -10, height_monitor-110, outline=Fun_Rgb(C_Pal3), width=4)
            Main_Ses_Can.create_rectangle(120, 250, 520, 650, fill=Fun_Rgb(C_Black), outline=Fun_Rgb(C_Pal6), width=2)
            Main_Ses_Can.place(x=0,y=0)   
        #    #Img1 (Logo)
#            Img_Ses_Main_1 = Fun_Size(Dir_Images + '/' +'interfaz-01.png',.2)
#            Lbl_Ses_Main_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), image = Img_Ses_Main_1)
#            Lbl_Ses_Main_1.place(x=540,y=360) 

            #Tiempo
            #Sujeto
            Lbl_Sujeto_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Subject')
            Lbl_Sujeto_Text_1.config(font = (Font_1,18))
            Lbl_Sujeto_Text_1.place(x=30, y = 20)
            #Box
            Lbl_Sujeto_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
            Lbl_Sujeto_TextBox_1.config(font = (Font_1,15))
            Lbl_Sujeto_TextBox_1.place(x=150, y = 25)
            
            #Sesion
            Lbl_Sesion_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Session')
            Lbl_Sesion_Text_1.config(font = (Font_1,18))
            Lbl_Sesion_Text_1.place(x=30, y = 70)
            #Box
            Lbl_Sesion_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
            Lbl_Sesion_TextBox_1.config(font = (Font_1,15))
            Lbl_Sesion_TextBox_1.place(x=150, y = 75)
            
            #Grupo
            Lbl_Grupo_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Group')
            Lbl_Grupo_Text_1.config(font = (Font_1,18))
            Lbl_Grupo_Text_1.place(x=30, y = 120)
            #Box
            Lbl_Grupo_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
            Lbl_Grupo_TextBox_1.config(font = (Font_1,15))
            Lbl_Grupo_TextBox_1.place(x=150, y = 125)
            
            #Notas
            Lbl_Notas_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Notes')
            Lbl_Notas_Text_1.config(font = (Font_1,18))
            Lbl_Notas_Text_1.place(x=30, y = 170)
            #Box
            Lbl_Notas_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
            Lbl_Notas_TextBox_1.config(font = (Font_1,15))
            Lbl_Notas_TextBox_1.place(x=150, y = 175)
                    

            
            def Fun_Run():
                global Tiempo_Sesion, C_Final_Sesion, PRef_Tipo_Programa, Pref_Intervalo, Pref_Senalar_Intervalo, Pref_Distancia, Pref_Senalar_Distancia, Pref_Cuadrante_Intervalo, Pref_Senalar_Cuadrante, Pref_Cuadrante, Pref_Tiempo_Consecuencia
                
                global Arr_Parametros_track
                
                global Str_Sujeto, Str_Sesion, Str_Grupo, Str_Notas, Dir_Archivo_Datos
                Str_Sujeto = Lbl_Sujeto_TextBox_1.get('1.0','end-1c')
                Str_Sesion = Lbl_Sesion_TextBox_1.get('1.0','end-1c')
                Str_Grupo = Lbl_Grupo_TextBox_1.get('1.0','end-1c')
                Str_Notas = Lbl_Notas_TextBox_1.get('1.0','end-1c')
                
                #Variables Programa
                
                C_Intervalo = 1
                if Pref_Intervalo[-1] == -1:
                    Pref_Intervalo = Pref_Intervalo[:-1]
                    C_Intervalo = 0
                    
                C_Distancia = 1
                if Pref_Distancia[-1] == -1:
                    Pref_Distancia = Pref_Distancia[:-1]
                    C_Distancia = 0
                
                C_Cuadrante = 1
                if Pref_Cuadrante_Intervalo[-1] == -1:
                    Pref_Cuadrante_Intervalo = Pref_Cuadrante_Intervalo[:-1]
                    C_Cuadrante = 0
                elif Pref_Cuadrante_Intervalo[-1] == -2:
                    Pref_Cuadrante_Intervalo = Pref_Cuadrante_Intervalo[:-1]
                    C_Cuadrante = 2
                elif Pref_Cuadrante_Intervalo[-1] == -3:
                    Pref_Cuadrante_Intervalo = Pref_Cuadrante_Intervalo[:-1]
                    C_Cuadrante = 3
                    
                        
                
                #Programas Reforzamiento
                Arr_Control_Consecuencia = np.zeros(5)
                Arr_Contador_Consecuencia = np.zeros(5)
                Arr_Control_Senales = np.zeros(4)
                Int_Contador_Intervalo = 0
                Int_Contador_Distancia = 0
                Int_Contador_Cuadrante = 0
                Int_Contador_Velocidad = 0
                
                if C_Intervalo == 0:
                    Contador_Valor_Intervalo = 0; 
                    Pref_Intervalo = np.random.permutation(Pref_Intervalo)
                    Int_Valor_Intervalo = Pref_Intervalo[Contador_Valor_Intervalo]
                else:    
                    Int_Valor_Intervalo = random.choice(Pref_Intervalo)
                    
                if C_Distancia == 0:
                    Contador_Valor_Distancia = 0; 
                    Pref_Distancia = np.random.permutation(Pref_Distancia)
                    Int_Valor_Distancia = Pref_Intervalo[Contador_Valor_Distancia]
                else:    
                    Int_Valor_Distancia = random.choice(Pref_Distancia)  
                    
                if C_Cuadrante == 2:
                    Contador_Cuadrante_Intervalo = 0; 
                    Pref_Cuadrante_Intervalo = np.random.permutation(Pref_Cuadrante_Intervalo)
                    Int_Valor_Cuadrante = Pref_Intervalo[Contador_Cuadrante_Intervalo]
                else:    
                    Int_Valor_Cuadrante = random.choice(Pref_Cuadrante_Intervalo)    
               
                
                
                
                
                x_control = 1
                #Datos
                Int_Contador = 1
                global int_Tipo_Programa, Int_Contador_Consecuencia
                int_Tipo_Programa = 0
                Int_Datos_Consecuencia = 0
                Arr_TiempoReal = np.zeros(4)
                Int_Contador_Consecuencia = 0
                global Mat_Datos
                Mat_Datos = np.zeros((9999999,7))
                Mat_Datos[:,0] = -1
        
                #Funciones
                def Fun_Distancia(x1,x2,y1,y2,DistanciaRelativa):
                    return math.sqrt((x2-x1)**2+(y2-y1)**2)*DistanciaRelativa
        
                #CamaraWeb
                Dev_WebCam_Read = cv2.VideoCapture(int(Arr_Parametros_track[0]))
                Dev_WebCam_Resolution = int(Arr_Parametros_track[1])
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
        
                #Arduino
                Arduino = serial.Serial(Arduino_Com)
                Var_Save_video = Var_Radiobutton.get()
                
                if Var_Save_video != 1:
                    Var_Save_video = 0
                
                global Nombre_Archivo, Ruta_Video, Ruta_Carpeta_Imagenes
                
                fourcc = cv2.VideoWriter_fourcc(*'MP4V')
                out = cv2.VideoWriter(Dir_Videos + Str_Sujeto + '.mp4',fourcc, 30.0, (640,480))
                
                
                
                    
                
                Arr_TiempoReal[0]=time.time() 
                Int_Contador_Consecuencia = 0;
                
                while((int(Tiempo_Sesion) >= Arr_TiempoReal[3]) or (int(Consecuencias_Sesion)-1 >= Int_Contador_Consecuencia)):
                    
                    
                    ret, Img_WebCam = Dev_WebCam_Read.read()
                    
                    if ret==True and Var_Save_video == 1:
                        out.write(Img_WebCam)
                    
                    
                    #Tranformar Imagen
                    num_rows, num_cols = Img_WebCam.shape[:2]
                    Mat_Img_Rotada = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), Arr_ImgConfig[4], 1)
                    Img_WebCam  = cv2.warpAffine(Img_WebCam, Mat_Img_Rotada, (num_cols, num_rows))
                    Img_WebCam = Img_WebCam[round(Img_WebCam.shape[0]*Arr_ImgConfig[2]):round(Img_WebCam.shape[0]*Arr_ImgConfig[3]),
                                                round(Img_WebCam.shape[1]*Arr_ImgConfig[0]):round(Img_WebCam.shape[1]*Arr_ImgConfig[1])]
                    
                    
                    
                    
                    #Seleccio de color
                    Mat_WebCam_RGB = np.zeros((Img_WebCam.shape))
                    Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,2]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[0]+Mat_RGB[3])))[0]),
                                   (np.where((Img_WebCam[:,:,2]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[0]+Mat_RGB[3])))[1]),0] = 1
                    Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[0]),
                                   (np.where((Img_WebCam[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[1]),1] = 1
                    Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,0]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[2]+Mat_RGB[3])))[0]),
                                   (np.where((Img_WebCam[:,:,0]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[2]+Mat_RGB[3])))[1]),2] = 1          
                    Img_WebCam = Mat_WebCam_RGB  
                                
                    #Filtro Imagen
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
                    
                    
                
                    #PLot
                    try:
                        Mat_Centroide = ndimage.label(Img_WebCam)[0]
                        Centroide = scipy.ndimage.measurements.center_of_mass(Img_WebCam, Mat_Centroide, [1,2,3,4,5])
                        Mat_Size = ndimage.label(Img_WebCam)[0]
                        Size = np.sqrt(scipy.ndimage.measurements.sum(Img_WebCam, Mat_Size, [1,2,3,4,5]))
                        MinSize = int(np.where(Size == np.min(Size[(Size >= Track_MinSize)]))[0])
                        cv2.circle(Img_WebCam,(int(Centroide[MinSize][1]),int(Centroide[MinSize][0])),2,(0,0,255),3)
                    except:
                        Img_WebCam = Img_WebCam
        
                        
                    if PRef_Tipo_Programa == 5:
                        cv2.rectangle(Img_WebCam,(round(Pref_Cuadrante[0]*Img_WebCam.shape[1]),round(Pref_Cuadrante[1]*Img_WebCam.shape[0])),
                                                 (round(Pref_Cuadrante[2]*Img_WebCam.shape[1]),round(Pref_Cuadrante[3]*Img_WebCam.shape[0])),
                                                 (255,255,255),1)
                        
                    #Programas Reforzamiento
                    #---Intervalo---
                    if PRef_Tipo_Programa == 1:
                        if Int_Contador_Intervalo  >= Int_Valor_Intervalo:
                            if C_Intervalo == 0:
                                Contador_Valor_Intervalo+=1    
                                if Contador_Valor_Intervalo >= Pref_Intervalo.size:
                                    Contador_Valor_Intervalo = 0
                                    Pref_Intervalo = np.random.permutation(Pref_Intervalo)
                                Int_Valor_Intervalo = Pref_Intervalo[Contador_Valor_Intervalo]    
                            else:        
                                Int_Valor_Intervalo = random.choice(Pref_Intervalo)
                            Int_Contador_Intervalo = 0
                            Arr_Control_Consecuencia[0] = 1
                        else:
                            int_Tipo_Programa = 1
                    #---Distancia---        
                    elif PRef_Tipo_Programa == 2:
                        
                        if Int_Contador_Distancia  >= Int_Valor_Distancia:
                            if C_Distancia == 0:
                                Contador_Valor_Distancia+=1    
                                if Contador_Valor_Distancia >= Pref_Distancia.size:
                                    Contador_Valor_Distancia = 0
                                    Pref_Distancia = np.random.permutation(Pref_Distancia)
                                Int_Valor_Distancia = Pref_Distancia[Contador_Valor_Distancia]    
                            else:        
                                Int_Valor_Distancia = random.choice(Pref_Distancia)
                            Int_Contador_Distancia = 0
                            Arr_Control_Consecuencia[0] = 1
                        else:
                            int_Tipo_Programa = 2
                    #---Intervalo-Distancia---        
                    elif PRef_Tipo_Programa == 3:
                        if Int_Contador_Intervalo  < Int_Valor_Intervalo:
                            Int_Contador_Distancia = 0
                            int_Tipo_Programa = 1
                            if Arr_Control_Senales[1] == 0:
                                Arr_Control_Senales[1] = 1
                            if Arr_Control_Senales[2] == 2:
                                Arr_Control_Senales[2] = 3
                        if Int_Contador_Intervalo  >= Int_Valor_Intervalo:
                            int_Tipo_Programa = 2
                            if Arr_Control_Senales[1] == 2:
                                Arr_Control_Senales[1] = 3
                            if Arr_Control_Senales[2] == 0:
                                Arr_Control_Senales[2] = 1
                            if Int_Contador_Distancia  >= Int_Valor_Distancia:
                                
                                if C_Intervalo == 0:
                                    Contador_Valor_Intervalo+=1    
                                    if Contador_Valor_Intervalo >= Pref_Intervalo.size:
                                        Contador_Valor_Intervalo = 0
                                        Pref_Intervalo = np.random.permutation(Pref_Intervalo)
                                    Int_Valor_Intervalo = Pref_Intervalo[Contador_Valor_Intervalo]    
                                else:        
                                    Int_Valor_Intervalo = random.choice(Pref_Intervalo)
                                Int_Contador_Intervalo = 0
                                
                                if C_Distancia == 0:
                                    Contador_Valor_Distancia+=1    
                                    if Contador_Valor_Distancia >= Pref_Distancia.size:
                                        Contador_Valor_Distancia = 0
                                        Pref_Distancia = np.random.permutation(Pref_Distancia)
                                    Int_Valor_Distancia = Pref_Distancia[Contador_Valor_Distancia]    
                                else:        
                                    Int_Valor_Distancia = random.choice(Pref_Distancia)
                                Int_Contador_Distancia = 0
                                
                                Arr_Control_Consecuencia[0] = 1
                            
                    #---Distancia-Intervalo----        
                    elif PRef_Tipo_Programa == 4:
                        if Int_Contador_Distancia  < Int_Valor_Distancia:
                            Int_Contador_Intervalo = 0
                            int_Tipo_Programa = 2
                            if Arr_Control_Senales[1] == 0:
                                Arr_Control_Senales[1] = 1
                            if Arr_Control_Senales[2] == 2:
                                Arr_Control_Senales[2] = 3
                        if Int_Contador_Distancia  >= Int_Valor_Distancia:
                            int_Tipo_Programa = 1
                            if Arr_Control_Senales[1] == 2:
                                Arr_Control_Senales[1] = 3
                            if Arr_Control_Senales[2] == 0:
                                Arr_Control_Senales[2] = 1
                            if Int_Contador_Intervalo  >= Int_Valor_Intervalo:
                                
                                if C_Intervalo == 0:
                                    Contador_Valor_Intervalo+=1    
                                    if Contador_Valor_Intervalo >= Pref_Intervalo.size:
                                        Contador_Valor_Intervalo = 0
                                        Pref_Intervalo = np.random.permutation(Pref_Intervalo)
                                    Int_Valor_Intervalo = Pref_Intervalo[Contador_Valor_Intervalo]    
                                else:        
                                    Int_Valor_Intervalo = random.choice(Pref_Intervalo)
                                Int_Contador_Intervalo = 0
                                
                                if C_Distancia == 0:
                                    Contador_Valor_Distancia+=1    
                                    if Contador_Valor_Distancia >= Pref_Distancia.size:
                                        Contador_Valor_Distancia = 0
                                        Pref_Distancia = np.random.permutation(Pref_Distancia)
                                    Int_Valor_Distancia = Pref_Distancia[Contador_Valor_Distancia]    
                                else:        
                                    Int_Valor_Distancia = random.choice(Pref_Distancia)
                                Int_Contador_Distancia = 0
                                
                                Arr_Control_Consecuencia[0] = 1
                                
                    #---Permanecia Cuadrante----        
                    elif PRef_Tipo_Programa == 5:
                        try:
                            if (int(Centroide[MinSize][1]) >= int(round(Pref_Cuadrante[0]*Img_WebCam.shape[1]))) &\
                               (int(Centroide[MinSize][1]) <= int(round(Pref_Cuadrante[2]*Img_WebCam.shape[1]))) &\
                               (int(Centroide[MinSize][0]) >= int(round(Pref_Cuadrante[1]*Img_WebCam.shape[0]))) &\
                               (int(Centroide[MinSize][0]) <= int(round(Pref_Cuadrante[3]*Img_WebCam.shape[0]))):
                                Int_Contador_Cuadrante+=Arr_TiempoReal[2]
                                int_Tipo_Programa = 3
                                if Arr_Control_Senales[3] == 0:
                                    Arr_Control_Senales[3] = 1
                                if Int_Contador_Cuadrante  >= Int_Valor_Cuadrante:
                                    Int_Valor_Cuadrante = random.choice(Pref_Cuadrante_Intervalo)
                                    Int_Contador_Cuadrante = 0
                                    Arr_Control_Consecuencia[0] = 1
                                    if Arr_Control_Senales[3] == 2:
                                        Arr_Control_Senales[3] = 3
                            else:
                                int_Tipo_Programa = 5
                                if (C_Cuadrante == 1) | (C_Cuadrante == 2):
                                    Int_Contador_Cuadrante = 0
                                if Arr_Control_Senales[3] == 2:
                                    Arr_Control_Senales[3] = 3
                        except:
                            Int_Contador_Cuadrante = Int_Contador_Cuadrante
                            
                            
                    Img_WebCam = cv2.resize(Img_WebCam,(400, round((400/Img_WebCam.shape[1])*Img_WebCam.shape[1])))
                    
                    if C_Final_Sesion == 1:
                        cv2.putText(Img_WebCam,'C: ',(5,15),Font_CV, .5,(255,255,255),1)
                        cv2.putText(Img_WebCam,str(Int_Contador_Consecuencia),(20,15),Font_CV, .5,(255,255,255),1)
                    else:
                        cv2.putText(Img_WebCam,'T: ',(5,15),Font_CV, .5,(255,255,255),1)
                        cv2.putText(Img_WebCam,str(round((Arr_TiempoReal[3]) ,2)),(20,15),Font_CV, .5,(255,255,255),1)
                    cv2.putText(Img_WebCam,'I: ',(5,35),Font_CV, .5,(255,255,255),1)
                    cv2.putText(Img_WebCam,str(round(Int_Contador_Intervalo ,2)),(20,35),Font_CV, .5,(255,255,255),1)
                    cv2.putText(Img_WebCam,'D: ',(5,55),Font_CV, .5,(255,255,255),1)
                    cv2.putText(Img_WebCam,str(round(Int_Contador_Distancia ,2)),(20,55),Font_CV, .5,(255,255,255),1)
                    cv2.putText(Img_WebCam,'C: ',(5,75),Font_CV, .5,(255,255,255),1)
                    cv2.putText(Img_WebCam,str(round(Int_Contador_Cuadrante ,2)),(20,75),Font_CV, .5,(255,255,255),1)
                    cv2.imshow('Tracking',Img_WebCam)
                    cv2.moveWindow('Tracking', 120,250);
                                       
                    #Arduino   
                    #---SeñalIntervalo---
                    if Pref_Senalar_Intervalo == 1:
                        if PRef_Tipo_Programa == 1:
                            if Arr_Control_Senales[0] == 1:
                                Arduino.write(b'd')
                                Arr_Control_Senales[0] = 2
                            if Arr_Control_Senales[0] == 0:
                                if x_control == 1:
                                    Arduino.write(b'c')
                                    x_control = 0
                                int_Tipo_Programa = 1
                        if (PRef_Tipo_Programa == 3):    
                            if (Arr_Control_Senales[1] == 1) & (Arr_Control_Senales[0] == 0):
                                Arduino.write(b'c')
                                int_Tipo_Programa = 1
                                Arr_Control_Senales[1] = 2
                            if Arr_Control_Senales[1] == 3:
                                Arduino.write(b'd')
                                Arr_Control_Senales[1] = 0
                        if (PRef_Tipo_Programa == 4):    
                            if (Arr_Control_Senales[1] == 1) & (Arr_Control_Senales[0] == 0):
                                Arduino.write(b'c')
                                int_Tipo_Programa = 1
                                Arr_Control_Senales[1] = 2
                            if Arr_Control_Senales[1] == 3:
                                Arduino.write(b'd')
                                Arr_Control_Senales[1] = 0
                    #---SeñalDistancia---
                    if Pref_Senalar_Distancia == 1:
                        if PRef_Tipo_Programa == 2:
                            if Arr_Control_Senales[0] == 1:
                                Arduino.write(b'f')
                                Arr_Control_Senales[0] = 2
                            if Arr_Control_Senales[0] == 0:
                                if x_control == 1:
                                    Arduino.write(b'e')
                                    x_control = 0
                                int_Tipo_Programa = 2
                        if (PRef_Tipo_Programa == 3):    
                            if (Arr_Control_Senales[2] == 1) & (Arr_Control_Senales[0] == 0):
                                Arduino.write(b'e')
                                int_Tipo_Programa = 2
                                Arr_Control_Senales[2] = 2
                            if Arr_Control_Senales[2] == 3:
                                Arduino.write(b'f')
                                Arr_Control_Senales[2] = 0
                        if (PRef_Tipo_Programa == 4):    
                            if (Arr_Control_Senales[2] == 1) & (Arr_Control_Senales[0] == 0):
                                Arduino.write(b'e')
                                int_Tipo_Programa = 2
                                Arr_Control_Senales[2] = 2
                            if Arr_Control_Senales[2] == 3:
                                Arduino.write(b'f')
                                Arr_Control_Senales[2] = 0
                    #---SeñalIntervalo---
                    if Pref_Senalar_Cuadrante == 1:
                        if PRef_Tipo_Programa == 5:
                            if (C_Cuadrante == 3):
                                if (Arr_Control_Senales[3] == 1) & (Arr_Control_Senales[0] == 0):
                                    if (Arr_Control_Consecuencia[0] == 1) & (C_Cuadrante == 3):
                                        Arduino.write(b'e')
                                    else:
                                        Arduino.write(b'c')
                                    int_Tipo_Programa = 3
                                    Arr_Control_Senales[3] = 2
                                if Arr_Control_Senales[3] == 3:
                                    if (Arr_Control_Consecuencia[0] == 1) & (C_Cuadrante == 3):
                                        Arduino.write(b'e')
                                    else:
                                        Arduino.write(b'd')
                                    Arr_Control_Senales[3] = 0
                            else:
                                if (Arr_Control_Senales[3] == 1): #& (Arr_Control_Senales[0] == 0):
                                    Arduino.write(b'c')
                                    int_Tipo_Programa = 3
                                    Arr_Control_Senales[3] = 2
                                if Arr_Control_Senales[3] == 3:
                                    Arduino.write(b'd')
                                    Arr_Control_Senales[3] = 0
                    #---Consecuencia---
                    if Arr_Control_Consecuencia[0] == 1:
                        if Arr_Contador_Consecuencia[0] == 0:
                            Arr_Contador_Consecuencia[0]+=Arr_TiempoReal[2]
                            Arduino.write(b'a')
                            int_Tipo_Programa = 0
                            Arr_Control_Senales[0] = 1
                            Int_Datos_Consecuencia = 1
                            x_control = 1
                        elif Arr_Contador_Consecuencia[0] >= Pref_Tiempo_Consecuencia[0]:
                            Arr_Contador_Consecuencia[0] = 0
                            Arr_Control_Consecuencia[0] = 0
                            Arr_Control_Senales[0] = 0
                            Int_Datos_Consecuencia = 0
                            if C_Final_Sesion == 1:
                                Int_Contador_Consecuencia += 1;
                            Arduino.write(b'b')
                        else:
                            Arr_Contador_Consecuencia[0]+=Arr_TiempoReal[2]
                            Arr_Control_Senales[0] = 2  
                            Int_Contador_Intervalo = 0 
                            Int_Contador_Distancia = 0
                            Int_Contador_Cuadrante = 0
                                
                    
                    
                    Mat_Datos[Int_Contador][0] = Arr_TiempoReal[3]
                    try:
                        Mat_Datos[Int_Contador][1] = int(Centroide[MinSize][1])
                        Mat_Datos[Int_Contador][2] = int(Centroide[MinSize][0])
                    except:
                        Mat_Datos[Int_Contador][1] = Mat_Datos[Int_Contador-1][1]
                        Mat_Datos[Int_Contador][2] = Mat_Datos[Int_Contador-1][2]
                    Mat_Datos[Int_Contador][4] = Int_Datos_Consecuencia
                    if Int_Contador == 1:
                        Mat_Datos[Int_Contador][3] = 0
                    else:    
                        Mat_Datos[Int_Contador][3] = (Fun_Distancia(Mat_Datos[Int_Contador-1][1],Mat_Datos[Int_Contador][1],Mat_Datos[Int_Contador-1][2],Mat_Datos[Int_Contador][2],Dev_Espacio_Tamano/int(Arr_Parametros_track[15])))
                    Mat_Datos[Int_Contador][5] = int_Tipo_Programa
                    
                    Int_Contador += 1
                    
                    #Relog
                    Arr_TiempoReal[1]=time.time()
                    Arr_TiempoReal[2]=Arr_TiempoReal[1]-Arr_TiempoReal[0] 
                    Arr_TiempoReal[3]+= Arr_TiempoReal[2]
                    Int_Contador_Intervalo+=Arr_TiempoReal[2]
                    
                    #Distancia
                    Int_Contador_Distancia += Mat_Datos[Int_Contador-1][3]
                    Mat_Datos[Int_Contador-1][6] = (Mat_Datos[Int_Contador-1][3]/100) / Arr_TiempoReal[2]
                    Arr_TiempoReal[0]=time.time()
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
          
                Dev_WebCam_Read.release()
                cv2.destroyAllWindows()
                Mat_Datos = np.delete(Mat_Datos,np.where(Mat_Datos[:,0] == -1), axis=0)
                Mat_Datos[0,3] = 0
                Mat_Datos[0,6] = 0
                
                Arduino.write(b'b')
                Arduino.write(b'd')
                Arduino.write(b'f')
                Arduino.write(b'h')
                Arduino.write(b'j')
                Arduino.close()
                    
                                
                
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
                                    
                
                #Datos                
                Nombre_Grafico =  filedialog.asksaveasfilename(initialdir = Dir_Datos,
                                                                            title = "Save Data",
                                                                            filetypes = (("all files","*.*"), ("txt files","*.txt"))) 
                i = 1
                Archivo_Mat_Datos = open(Nombre_Grafico + '.txt','w')
                Archivo_Mat_Datos.write('Subject: ' + Str_Sujeto + '\n' +
                                        'Session: ' + Str_Sesion + '\n' +
                                        'Group: ' + Str_Grupo + '\n' +
                                        'Time: '+ str(max(Mat_Datos[:,0])) + '\n' +
                                        '# Consecuences: ' + str(np.size(np.where(Mat_Datos[:,4] == 1))) + '\n' +
                                        'Distance: ' + str(round(sum(Mat_Datos[:,3]),3)) + 'cm' + '\n' +
                                        'Velocity: ' + str(round(sum(Mat_Datos[:,3])/max(Mat_Datos[:,0]),3)) + 'cm/seg' + '\n' +
                                        'Mean Aceleration: ' + str(round(statistics.mean(Mat_Datos[:,5]),3)) + 'm/seg' + '\n' +
                                        '\n' + 'Frame;Time;X;Y;Aceleration;Distance;Consecuences;Signal' + '\n')
                for i in range(0,len(Mat_Datos)): 
                    Archivo_Mat_Datos.write(str(i) + ',' + str(round(Mat_Datos[i][0],3)) +
                                                     ',' + str(round(Mat_Datos[i][1] * (Dev_Espacio_Tamano/int(Arr_Parametros_track[15])),3)) +
                                                     ',' + str(round(Mat_Datos[i][2] * (Dev_Espacio_Tamano/int(Arr_Parametros_track[16])),3)) +
                                                     ',' + str(round(Mat_Datos[i][3],3)) +
                                                     ',' + str(Mat_Datos[i][4]) + ';' + str(Mat_Datos[i][5]) +
                                                     ',' + str(round(Mat_Datos[i][6],3)) + '\n')
        
                Archivo_Mat_Datos.close() 
                messagebox.showinfo("Finalized", "End Sesion")
#                Main_Ses.destroy()
              
            #Cerrar
            Lbl_Save_Text = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Save video')
            Lbl_Save_Text.config(font = (Font_1,14))
            Lbl_Save_Text.place(x=aux_width_monitor*6.1, y = aux_height_monitor*10.2)
            
            Var_Radiobutton = tkinter.IntVar(Main_Ses)
            radiobutton1 = tkinter.Radiobutton(Main_Ses, text='', bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), 
                                               activebackground=Fun_Rgb(C_Pal4),
                                               highlightbackground=Fun_Rgb(C_Pal5), variable=Var_Radiobutton, value=1)
            radiobutton1.config(font = (Font_1,24))
            radiobutton1.place(x=aux_width_monitor*7.2, y = aux_height_monitor*10.05)
            Var_Radiobutton.get()
            #Bnt Next
            Bnt_Next = tkinter.Button(Main_Ses, bd=0, fg = Fun_Rgb(C_Pal5),
                                      bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                      highlightbackground=Fun_Rgb(C_Pal5),
                                      text = '  Run  ', command = Fun_Run)
            Bnt_Next.config(font = (Font_1,25))
            Bnt_Next.place(x=aux_width_monitor*6.1, y = aux_height_monitor*11)
            
            Main.mainloop()
            
        
        
            
        Bnt_Next = tkinter.Button(Main, bd=0, fg = Fun_Rgb(C_Pal5),
                                  bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                  highlightbackground=Fun_Rgb(C_Pal5),
                                  text = '   Next   ', command = Fun_Bnt_Next)
        Bnt_Next.config(font = (Font_1,25))
        Bnt_Next.place(x=aux_width_monitor*12.5, y = aux_height_monitor *11)
        
        Main.mainloop()
        

#%%Programas Reforzamiento
    def Fun_Programas_Ref2():
        ventanaMenuPrincipal.destroy()
        
        #Configuracion
        global Dir_Archivo_Parametros, Arr_Parametros_track, Arr_Parametros_Pref, Dir_Archivo_Datos
        Txt_Imagen = open(Dir_Archivo_Parametros +'Image.txt','r')
        Arr_Parametros_track = Txt_Imagen.read().split('\n')
        Txt_Imagen.close()
        Txt_Pref = open(Dir_Archivo_Parametros +'PRef.txt','r')
        Arr_Parametros_Pref = Txt_Pref.read().split('\n')
        Txt_Pref.close()
        
        #rogramas Reforzamiento
        global PRef_Tipo_Programa, Pref_Intervalo, Pref_Senalar_Intervalo, Pref_Distancia, Pref_Senalar_Distancia, Pref_Cuadrante_Intervalo, Pref_Senalar_Cuadrante, Pref_Cuadrante, Pref_Tiempo_Consecuencia, Tiempo_Sesion
        PRef_Tipo_Programa = int(Arr_Parametros_Pref[0])
        Pref_Intervalo = literal_eval(Arr_Parametros_Pref[1])
        Pref_Senalar_Intervalo = int(Arr_Parametros_Pref[2])
        Pref_Distancia = literal_eval(Arr_Parametros_Pref[3])
        Pref_Senalar_Distancia = int(Arr_Parametros_Pref[4])
        Pref_Cuadrante_Intervalo = literal_eval(Arr_Parametros_Pref[5])
        Pref_Senalar_Cuadrante = int(Arr_Parametros_Pref[6])
        Pref_Cuadrante = literal_eval(Arr_Parametros_Pref[7])
        Pref_Tiempo_Consecuencia = literal_eval(Arr_Parametros_Pref[8])
        Tiempo_Sesion = int(Arr_Parametros_Pref[9])
        
        #magen + traking
        global Dev_WebCam, Dev_WebCam_Resolution, Arr_ImgConfig,  Mat_RGB, Img_Filtro, Track_MinSize, Size_Proportion, Dev_Espacio_Tamano
        Dev_WebCam = int(Arr_Parametros_track[0])
        Dev_WebCam_Resolution = int(Arr_Parametros_track[1])
        Arr_ImgConfig = (float(Arr_Parametros_track[2]),float(Arr_Parametros_track[3]),float(Arr_Parametros_track[4]),float(Arr_Parametros_track[5]),int(Arr_Parametros_track[6]),0,1) #X1,X2,Y1,Y2,Grados,AaumentarReducir,Porcentaje
        Dev_Espacio_Tamano = int(Arr_Parametros_track[7])
        Size_Proportion = int(Arr_Parametros_track[15])
        Mat_RGB = ([int(Arr_Parametros_track[8]),int(Arr_Parametros_track[9]),int(Arr_Parametros_track[10]),int(Arr_Parametros_track[11]),float(Arr_Parametros_track[12])])
        Img_Filtro = int(Arr_Parametros_track[13])
        Track_MinSize = float(Arr_Parametros_track[14])
        
        #Arduino
        global Arduino_Com
        Arduino_Com = Arr_Parametros_Pref[10]
        
        #Sesion
        global Str_Sujeto, Str_Sesion, Str_Grupo, Str_Notas
        Str_Sujeto = ' '
        Str_Sesion = ' '
        Str_Grupo = ' '
        Str_Notas = ' '
        
        #Save programas reforzamiento
        global Arr_Variables_Pref
        
        
        
        #%%Funciones
        
        def Fun_Rgb(RGB):
            return "#%02x%02x%02x" % RGB  
         
        def Fun_Size(img, size):
            img = Image.open(img)
            size_1 = img.size
            width = int(size_1[0]*size)
            height = int(size_1[1]*size)
            img = img.resize((width, height),Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            return img
        

        
        #%%Menu Save programas reforzamiento
        def Fun_Save_PRef():
            global Arr_Variables_Pref, Tiempo_Sesion, PRef_Tipo_Programa, Pref_Intervalo, Pref_Senalar_Intervalo, Pref_Distancia, Pref_Senalar_Distancia, Pref_Cuadrante_Intervalo, Pref_Senalar_Cuadrante, Pref_Cuadrante, Pref_Tiempo_Consecuencia
            if PRef_Tipo_Programa == 1:
                Pref_Intervalo = Lbl_Programa1_TextBox_1.get('1.0','end-1c')
                Pref_Distancia = '(0,)'
                Pref_Senalar_Distancia = '0'
                Pref_Cuadrante_Intervalo = '(0,)'
                Pref_Senalar_Cuadrante = '0'
                Pref_Cuadrante = '(0,0,0,0)'
            elif PRef_Tipo_Programa == 2:
                Pref_Distancia = Lbl_Programa2_TextBox_1.get('1.0','end-1c')
                Pref_Intervalo = '(0,)'
                Pref_Senalar_Intervalo = '0'
                Pref_Cuadrante_Intervalo = '(0,)'
                Pref_Senalar_Cuadrante = '0'
                Pref_Cuadrante = '(0,0,0,0)'
            elif PRef_Tipo_Programa == 3:
                Pref_Intervalo = Lbl_Programa3_TextBox_1.get('1.0','end-1c')
                Pref_Distancia = Lbl_Programa3_TextBox_2.get('1.0','end-1c')
                Pref_Cuadrante_Intervalo = '(0,)'
                Pref_Senalar_Cuadrante = '0'
                Pref_Cuadrante = '(0,0,0,0)'
            elif PRef_Tipo_Programa == 4:
                Pref_Intervalo = Lbl_Programa4_TextBox_2.get('1.0','end-1c')
                Pref_Distancia = Lbl_Programa4_TextBox_1.get('1.0','end-1c')
                Pref_Cuadrante_Intervalo = '(0,)'
                Pref_Senalar_Cuadrante = '0'
                Pref_Cuadrante = '(0,0,0,0)'
            elif PRef_Tipo_Programa == 5:
                Pref_Cuadrante_Intervalo = Lbl_Programa5_TextBox_1.get('1.0','end-1c')
                Pref_Cuadrante = Lbl_Programa5_TextBox_2.get('1.0','end-1c')
                Pref_Distancia = '(0,)'
                Pref_Senalar_Distancia = '0'
                Pref_Intervalo = '(0,)'
                Pref_Senalar_Intervalo = '0'
            Pref_Tiempo_Consecuencia = (int(Lbl_Consecuencia_TextBox_1.get('1.0','end-1c')),0,0,0,0)
            Tiempo_Sesion = Lbl_TSesion_TextBox_1.get('1.0','end-1c')
            global Arr_Variables_Pref
            
            Arr_Variables_Pref = [str(PRef_Tipo_Programa),
                                  str(Pref_Intervalo), str(Pref_Senalar_Intervalo),
                                  str(Pref_Distancia),str(Pref_Senalar_Distancia),
                                  str(Pref_Cuadrante_Intervalo),str(Pref_Senalar_Cuadrante),str(Pref_Cuadrante),
                                  str(Pref_Tiempo_Consecuencia), str(Tiempo_Sesion), Arduino_Com, Temp_Txt_Image]
            
            
            Main.Ruta_Carpeta_Proyecto =  filedialog.asksaveasfilename(initialdir = Dir_Archivo_PRef,
                                                                       title = "Save file",
                                                                       filetypes = (("all files","*.*"), ("txt","*.txt")))
            
            Archivo_Vaariables = open(Main.Ruta_Carpeta_Proyecto + '.txt','w')
            for i in Arr_Variables_Pref:
                Archivo_Vaariables.write(i +'\n')            
            Archivo_Vaariables.close()
            
            
            
        #%%Menu Open programas reforzamiento    
        def Fun_Open_PRef():
            
            #Reset Values
            global Arr_Variables_Pref, Tiempo_Sesion, PRef_Tipo_Programa, Pref_Intervalo, Pref_Senalar_Intervalo, Pref_Distancia, Pref_Senalar_Distancia, Pref_Cuadrante_Intervalo, Pref_Senalar_Cuadrante, Pref_Cuadrante, Pref_Tiempo_Consecuencia
            Pref_Senalar_Intervalo = '(0,)'
            Pref_Distancia = '(0,)'
            Pref_Senalar_Intervalo = '0'
            Pref_Senalar_Distancia = '0'
            Pref_Cuadrante_Intervalo = '(0,)'
            Pref_Senalar_Cuadrante = '0'
            Pref_Cuadrante = '(0,0,0,0)'
            Pref_Senalar_Intervalo = 0
            Pref_Senalar_Distancia = 0
            Pref_Senalar_Cuadrante = 0
            PRef_Tipo_Programa = 0
                
            global Dir_Archivo_Parametros, Arr_Parametros_Pref, Arduino_Com
            Main.Txt_Pref = filedialog.askopenfilename(initialdir = Dir_Archivo_PRef,
                                                    title = "Select file",
                                                    filetypes = (("txt","*.txt"),
                                                    ("all files","*.*")))
            Dir_Archivo_Parametros = open(Main.Txt_Pref, 'r')
            Arr_Parametros_Pref = Dir_Archivo_Parametros.read().split('\n')
            
            Lbl_Consecuencia_TextBox_1.delete('1.0', 'end')
            Lbl_TSesion_TextBox_1.delete('1.0', 'end')
            
            global Tiempo_Sesion, Final_Sesion, C_Final_Sesion, Consecuencias_Sesion
            try:
                if Arr_Parametros_Pref[9].split(',')[1] == '-1':
                    Tiempo_Sesion = 0
                    Consecuencias_Sesion = int(Arr_Parametros_Pref[9].split(',')[0])
                    C_Final_Sesion = 1
            except:
                Tiempo_Sesion = int(Arr_Parametros_Pref[9])
                Consecuencias_Sesion = 0
                C_Final_Sesion = 0
            PRef_Tipo_Programa = int(Arr_Parametros_Pref[0])
            Pref_Intervalo = literal_eval(Arr_Parametros_Pref[1])
            Pref_Senalar_Intervalo = int(Arr_Parametros_Pref[2])
            Pref_Distancia = literal_eval(Arr_Parametros_Pref[3])
            Pref_Senalar_Distancia = int(Arr_Parametros_Pref[4])
            Pref_Cuadrante_Intervalo = literal_eval(Arr_Parametros_Pref[5])
            Pref_Senalar_Cuadrante = int(Arr_Parametros_Pref[6])
            Pref_Cuadrante = literal_eval(Arr_Parametros_Pref[7])
            Pref_Tiempo_Consecuencia = literal_eval(Arr_Parametros_Pref[8])
            Arduino_Com = Arr_Parametros_Pref[10]
            
            if Pref_Senalar_Intervalo == 1:
               Bnt_Senalar1.config(text = '1',bg = Fun_Rgb(C_Pal2))
               Lbl_Senalar1_Text_1.config(bg = Fun_Rgb(C_Pal2),fg = Fun_Rgb(C_Pal5))
            else:
                Bnt_Senalar1.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Senalar1_Text_1.config(bg = Fun_Rgb(C_Pal5),fg = Fun_Rgb(C_Pal2))
            if Pref_Senalar_Distancia == 1:
               Bnt_Senalar2.config(text = '1',bg = Fun_Rgb(C_Pal2))
               Lbl_Senalar2_Text_1.config(bg = Fun_Rgb(C_Pal2),fg = Fun_Rgb(C_Pal5))
            else:
                Bnt_Senalar2.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Senalar2_Text_1.config(bg = Fun_Rgb(C_Pal5),fg = Fun_Rgb(C_Pal2))
            Lbl_Consecuencia_TextBox_1.insert('end',str(Pref_Tiempo_Consecuencia[0]))
            Lbl_TSesion_TextBox_1.insert('end',str(Tiempo_Sesion))
            
            if PRef_Tipo_Programa == 1:
                Fun_Bnt_Pro1()    
            elif PRef_Tipo_Programa == 3:
                Fun_Bnt_Pro3()    
            elif PRef_Tipo_Programa == 4:
                Fun_Bnt_Pro4() 
            else:
                Lbl_Programa3_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_2.delete('1.0', 'end')
                Lbl_Programa4_TextBox_1.delete('1.0', 'end')
                Lbl_Programa4_TextBox_2.delete('1.0', 'end')
                
            
            global Arr_Parametros_track
            
            Dir_Archivo_Parametros = open(Arr_Parametros_Pref[11], 'r')
            Arr_Parametros_track = Dir_Archivo_Parametros.read().split('\n')
            #Dispositivos
            global Dev_WebCam, Dev_WebCam_Resolution
            Dev_WebCam = int(Arr_Parametros_track[0])
            Dev_WebCam_Resolution = int(Arr_Parametros_track[1])
            #Imagen
            global Arr_ImgConfig
            Arr_ImgConfig = (float(Arr_Parametros_track[2]),float(Arr_Parametros_track[3]),float(Arr_Parametros_track[4]),float(Arr_Parametros_track[5]),int(Arr_Parametros_track[6]),0,1) #X1,X2,Y1,Y2,Grados,AaumentarReducir,Porcentaje
            #Traking
            global Mat_RGB, Img_Filtro, Track_MinSize, Dev_Espacio_Tamano, Size_Proportion
            Mat_RGB = ([int(Arr_Parametros_track[8]),int(Arr_Parametros_track[9]),int(Arr_Parametros_track[10]),int(Arr_Parametros_track[11]),float(Arr_Parametros_track[12])])
            Img_Filtro = int(Arr_Parametros_track[13])
            Track_MinSize = float(Arr_Parametros_track[14])
            Dev_Espacio_Tamano = int(Arr_Parametros_track[7])
            Size_Proportion = int(Arr_Parametros_track[15])
                    
            
            
            
            
            
        #%%Menu Open traking parameters
        def Fun_O_ImageParameters():
            global Dir_Archivo_Parametros, Arr_Parametros_track, Temp_Txt_Image
            Main.Txt_Imagen = filedialog.askopenfilename(initialdir = Dir_Proyecto,
                                                    title = "Select file",
                                                    filetypes = (("txt","*.txt"),
                                                    ("all files","*.*")))
            Temp_Txt_Image = Main.Txt_Imagen
            Dir_Archivo_Parametros = open(Main.Txt_Imagen, 'r')
            Arr_Parametros_track = Dir_Archivo_Parametros.read().split('\n')
            #Dispositivos
            global Dev_WebCam, Dev_WebCam_Resolution
            Dev_WebCam = int(Arr_Parametros_track[0])
            Dev_WebCam_Resolution = int(Arr_Parametros_track[1])
            #Imagen
            global Arr_ImgConfig
            Arr_ImgConfig = (float(Arr_Parametros_track[2]),float(Arr_Parametros_track[3]),float(Arr_Parametros_track[4]),float(Arr_Parametros_track[5]),int(Arr_Parametros_track[6]),0,1) #X1,X2,Y1,Y2,Grados,AaumentarReducir,Porcentaje
            #Traking
            global Mat_RGB, Img_Filtro, Track_MinSize, Dev_Espacio_Tamano, Size_Proportion
            Mat_RGB = ([int(Arr_Parametros_track[8]),int(Arr_Parametros_track[9]),int(Arr_Parametros_track[10]),int(Arr_Parametros_track[11]),float(Arr_Parametros_track[12])])
            Img_Filtro = int(Arr_Parametros_track[13])
            Track_MinSize = float(Arr_Parametros_track[14])
            Dev_Espacio_Tamano = int(Arr_Parametros_track[7])
            Size_Proportion = int(Arr_Parametros_track[15])
            
            
                
        #%%Main
        Main = tkinter.Tk()
        Main.title('Reinforcement Schedules 2.0')
        Main.geometry(str(width_monitor)+'x'+str(height_monitor-100)+'+0+0')
        Main.configure(background=Fun_Rgb(C_Pal5))
        #Fondo
        Main_Can = Canvas(width=width_monitor, height=height_monitor-110, bg=Fun_Rgb(C_Pal5))
        Main_Can.create_rectangle(10, 10, width_monitor-10, height_monitor-120, outline=Fun_Rgb(C_Pal3), width=4)
        Main_Can.place(x=0,y=0)  
        
        
        
        #%%Control Menu
        Main_Menu = tkinter.Menu(Main)
        Main.config(menu=Main_Menu)
        #File
        Main_Menu_Opc1 = tkinter.Menu(Main_Menu, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                                     activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Pal2),
                                     tearoff=0)                         
        Main_Menu.add_cascade(label="File", menu=Main_Menu_Opc1)
        Main_Menu_Opc1.add_command(label='Save Schedule', command=Fun_Save_PRef)
        Main_Menu_Opc1.add_command(label='Open schedule', command=Fun_Open_PRef)   
        #Preferences
        Main_Menu_Opc2 = tkinter.Menu(Main_Menu, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                                     activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Pal2),
                                     tearoff=0)                           
        Main_Menu.add_cascade(label='Preferences', menu=Main_Menu_Opc2)
        Main_Menu_Opc2.add_command(label='Image', command=Fun_O_ImageParameters)
        #Com
        Main_Menu_Opc3 = tkinter.Menu(Main_Menu_Opc2, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
                                     activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Pal2),
                                     tearoff=0)              
                    
        Main_Menu_Opc2.add_cascade(label='Serial Port', menu=Main_Menu_Opc3) 
        
        Serial_Port = list(serial.tools.list_ports.comports())
        
        def Fun_GetSerial(PortCom):
            global Arduino_Com
            Arduino_Com = Port_String[PortCom]
        
        
        Port_String = list(('','','','',''))
        for i in range(0,len(Serial_Port)):
            Port_String[i] = Serial_Port[i].device
            Port_String_Des = Serial_Port[i].description
            Main_Menu_Opc3.add_command(label=(Port_String_Des),command=lambda PortCom=i: Fun_GetSerial(PortCom))
            
            
            
        #%%Programas Reforzamiento Widgets
            
        #-String
        Lbl_PRef_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Reinforment Schedules 2.0')
        Lbl_PRef_Text_1.config(font = (Font_1,30))
        Lbl_PRef_Text_1.place(x=aux_width_monitor*.5, y = aux_height_monitor *.5)
        
        #Tiempo
        #img
        #Img_TSesion_Img_1 = Fun_Size(Dir_Images + '/' +'interfaz-11.1.png',.18)
        #Lbl_TSesion_Img_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), image = Img_TSesion_Img_1)
        #Lbl_TSesion_Img_1.place(x=25,y=120)
        #String
        Lbl_TSesion_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal3), text = 'Session Time')
        Lbl_TSesion_Text_1.config(font = (Font_1,20))
        Lbl_TSesion_Text_1.place(x=aux_width_monitor*.75, y = aux_height_monitor *1.8)
        #Box
        Lbl_TSesion_TextBox_1 = tkinter.Text(Main,width = 15, height = 1)
        Lbl_TSesion_TextBox_1.config(font = (Font_1,15))
        Lbl_TSesion_TextBox_1.place(x=aux_width_monitor*3, y = aux_height_monitor *1.9)
        Lbl_TSesion_TextBox_1.insert('end',str(Tiempo_Sesion))
        #String2
        Lbl_TSesion_Text_2 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal3), text = 'sec.')
        Lbl_TSesion_Text_2.config(font = (Font_1,20))
        Lbl_TSesion_Text_2.place(x=aux_width_monitor*5.2, y = aux_height_monitor *1.8)
        
        #%%Programas
        
        #%%Tiempo
        #Accion
        def Fun_Bnt_Pro1():
            if Bnt_Programa1.cget('text') == '0':
                Bnt_Programa1.config(text = '1',bg = Fun_Rgb(C_Pal4))
                Bnt_Programa3.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa4.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Lbl_Programa1_TextBox_1.insert('end',str(Pref_Intervalo))
                Lbl_Programa3_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_2.delete('1.0', 'end')
                Lbl_Programa4_TextBox_1.delete('1.0', 'end')
                Lbl_Programa4_TextBox_2.delete('1.0', 'end')
                global PRef_Tipo_Programa
                PRef_Tipo_Programa = 1
            else:
                Bnt_Programa1.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Lbl_Programa1_TextBox_1.delete('1.0', 'end')
        #Imgo
        Img_Programa1 = Fun_Size(Dir_Images + '/' +'interfaz-03.1.png',.2)
        Bnt_Programa1 = tkinter.Button(Main,image = Img_Programa1,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_Pro1)
        Bnt_Programa1.place(x=aux_width_monitor*.75, y = aux_height_monitor *3)
        #String1
        Lbl_Programa1_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Velocity')
        Lbl_Programa1_Text_1.config(font = (Font_1,20))
        Lbl_Programa1_Text_1.place(x=aux_width_monitor*1.65, y = aux_height_monitor *3.1)
        #Box
        Lbl_Programa1_TextBox_1 = tkinter.Text(Main,width = 38, height = 1)
        Lbl_Programa1_TextBox_1.config(font = (Font_1,20))
        Lbl_Programa1_TextBox_1.place(x=aux_width_monitor*4.6, y = aux_height_monitor *3)
        #String2
        Lbl_Programa1_Text_2 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'cm/seg')
        Lbl_Programa1_Text_2.config(font = (Font_1,15))
        Lbl_Programa1_Text_2.place(x=aux_width_monitor*11.5, y = aux_height_monitor *3.1)
        

        #%%Tiempo Distancia
        #Accion
        def Fun_Bnt_Pro3():
            if Bnt_Programa3.cget('text') == '0':
                Bnt_Programa3.config(text = '1',bg = Fun_Rgb(C_Pal4))
                Bnt_Programa1.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa4.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Lbl_Programa3_TextBox_1.insert('end',str(Pref_Intervalo))
                Lbl_Programa3_TextBox_2.insert('end',str(Pref_Distancia))
                Lbl_Programa1_TextBox_1.delete('1.0', 'end')
                Lbl_Programa4_TextBox_1.delete('1.0', 'end')
                Lbl_Programa4_TextBox_2.delete('1.0', 'end')
                global PRef_Tipo_Programa
                PRef_Tipo_Programa = 3
            else:
                Bnt_Programa3.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Programa3_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_2.delete('1.0', 'end')
        #Img
        Img_Programa3 = Fun_Size(Dir_Images + '/' +'interfaz-03.1.png',.2)
        Bnt_Programa3 = tkinter.Button(Main,image = Img_Programa3,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_Pro3)
        Bnt_Programa3.place(x=aux_width_monitor*.75, y = aux_height_monitor *4.5)
        #String1
        Lbl_Programa3_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Time-Time')
        Lbl_Programa3_Text_1.config(font = (Font_1,20))
        Lbl_Programa3_Text_1.place(x=aux_width_monitor*1.65, y = aux_height_monitor *4.6)
        #Box
        Lbl_Programa3_TextBox_1 = tkinter.Text(Main,width = 14, height = 1)
        Lbl_Programa3_TextBox_1.config(font = (Font_1,20))
        Lbl_Programa3_TextBox_1.place(x=aux_width_monitor*4.6, y = aux_height_monitor *4.5)
        #String2
        Lbl_Programa3_Text_2 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'seg.')
        Lbl_Programa3_Text_2.config(font = (Font_1,15))
        Lbl_Programa3_Text_2.place(x=aux_width_monitor*7.55, y = aux_height_monitor *4.6)
        #Box
        Lbl_Programa3_TextBox_2 = tkinter.Text(Main,width = 18, height = 1)
        Lbl_Programa3_TextBox_2.config(font = (Font_1,20))
        Lbl_Programa3_TextBox_2.place(x=aux_width_monitor*8.15, y = aux_height_monitor *4.5)
        #String2
        Lbl_Programa3_Text_3 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'seg.')
        Lbl_Programa3_Text_3.config(font = (Font_1,15))
        Lbl_Programa3_Text_3.place(x=aux_width_monitor*11.5, y = aux_height_monitor *4.6)
        
        
        #%%Distancia Tiempo
        #Accion
        def Fun_Bnt_Pro4():
            if Bnt_Programa4.cget('text') == '0':
                Bnt_Programa4.config(text = '1',bg = Fun_Rgb(C_Pal4))
                Bnt_Programa1.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Bnt_Programa3.config(text = '0',bg = Fun_Rgb(C_Pal5))
                Lbl_Programa4_TextBox_2.insert('end',str(Pref_Intervalo))
                Lbl_Programa4_TextBox_1.insert('end',str(Pref_Distancia))
                Lbl_Programa1_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_1.delete('1.0', 'end')
                Lbl_Programa3_TextBox_2.delete('1.0', 'end')
                global PRef_Tipo_Programa
                PRef_Tipo_Programa = 4
            else:
                Bnt_Programa4.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Programa4_TextBox_2.delete('1.0', 'end')
                Lbl_Programa4_TextBox_1.delete('1.0', 'end')
        #Img
        Img_Programa4 = Fun_Size(Dir_Images + '/' +'interfaz-03.1.png',.2)
        Bnt_Programa4 = tkinter.Button(Main,image = Img_Programa4,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_Pro4)
        Bnt_Programa4.place(x=aux_width_monitor*.75, y = aux_height_monitor *6)
        #String1
        Lbl_Programa4_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Distance-Distance')
        Lbl_Programa4_Text_1.config(font = (Font_1,20))
        Lbl_Programa4_Text_1.place(x=aux_width_monitor*1.65, y = aux_height_monitor *6.1)
        #Box
        Lbl_Programa4_TextBox_1 = tkinter.Text(Main,width = 16, height = 1)
        Lbl_Programa4_TextBox_1.config(font = (Font_1,20))
        Lbl_Programa4_TextBox_1.place(x=aux_width_monitor*4.6, y = aux_height_monitor *6)
        #String2
        Lbl_Programa4_Text_2 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'cm.')
        Lbl_Programa4_Text_2.config(font = (Font_1,15))
        Lbl_Programa4_Text_2.place(x=aux_width_monitor*7.55, y = aux_height_monitor *6.1)
        #Box
        Lbl_Programa4_TextBox_2 = tkinter.Text(Main,width = 18, height = 1)
        Lbl_Programa4_TextBox_2.config(font = (Font_1,20))
        Lbl_Programa4_TextBox_2.place(x=aux_width_monitor*8.15, y = aux_height_monitor *6)
        #String2
        Lbl_Programa3_Text_4 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'cm.')
        Lbl_Programa3_Text_4.config(font = (Font_1,15))
        Lbl_Programa3_Text_4.place(x=aux_width_monitor*11.5, y = aux_height_monitor *6.1)
        
        
        #%% Consecuencia
        #Img
        Img_Consecuencia = Fun_Size(Dir_Images + '/' +'interfaz-18.1.png',.18)
        Bnt_Consecuencia = tkinter.Button(Main,image = Img_Consecuencia,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0')
        Bnt_Consecuencia.place(x=aux_width_monitor*.75, y = aux_height_monitor *10.5)
        #String
        Lbl_Consecuencia_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Consequence')
        Lbl_Consecuencia_Text_1.config(font = (Font_1,20))
        Lbl_Consecuencia_Text_1.place(x=aux_width_monitor*1.65, y = aux_height_monitor *10.6)
        #Box
        Lbl_Consecuencia_TextBox_1 = tkinter.Text(Main,width = 10, height = 1)
        Lbl_Consecuencia_TextBox_1.config(font = (Font_1,20))
        Lbl_Consecuencia_TextBox_1.place(x=aux_width_monitor*4.25, y = aux_height_monitor *10.5)
        #String2
        Lbl_Consecuencia_Text_2 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'seg.')
        Lbl_Consecuencia_Text_2.config(font = (Font_1,15))
        Lbl_Consecuencia_Text_2.place(x=aux_width_monitor*6.25, y = aux_height_monitor *10.6)
        #%%Senalar1
        def Fun_Bnt_S1():
            global Pref_Senalar_Intervalo
            if Bnt_Senalar1.cget('text') == '0':
               Bnt_Senalar1.config(text = '1',bg = Fun_Rgb(C_Pal6))
               Lbl_Senalar1_Text_1.config(bg = Fun_Rgb(C_Pal6),fg = Fun_Rgb(C_Pal2))
               Pref_Senalar_Intervalo = 1
            else:
                Bnt_Senalar1.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Senalar1_Text_1.config(bg = Fun_Rgb(C_Pal5),fg = Fun_Rgb(C_Pal2))
                Pref_Senalar_Intervalo = 0
                
        ##Img
        Img_Senalar1 = Fun_Size(Dir_Images + '/' +'interfaz-02.2.png',aux_size-.35)
        Bnt_Senalar1 = tkinter.Button(Main,image = Img_Senalar1,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal5), 
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_S1)
        Bnt_Senalar1.place(x=aux_width_monitor*12.5, y = aux_height_monitor *3)
        #-String
        Lbl_Senalar1_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'S1')
        Lbl_Senalar1_Text_1.config(font = (Font_1,11))
        Lbl_Senalar1_Text_1.place(x=aux_width_monitor*13.75, y = aux_height_monitor *4.85) 
        
        #Senalar2
        def Fun_Bnt_S2():
            global Pref_Senalar_Distancia
            if Bnt_Senalar2.cget('text') == '0':
               Bnt_Senalar2.config(text = '1',bg = Fun_Rgb(C_Pal6))
               Lbl_Senalar2_Text_1.config(bg = Fun_Rgb(C_Pal6),fg = Fun_Rgb(C_Pal2))
               Pref_Senalar_Distancia = 1
            else:
                Bnt_Senalar2.config(text = '0',bg = Fun_Rgb(C_Pal5))  
                Lbl_Senalar2_Text_1.config(bg = Fun_Rgb(C_Pal5),fg = Fun_Rgb(C_Pal2))
                Pref_Senalar_Distancia = 0
        ##Img
        Bnt_Senalar2 = tkinter.Button(Main,image = Img_Senalar1,  bd=0, 
                                             bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal6),
                                             highlightbackground = Fun_Rgb(C_Pal5),
                                             text = '0', command = Fun_Bnt_S2)
        Bnt_Senalar2.place(x=aux_width_monitor*12.5, y = aux_height_monitor *5.5)
        #String1
        Lbl_Senalar2_Text_1 = tkinter.Label(Main, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'S2')
        Lbl_Senalar2_Text_1.config(font = (Font_1,11))
        Lbl_Senalar2_Text_1.place(x=aux_width_monitor*13.75, y = aux_height_monitor *7.25) 

        #%% Fcambio de ventana
        def onCloseOtherFrame(otherFrame):
            otherFrame.destroy()
            show()
         
        def show():
            Main.update()
            Main.deiconify()       
        
        #%% Sesion nueva
        def Fun_Bnt_Next():
            Main.destroy()
            def Fun_Size(img, size):
                img = Image.open(img)
                size_1 = img.size
                width = int(size_1[0]*size)
                height = int(size_1[1]*size)
                img = img.resize((width, height),Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                return img
            
            global Dir_Images
            
            global Arr_Parametros_track
            
            #Tkinter
            Main_Ses = tkinter.Tk()
            Main_Ses.title('Run experiment')
            Main_Ses.geometry(str(int(aux_width_monitor*8))+'x'+str(height_monitor-100)+'+0+0')
            Main_Ses.configure(background=Fun_Rgb(C_Pal5))
            #canvaz
            Main_Ses_Can = Canvas(Main_Ses, width=round(aux_width_monitor*8), height=round(height_monitor-110), bg=Fun_Rgb(C_Pal5))
            Main_Ses_Can.create_rectangle(10, 10, aux_width_monitor*8 -10, height_monitor-110, outline=Fun_Rgb(C_Pal3), width=4)
            Main_Ses_Can.create_rectangle(120, 250, 520, 650, fill=Fun_Rgb(C_Black), outline=Fun_Rgb(C_Pal6), width=2)
            Main_Ses_Can.place(x=0,y=0)   
        #    #Img1 (Logo)
#            Img_Ses_Main_1 = Fun_Size(Dir_Images + '/' +'interfaz-01.png',.2)
#            Lbl_Ses_Main_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), image = Img_Ses_Main_1)
#            Lbl_Ses_Main_1.place(x=540,y=360) 

            #Tiempo
            #Sujeto
            Lbl_Sujeto_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Subject')
            Lbl_Sujeto_Text_1.config(font = (Font_1,18))
            Lbl_Sujeto_Text_1.place(x=30, y = 20)
            #Box
            Lbl_Sujeto_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
            Lbl_Sujeto_TextBox_1.config(font = (Font_1,15))
            Lbl_Sujeto_TextBox_1.place(x=150, y = 25)
            
            #Sesion
            Lbl_Sesion_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Session')
            Lbl_Sesion_Text_1.config(font = (Font_1,18))
            Lbl_Sesion_Text_1.place(x=30, y = 70)
            #Box
            Lbl_Sesion_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
            Lbl_Sesion_TextBox_1.config(font = (Font_1,15))
            Lbl_Sesion_TextBox_1.place(x=150, y = 75)
            
            #Grupo
            Lbl_Grupo_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Group')
            Lbl_Grupo_Text_1.config(font = (Font_1,18))
            Lbl_Grupo_Text_1.place(x=30, y = 120)
            #Box
            Lbl_Grupo_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
            Lbl_Grupo_TextBox_1.config(font = (Font_1,15))
            Lbl_Grupo_TextBox_1.place(x=150, y = 125)
            
            #Notas
            Lbl_Notas_Text_1 = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Notes')
            Lbl_Notas_Text_1.config(font = (Font_1,18))
            Lbl_Notas_Text_1.place(x=30, y = 170)
            #Box
            Lbl_Notas_TextBox_1 = tkinter.Text(Main_Ses,width = 40, height = 1)
            Lbl_Notas_TextBox_1.config(font = (Font_1,15))
            Lbl_Notas_TextBox_1.place(x=150, y = 175)
                    

            
            def Fun_Run():
                global Tiempo_Sesion, C_Final_Sesion, PRef_Tipo_Programa, Pref_Intervalo, Pref_Senalar_Intervalo, Pref_Distancia, Pref_Senalar_Distancia, Pref_Cuadrante_Intervalo, Pref_Senalar_Cuadrante, Pref_Cuadrante, Pref_Tiempo_Consecuencia, Int_Contador_Velocidad
                
                global Arr_Parametros_track
                
                global Str_Sujeto, Str_Sesion, Str_Grupo, Str_Notas, Dir_Archivo_Datos
                Str_Sujeto = Lbl_Sujeto_TextBox_1.get('1.0','end-1c')
                Str_Sesion = Lbl_Sesion_TextBox_1.get('1.0','end-1c')
                Str_Grupo = Lbl_Grupo_TextBox_1.get('1.0','end-1c')
                Str_Notas = Lbl_Notas_TextBox_1.get('1.0','end-1c')
                
                #Variables Programa
                
                C_Intervalo = 1
                if Pref_Intervalo[-1] == -1:
                    Pref_Intervalo = Pref_Intervalo[:-1]
                    C_Intervalo = 0
                    
                C_Distancia = 1
                if Pref_Distancia[-1] == -1:
                    Pref_Distancia = Pref_Distancia[:-1]
                    C_Distancia = 0
                
                C_Cuadrante = 1
                if Pref_Cuadrante_Intervalo[-1] == -1:
                    Pref_Cuadrante_Intervalo = Pref_Cuadrante_Intervalo[:-1]
                    C_Cuadrante = 0
                elif Pref_Cuadrante_Intervalo[-1] == -2:
                    Pref_Cuadrante_Intervalo = Pref_Cuadrante_Intervalo[:-1]
                    C_Cuadrante = 2
                    
                        
                
                #Programas Reforzamiento
                Arr_Control_Consecuencia = np.zeros(5)
                Arr_Contador_Consecuencia = np.zeros(5)
                Arr_Control_Senales = np.zeros(4)
                Int_Contador_Intervalo = 0
                Int_Contador_Distancia = 0
                Int_Contador_Intervalo2 = 0
                Int_Contador_Distancia2 = 0
                Int_Contador_Cuadrante = 0
                Int_Contador_Velocidad = 0
                
                if C_Intervalo == 0:
                    Contador_Valor_Intervalo = 0; 
                    Pref_Intervalo = np.random.permutation(Pref_Intervalo)
                    Int_Valor_Intervalo = Pref_Intervalo[Contador_Valor_Intervalo]
                else:    
                    Int_Valor_Intervalo = random.choice(Pref_Intervalo)
                    
                if C_Distancia == 0:
                    Contador_Valor_Distancia = 0; 
                    Pref_Distancia = np.random.permutation(Pref_Distancia)
                    Int_Valor_Distancia = Pref_Intervalo[Contador_Valor_Distancia]
                else:    
                    Int_Valor_Distancia = random.choice(Pref_Distancia)  
                    
                if C_Cuadrante == 2:
                    Contador_Cuadrante_Intervalo = 0; 
                    Pref_Cuadrante_Intervalo = np.random.permutation(Pref_Cuadrante_Intervalo)
                    Int_Valor_Cuadrante = Pref_Intervalo[Contador_Cuadrante_Intervalo]
                else:    
                    Int_Valor_Cuadrante = random.choice(Pref_Cuadrante_Intervalo)    
               
                
                
                
                
                x_control = 1
                #Datos
                Int_Contador = 1
                global int_Tipo_Programa, Int_Contador_Consecuencia
                int_Tipo_Programa = 0
                Int_Datos_Consecuencia = 0
                Arr_TiempoReal = np.zeros(4)
                Int_Contador_Consecuencia = 0
                global Mat_Datos
                Mat_Datos = np.zeros((9999999,7))
                Mat_Datos[:,0] = -1
        
                #Funciones
                def Fun_Distancia(x1,x2,y1,y2,DistanciaRelativa):
                    return math.sqrt((x2-x1)**2+(y2-y1)**2)*DistanciaRelativa
        
                #CamaraWeb
                Dev_WebCam_Read = cv2.VideoCapture(int(Arr_Parametros_track[0]))
                Dev_WebCam_Resolution = int(Arr_Parametros_track[1])
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
        
                #Arduino
                Arduino = serial.Serial(Arduino_Com)
                Var_Save_video = Var_Radiobutton.get()
                
                if Var_Save_video != 1:
                    Var_Save_video = 0
                
                global Nombre_Archivo, Ruta_Video, Ruta_Carpeta_Imagenes
                
                fourcc = cv2.VideoWriter_fourcc(*'MP4V')
                out = cv2.VideoWriter(Dir_Videos + Str_Sujeto + '.mp4',fourcc, 30.0, (640,480))
                
                
                
                    
                
                Arr_TiempoReal[0]=time.time() 
                Int_Contador_Consecuencia = 0;
                
                while((int(Tiempo_Sesion) >= Arr_TiempoReal[3]) or (int(Consecuencias_Sesion)-1 >= Int_Contador_Consecuencia)):
                    
                    
                    ret, Img_WebCam = Dev_WebCam_Read.read()
                    
                    if ret==True and Var_Save_video == 1:
                        out.write(Img_WebCam)
                    
                    
                    #Tranformar Imagen
                    num_rows, num_cols = Img_WebCam.shape[:2]
                    Mat_Img_Rotada = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), Arr_ImgConfig[4], 1)
                    Img_WebCam  = cv2.warpAffine(Img_WebCam, Mat_Img_Rotada, (num_cols, num_rows))
                    Img_WebCam = Img_WebCam[round(Img_WebCam.shape[0]*Arr_ImgConfig[2]):round(Img_WebCam.shape[0]*Arr_ImgConfig[3]),
                                                round(Img_WebCam.shape[1]*Arr_ImgConfig[0]):round(Img_WebCam.shape[1]*Arr_ImgConfig[1])]
                    
                    
                    
                    
                    #Seleccio de color
                    Mat_WebCam_RGB = np.zeros((Img_WebCam.shape))
                    Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,2]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[0]+Mat_RGB[3])))[0]),
                                   (np.where((Img_WebCam[:,:,2]>=(Mat_RGB[0]-Mat_RGB[3])) & (Img_WebCam[:,:,2]<=(Mat_RGB[0]+Mat_RGB[3])))[1]),0] = 1
                    Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[0]),
                                   (np.where((Img_WebCam[:,:,1]>=(Mat_RGB[1]-Mat_RGB[3])) & (Img_WebCam[:,:,1]<=(Mat_RGB[1]+Mat_RGB[3])))[1]),1] = 1
                    Mat_WebCam_RGB[(np.where((Img_WebCam[:,:,0]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[2]+Mat_RGB[3])))[0]),
                                   (np.where((Img_WebCam[:,:,0]>=(Mat_RGB[2]-Mat_RGB[3])) & (Img_WebCam[:,:,0]<=(Mat_RGB[2]+Mat_RGB[3])))[1]),2] = 1          
                    Img_WebCam = Mat_WebCam_RGB  
                                
                    #Filtro Imagen
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
                    
                    
                
                    #PLot
                    try:
                        Mat_Centroide = ndimage.label(Img_WebCam)[0]
                        Centroide = scipy.ndimage.measurements.center_of_mass(Img_WebCam, Mat_Centroide, [1,2,3,4,5])
                        Mat_Size = ndimage.label(Img_WebCam)[0]
                        Size = np.sqrt(scipy.ndimage.measurements.sum(Img_WebCam, Mat_Size, [1,2,3,4,5]))
                        MinSize = int(np.where(Size == np.min(Size[(Size >= Track_MinSize)]))[0])
                        cv2.circle(Img_WebCam,(int(Centroide[MinSize][1]),int(Centroide[MinSize][0])),2,(0,0,255),3)
                    except:
                        Img_WebCam = Img_WebCam
        
                        
                    if PRef_Tipo_Programa == 5:
                        cv2.rectangle(Img_WebCam,(round(Pref_Cuadrante[0]*Img_WebCam.shape[1]),round(Pref_Cuadrante[1]*Img_WebCam.shape[0])),
                                                 (round(Pref_Cuadrante[2]*Img_WebCam.shape[1]),round(Pref_Cuadrante[3]*Img_WebCam.shape[0])),
                                                 (255,255,255),1)
                        
                    #Programas Reforzamiento
                    #---Intervalo---
                    if PRef_Tipo_Programa == 1:
                        if Int_Contador_Velocidad  >= Int_Valor_Intervalo:
                            if C_Intervalo == 0:
                                Contador_Valor_Intervalo+=1    
                                if Contador_Valor_Intervalo >= Pref_Intervalo.size:
                                    Contador_Valor_Intervalo = 0
                                    Pref_Intervalo = np.random.permutation(Pref_Intervalo)
                                Int_Valor_Intervalo = Pref_Intervalo[Contador_Valor_Intervalo]    
                            else:        
                                Int_Contador_Velocidad = random.choice(Pref_Intervalo)
                            Int_Contador_Intervalo = 0
                            Arr_Control_Consecuencia[0] = 1
                        else:
                            int_Tipo_Programa = 1
                    #---Distancia---        
                    elif PRef_Tipo_Programa == 2:
                        
                        if Int_Contador_Distancia  >= Int_Valor_Distancia:
                            if C_Distancia == 0:
                                Contador_Valor_Distancia+=1    
                                if Contador_Valor_Distancia >= Pref_Distancia.size:
                                    Contador_Valor_Distancia = 0
                                    Pref_Distancia = np.random.permutation(Pref_Distancia)
                                Int_Valor_Distancia = Pref_Distancia[Contador_Valor_Distancia]    
                            else:        
                                Int_Valor_Distancia = random.choice(Pref_Distancia)
                            Int_Contador_Distancia = 0
                            Arr_Control_Consecuencia[0] = 1
                        else:
                            int_Tipo_Programa = 2
                    #---Intervalo-Distancia---        
                    elif PRef_Tipo_Programa == 3:
                        if Int_Contador_Intervalo  < Int_Valor_Intervalo:
                            Int_Contador_Intervalo2 = 0
                            int_Tipo_Programa = 1
                            if Arr_Control_Senales[1] == 0:
                                Arr_Control_Senales[1] = 1
                            if Arr_Control_Senales[2] == 2:
                                Arr_Control_Senales[2] = 3
                        if Int_Contador_Intervalo  >= Int_Valor_Intervalo:
                            int_Tipo_Programa = 2
                            if Arr_Control_Senales[1] == 2:
                                Arr_Control_Senales[1] = 3
                            if Arr_Control_Senales[2] == 0:
                                Arr_Control_Senales[2] = 1
                            if Int_Contador_Intervalo2  >= Int_Valor_Distancia:
                                
                                if C_Intervalo == 0:
                                    Contador_Valor_Intervalo+=1    
                                    if Contador_Valor_Intervalo >= Pref_Intervalo.size:
                                        Contador_Valor_Intervalo = 0
                                        Pref_Intervalo = np.random.permutation(Pref_Intervalo)
                                    Int_Valor_Intervalo = Pref_Intervalo[Contador_Valor_Intervalo]    
                                else:        
                                    Int_Valor_Intervalo = random.choice(Pref_Intervalo)
                                Int_Contador_Intervalo = 0
                                
                                if C_Distancia == 0:
                                    Contador_Valor_Distancia+=1    
                                    if Contador_Valor_Distancia >= Pref_Distancia.size:
                                        Contador_Valor_Distancia = 0
                                        Pref_Distancia = np.random.permutation(Pref_Distancia)
                                    Int_Valor_Distancia = Pref_Distancia[Contador_Valor_Distancia]    
                                else:        
                                    Int_Valor_Distancia = random.choice(Pref_Distancia)
                                Int_Contador_Intervalo2 = 0
                                
                                Arr_Control_Consecuencia[0] = 1
                            
                    #---Distancia-Intervalo----        
                    elif PRef_Tipo_Programa == 4:
                        if Int_Contador_Distancia  < Int_Valor_Distancia:
                            Int_Contador_Distancia2 = 0
                            int_Tipo_Programa = 2
                            if Arr_Control_Senales[1] == 0:
                                Arr_Control_Senales[1] = 1
                            if Arr_Control_Senales[2] == 2:
                                Arr_Control_Senales[2] = 3
                        if Int_Contador_Distancia  >= Int_Valor_Distancia:
                            int_Tipo_Programa = 1
                            if Arr_Control_Senales[1] == 2:
                                Arr_Control_Senales[1] = 3
                            if Arr_Control_Senales[2] == 0:
                                Arr_Control_Senales[2] = 1
                            if Int_Contador_Distancia2  >= Int_Valor_Intervalo:
                                
                                if C_Intervalo == 0:
                                    Contador_Valor_Intervalo+=1    
                                    if Contador_Valor_Intervalo >= Pref_Intervalo.size:
                                        Contador_Valor_Intervalo = 0
                                        Pref_Intervalo = np.random.permutation(Pref_Intervalo)
                                    Int_Valor_Intervalo = Pref_Intervalo[Contador_Valor_Intervalo]    
                                else:        
                                    Int_Valor_Intervalo = random.choice(Pref_Intervalo)
                                Int_Contador_Distancia2 = 0
                                
                                if C_Distancia == 0:
                                    Contador_Valor_Distancia+=1    
                                    if Contador_Valor_Distancia >= Pref_Distancia.size:
                                        Contador_Valor_Distancia = 0
                                        Pref_Distancia = np.random.permutation(Pref_Distancia)
                                    Int_Valor_Distancia = Pref_Distancia[Contador_Valor_Distancia]    
                                else:        
                                    Int_Valor_Distancia = random.choice(Pref_Distancia)
                                Int_Contador_Distancia = 0
                                
                                Arr_Control_Consecuencia[0] = 1
                                
                    #---Permanecia Cuadrante----        
                    elif PRef_Tipo_Programa == 5:
                        try:
                            if (int(Centroide[MinSize][1]) >= int(round(Pref_Cuadrante[0]*Img_WebCam.shape[1]))) &\
                               (int(Centroide[MinSize][1]) <= int(round(Pref_Cuadrante[2]*Img_WebCam.shape[1]))) &\
                               (int(Centroide[MinSize][0]) >= int(round(Pref_Cuadrante[1]*Img_WebCam.shape[0]))) &\
                               (int(Centroide[MinSize][0]) <= int(round(Pref_Cuadrante[3]*Img_WebCam.shape[0]))):
                                Int_Contador_Cuadrante+=Arr_TiempoReal[2]
                                int_Tipo_Programa = 3
                                if Arr_Control_Senales[3] == 0:
                                    Arr_Control_Senales[3] = 1
                                if Int_Contador_Cuadrante  >= Int_Valor_Cuadrante:
                                    Int_Valor_Cuadrante = random.choice(Pref_Cuadrante_Intervalo)
                                    Int_Contador_Cuadrante = 0
                                    Arr_Control_Consecuencia[0] = 1
                                    if Arr_Control_Senales[3] == 2:
                                        Arr_Control_Senales[3] = 3
                            else:
                                int_Tipo_Programa = 5
                                if (C_Cuadrante == 1) | (C_Cuadrante == 2):
                                    Int_Contador_Cuadrante = 0
                                if Arr_Control_Senales[3] == 2:
                                    Arr_Control_Senales[3] = 3
                        except:
                            Int_Contador_Cuadrante = Int_Contador_Cuadrante
                            
                            
                    Img_WebCam = cv2.resize(Img_WebCam,(400, round((400/Img_WebCam.shape[1])*Img_WebCam.shape[1])))
                    
                    if C_Final_Sesion == 1:
                        cv2.putText(Img_WebCam,'C: ',(5,15),Font_CV, .5,(255,255,255),1)
                        cv2.putText(Img_WebCam,str(Int_Contador_Consecuencia),(20,15),Font_CV, .5,(255,255,255),1)
                    else:
                        cv2.putText(Img_WebCam,'T: ',(5,15),Font_CV, .5,(255,255,255),1)
                        cv2.putText(Img_WebCam,str(round((Arr_TiempoReal[3]) ,2)),(20,15),Font_CV, .5,(255,255,255),1)
                    if PRef_Tipo_Programa == 1:
                        cv2.putText(Img_WebCam,'V: ',(5,35),Font_CV, .5,(255,255,255),1)
                        cv2.putText(Img_WebCam,str(round(Int_Contador_Velocidad ,2)),(20,35),Font_CV, .5,(255,255,255),1)
                    elif PRef_Tipo_Programa == 3:
                        cv2.putText(Img_WebCam,'I1: ',(5,35),Font_CV, .5,(255,255,255),1)
                        cv2.putText(Img_WebCam,str(round(Int_Contador_Intervalo ,2)),(30,35),Font_CV, .5,(255,255,255),1)
                        cv2.putText(Img_WebCam,'I2: ',(5,55),Font_CV, .5,(255,255,255),1)
                        cv2.putText(Img_WebCam,str(round(Int_Contador_Intervalo2 ,2)),(30,55),Font_CV, .5,(255,255,255),1)
                    elif PRef_Tipo_Programa == 4:
                        cv2.putText(Img_WebCam,'D1: ',(5,35),Font_CV, .5,(255,255,255),1)
                        cv2.putText(Img_WebCam,str(round(Int_Contador_Distancia ,2)),(30,35),Font_CV, .5,(255,255,255),1)
                        cv2.putText(Img_WebCam,'D2: ',(5,55),Font_CV, .5,(255,255,255),1)
                        cv2.putText(Img_WebCam,str(round(Int_Contador_Distancia2 ,2)),(30,55),Font_CV, .5,(255,255,255),1)
                    else:
                        cv2.putText(Img_WebCam,'I: ',(5,35),Font_CV, .5,(255,255,255),1)
                        cv2.putText(Img_WebCam,str(round(Int_Contador_Intervalo ,2)),(20,35),Font_CV, .5,(255,255,255),1)
                        cv2.putText(Img_WebCam,'D: ',(5,55),Font_CV, .5,(255,255,255),1)
                        cv2.putText(Img_WebCam,str(round(Int_Contador_Distancia ,2)),(20,55),Font_CV, .5,(255,255,255),1)
                    cv2.putText(Img_WebCam,'C: ',(5,75),Font_CV, .5,(255,255,255),1)
                    cv2.putText(Img_WebCam,str(round(Int_Contador_Cuadrante ,2)),(20,75),Font_CV, .5,(255,255,255),1)
                    cv2.imshow('Tracking',Img_WebCam)
                    cv2.moveWindow('Tracking', 120,250);
                                       
                    #Arduino   
                    #---SeñalIntervalo---
                    if Pref_Senalar_Intervalo == 1:
                        if PRef_Tipo_Programa == 1:
                            if Arr_Control_Senales[0] == 1:
                                Arduino.write(b'd')
                                Arr_Control_Senales[0] = 2
                            if Arr_Control_Senales[0] == 0:
                                if x_control == 1:
                                    Arduino.write(b'c')
                                    x_control = 0
                                int_Tipo_Programa = 1
                        if (PRef_Tipo_Programa == 3):    
                            if (Arr_Control_Senales[1] == 1) & (Arr_Control_Senales[0] == 0):
                                Arduino.write(b'c')
                                int_Tipo_Programa = 1
                                Arr_Control_Senales[1] = 2
                            if Arr_Control_Senales[1] == 3:
                                Arduino.write(b'd')
                                Arr_Control_Senales[1] = 0
                        if (PRef_Tipo_Programa == 4):    
                            if (Arr_Control_Senales[1] == 1) & (Arr_Control_Senales[0] == 0):
                                Arduino.write(b'c')
                                int_Tipo_Programa = 1
                                Arr_Control_Senales[1] = 2
                            if Arr_Control_Senales[1] == 3:
                                Arduino.write(b'd')
                                Arr_Control_Senales[1] = 0
                    #---SeñalDistancia---
                    if Pref_Senalar_Distancia == 1:
                        if PRef_Tipo_Programa == 2:
                            if Arr_Control_Senales[0] == 1:
                                Arduino.write(b'f')
                                Arr_Control_Senales[0] = 2
                            if Arr_Control_Senales[0] == 0:
                                if x_control == 1:
                                    Arduino.write(b'e')
                                    x_control = 0
                                int_Tipo_Programa = 2
                        if (PRef_Tipo_Programa == 3):    
                            if (Arr_Control_Senales[2] == 1) & (Arr_Control_Senales[0] == 0):
                                Arduino.write(b'e')
                                int_Tipo_Programa = 2
                                Arr_Control_Senales[2] = 2
                            if Arr_Control_Senales[2] == 3:
                                Arduino.write(b'f')
                                Arr_Control_Senales[2] = 0
                        if (PRef_Tipo_Programa == 4):    
                            if (Arr_Control_Senales[2] == 1) & (Arr_Control_Senales[0] == 0):
                                Arduino.write(b'e')
                                int_Tipo_Programa = 2
                                Arr_Control_Senales[2] = 2
                            if Arr_Control_Senales[2] == 3:
                                Arduino.write(b'f')
                                Arr_Control_Senales[2] = 0
                    #---SeñalIntervalo---
                    if Pref_Senalar_Cuadrante == 1:
                        if PRef_Tipo_Programa == 5:
                            if (Arr_Control_Senales[3] == 1) & (Arr_Control_Senales[0] == 0):
                                Arduino.write(b'c')
                                int_Tipo_Programa = 3
                                Arr_Control_Senales[3] = 2
                            if Arr_Control_Senales[3] == 3:
                                Arduino.write(b'd')
                                Arr_Control_Senales[3] = 0
                    #---Consecuencia---
                    if Arr_Control_Consecuencia[0] == 1:
                        if Arr_Contador_Consecuencia[0] == 0:
                            Arr_Contador_Consecuencia[0]+=Arr_TiempoReal[2]
                            Arduino.write(b'a')
                            int_Tipo_Programa = 0
                            Arr_Control_Senales[0] = 1
                            Int_Datos_Consecuencia = 1
                            x_control = 1
                        elif Arr_Contador_Consecuencia[0] >= Pref_Tiempo_Consecuencia[0]:
                            Arr_Contador_Consecuencia[0] = 0
                            Arr_Control_Consecuencia[0] = 0
                            Arr_Control_Senales[0] = 0
                            Int_Datos_Consecuencia = 0
                            if C_Final_Sesion == 1:
                                Int_Contador_Consecuencia += 1;
                            Arduino.write(b'b')
                        else:
                            Arr_Contador_Consecuencia[0]+=Arr_TiempoReal[2]
                            Arr_Control_Senales[0] = 2  
                            Int_Contador_Intervalo = 0 
                            Int_Contador_Distancia = 0
                            Int_Contador_Cuadrante = 0
                    
                    
                    Mat_Datos[Int_Contador][0] = Arr_TiempoReal[3]
                    try:
                        Mat_Datos[Int_Contador][1] = int(Centroide[MinSize][1])
                        Mat_Datos[Int_Contador][2] = int(Centroide[MinSize][0])
                    except:
                        Mat_Datos[Int_Contador][1] = Mat_Datos[Int_Contador-1][1]
                        Mat_Datos[Int_Contador][2] = Mat_Datos[Int_Contador-1][2]
                    Mat_Datos[Int_Contador][4] = Int_Datos_Consecuencia
                    if Int_Contador == 1:
                        Mat_Datos[Int_Contador][3] = 0
                    else:    
                        Mat_Datos[Int_Contador][3] = (Fun_Distancia(Mat_Datos[Int_Contador-1][1],Mat_Datos[Int_Contador][1],Mat_Datos[Int_Contador-1][2],Mat_Datos[Int_Contador][2],Dev_Espacio_Tamano/int(Arr_Parametros_track[15])))
                    Mat_Datos[Int_Contador][5] = int_Tipo_Programa
                    
                    Int_Contador += 1
                    
                    #Relog
                    Arr_TiempoReal[1]=time.time()
                    Arr_TiempoReal[2]=Arr_TiempoReal[1]-Arr_TiempoReal[0] 
                    Arr_TiempoReal[3]+= Arr_TiempoReal[2]
                    Int_Contador_Intervalo+=Arr_TiempoReal[2]
                    Int_Contador_Intervalo2+=Arr_TiempoReal[2]
                    
                    #Distancia
                    Int_Contador_Distancia += Mat_Datos[Int_Contador-1][3]
                    Int_Contador_Distancia2 += Mat_Datos[Int_Contador-1][3]
                    Mat_Datos[Int_Contador-1][6] = (Mat_Datos[Int_Contador-1][3]/100) / Arr_TiempoReal[2]
                    Int_Contador_Velocidad = (Mat_Datos[Int_Contador-1][3]) / (Arr_TiempoReal[2]* 30)
                    Arr_TiempoReal[0]=time.time()
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
          
                Dev_WebCam_Read.release()
                cv2.destroyAllWindows()
                Mat_Datos = np.delete(Mat_Datos,np.where(Mat_Datos[:,0] == -1), axis=0)
                Mat_Datos[0,3] = 0
                Mat_Datos[0,6] = 0
                
                Arduino.write(b'b')
                Arduino.write(b'd')
                Arduino.write(b'f')
                Arduino.write(b'h')
                Arduino.write(b'j')
                Arduino.close()
                    
                                
                
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
                
                #Datos                
                Nombre_Grafico =  filedialog.asksaveasfilename(initialdir = Dir_Datos,
                                                                            title = "Save Data",
                                                                            filetypes = (("all files","*.*"), ("txt files","*.txt"))) 
 
                i = 1
                Archivo_Mat_Datos = open(Nombre_Grafico + '.txt','w')
                Archivo_Mat_Datos.write('Subject: ' + Str_Sujeto + '\n' +
                                        'Session: ' + Str_Sesion + '\n' +
                                        'Group: ' + Str_Grupo + '\n' +
                                        'Time: '+ str(max(Mat_Datos[:,0])) + '\n' +
                                        '# Consecuences: ' + str(np.size(np.where(Mat_Datos[:,4] == 1))) + '\n' +
                                        'Distance: ' + str(round(sum(Mat_Datos[:,3]),3)) + 'cm' + '\n' +
                                        'Velocity: ' + str(round(sum(Mat_Datos[:,3])/max(Mat_Datos[:,0]),3)) + 'cm/seg' + '\n' +
                                        'Mean Aceleration: ' + str(round(statistics.mean(Mat_Datos[:,5]),3)) + 'm/seg' + '\n' +
                                        '\n' + 'Frame;Time;X;Y;Aceleration;Distance;Consecuences;Signal' + '\n')
                for i in range(0,len(Mat_Datos)): 
                    Archivo_Mat_Datos.write(str(i) + ',' + str(round(Mat_Datos[i][0],3)) +
                                                     ',' + str(round(Mat_Datos[i][1] * (Dev_Espacio_Tamano/int(Arr_Parametros_track[15])),3)) +
                                                     ',' + str(round(Mat_Datos[i][2] * (Dev_Espacio_Tamano/int(Arr_Parametros_track[16])),3)) +
                                                     ',' + str(round(Mat_Datos[i][3],3)) +
                                                     ',' + str(Mat_Datos[i][4]) + ';' + str(Mat_Datos[i][5]) +
                                                     ',' + str(round(Mat_Datos[i][6],3)) + '\n')
        
                Archivo_Mat_Datos.close() 
                messagebox.showinfo("Finalized", "End Sesion")
#                Main_Ses.destroy()
              
            #Cerrar
            Lbl_Save_Text = tkinter.Label(Main_Ses, bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), text = 'Save video')
            Lbl_Save_Text.config(font = (Font_1,14))
            Lbl_Save_Text.place(x=aux_width_monitor*6.1, y = aux_height_monitor*10.2)
            
            Var_Radiobutton = tkinter.IntVar(Main_Ses)
            radiobutton1 = tkinter.Radiobutton(Main_Ses, text='', bg = Fun_Rgb(C_Pal5), fg = Fun_Rgb(C_Pal2), 
                                               activebackground=Fun_Rgb(C_Pal4),
                                               highlightbackground=Fun_Rgb(C_Pal5), variable=Var_Radiobutton, value=1)
            radiobutton1.config(font = (Font_1,24))
            radiobutton1.place(x=aux_width_monitor*7.2, y = aux_height_monitor*10.05)
            Var_Radiobutton.get()
            #Bnt Next
            Bnt_Next = tkinter.Button(Main_Ses, bd=0, fg = Fun_Rgb(C_Pal5),
                                      bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                      highlightbackground=Fun_Rgb(C_Pal5),
                                      text = '  Run  ', command = Fun_Run)
            Bnt_Next.config(font = (Font_1,25))
            Bnt_Next.place(x=aux_width_monitor*6.1, y = aux_height_monitor*11)
            
            Main.mainloop()
            
        
        
            
        Bnt_Next = tkinter.Button(Main, bd=0, fg = Fun_Rgb(C_Pal5),
                                  bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                  highlightbackground=Fun_Rgb(C_Pal5),
                                  text = '   Next   ', command = Fun_Bnt_Next)
        Bnt_Next.config(font = (Font_1,25))
        Bnt_Next.place(x=aux_width_monitor*12.5, y = aux_height_monitor *11)
        
        
        Main.mainloop()
    #%%Ventana Menu Principal
    
    #Tkinter
    ventanaMenuPrincipal = tkinter.Tk()
    ventanaMenuPrincipal.geometry(str(width_monitor)+'x'+str(height_monitor-70)+'+0+0') 
    ventanaMenuPrincipal.title('Menu')
    ventanaMenuPrincipal.config(background = Fun_Rgb(C_Pal5))
    
    #Canvas
    ventanaMenuPrincipal_Can = Canvas(ventanaMenuPrincipal, width=width_monitor, 
                                      height=height_monitor-80, bg=Fun_Rgb(C_Pal5))
    ventanaMenuPrincipal_Can.create_rectangle(10, 10, width_monitor-10, height_monitor-90, 
                                              outline=Fun_Rgb(C_Pal3), width=4)
    ventanaMenuPrincipal_Can.place(x=0,y=0)  
    
    
#    #Img1
    Img_ventanaMenuPrincipal_1 = Fun_Size(Dir_Images + '/' +'interfaz-01.png',.2)
    Lbl_ventanaMenuPrincipal_1 = tkinter.Label(ventanaMenuPrincipal, bg = Fun_Rgb(C_Pal5), image = Img_ventanaMenuPrincipal_1 )
    Lbl_ventanaMenuPrincipal_1.place(x=aux_width_monitor*13.5,y=aux_height_monitor*11) 
            
    #Bnt Cortar Video
    
    Lbl_SesionT_Text_1 = tkinter.Label(ventanaMenuPrincipal, bg = Fun_Rgb(C_Pal5),
                                       fg = Fun_Rgb(C_Pal2), text = '  3D Tracking  ')
    Lbl_SesionT_Text_1.config(font = (Font_1,35))
    Lbl_SesionT_Text_1.place(x=aux_width_monitor*2,y=aux_height_monitor)
    
    Img_ventanaMenuPrincipal_Bnt_CortarVideo = Fun_Size(Dir_Images + '/' +'Menu_4.png',aux_size-.45)
    Bnt_ventanaMenuPrincipal_Bnt_CortarVideo = tkinter.Button(ventanaMenuPrincipal,image = Img_ventanaMenuPrincipal_Bnt_CortarVideo,  bd=0,
                                                  bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2),
                                                  text = '0', highlightbackground = Fun_Rgb(C_Pal5),
                                                  command = Fun_Cortar_Video)
    Bnt_ventanaMenuPrincipal_Bnt_CortarVideo.place(x=aux_width_monitor*1.2,y=aux_height_monitor*2)  
    
    #Bnt Cortar Video
    
    Lbl_SesionT_Text_1 = tkinter.Label(ventanaMenuPrincipal, bg = Fun_Rgb(C_Pal5),
                                       fg = Fun_Rgb(C_Pal2), text = '     Projects    ')
    Lbl_SesionT_Text_1.config(font = (Font_1,35))
    Lbl_SesionT_Text_1.place(x=aux_width_monitor*9.5,y=aux_height_monitor)
    
    Img_ventanaMenuPrincipal_Bnt_Imagen = Fun_Size(Dir_Images + '/' +'Menu_1.png',aux_size-.45)
    Bnt_ventanaMenuPrincipal_Bnt_Imagen = tkinter.Button(ventanaMenuPrincipal,image = Img_ventanaMenuPrincipal_Bnt_Imagen,  bd=0,
                                                  bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2),
                                                  text = '0', highlightbackground = Fun_Rgb(C_Pal5),
                                                  command = Fun_Track_Vivo_Y_Videos)
    Bnt_ventanaMenuPrincipal_Bnt_Imagen.place(x=aux_width_monitor*8.5,y=aux_height_monitor*2)
    
    #Bnt Track con consecuencias
    
    
    Lbl_SesionT_Text_1 = tkinter.Label(ventanaMenuPrincipal, bg = Fun_Rgb(C_Pal5),
                                       fg = Fun_Rgb(C_Pal2), text = 'Schedules 1.0')
    Lbl_SesionT_Text_1.config(font = (Font_1,35))
    Lbl_SesionT_Text_1.place(x=aux_width_monitor*2,y=aux_height_monitor*7)
    
    Img_ventanaMenuPrincipal_Bnt_Consecuencias = Fun_Size(Dir_Images + '/' +'Menu_2.png',aux_size-.45)
    Bnt_ventanaMenuPrincipal_Bnt_Consecuencias = tkinter.Button(ventanaMenuPrincipal,image = Img_ventanaMenuPrincipal_Bnt_Consecuencias,  bd=0,
                                                  bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2),
                                                  text = '0', highlightbackground = Fun_Rgb(C_Pal5),
                                                  command = Fun_Programas_Ref)
    Bnt_ventanaMenuPrincipal_Bnt_Consecuencias.place(x=aux_width_monitor*1.2,y=aux_height_monitor*8)
    
    Lbl_SesionT_Text_1 = tkinter.Label(ventanaMenuPrincipal, bg = Fun_Rgb(C_Pal5),
                                       fg = Fun_Rgb(C_Pal2), text = 'Schedules 2.0 ')
    Lbl_SesionT_Text_1.config(font = (Font_1,35))
    Lbl_SesionT_Text_1.place(x=aux_width_monitor*9.5,y=aux_height_monitor*7)
    
    Img_ventanaMenuPrincipal_Bnt_Consecuencias2 = Fun_Size(Dir_Images + '/' +'Menu_3.png',aux_size-.45)
    Bnt_ventanaMenuPrincipal_Bnt_Consecuencias2 = tkinter.Button(ventanaMenuPrincipal,image = Img_ventanaMenuPrincipal_Bnt_Consecuencias2,  bd=0,
                                                  bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2),
                                                  text = '0', highlightbackground = Fun_Rgb(C_Pal5),
                                                  command = Fun_Programas_Ref2)
    Bnt_ventanaMenuPrincipal_Bnt_Consecuencias2.place(x=aux_width_monitor*8.7,y=aux_height_monitor*8)
            
    ventanaMenuPrincipal.mainloop()
    

#%%Bnt Ventana Inicio
    
Img_ventanaInicio_Bnt_Inicio = Fun_Size(Dir_Images + '/' +'interfaz-07.png',aux_size)
Bnt_ventanaInicio_Bnt_Inicio = tkinter.Button(ventanaInicio,image = Img_ventanaInicio_Bnt_Inicio,  bd=0,
                                              bg = Fun_Rgb(C_Pal5), activebackground=Fun_Rgb(C_Pal2),
                                              highlightbackground = Fun_Rgb(C_Pal5),
                                              text = '0', command = Fun_AbrirVentanaMenuPrincipal1)
Bnt_ventanaInicio_Bnt_Inicio.place(x=aux_width_monitor*7.5, y=aux_height_monitor*7.5)    
    
ventanaInicio.mainloop()
