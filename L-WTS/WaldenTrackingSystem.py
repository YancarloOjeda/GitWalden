# -*- coding: utf-8 -*-
"""
Walden Modular Equipment 2019
"""

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
from PIL import Image, ImageTk

global Font_CV, Key
Font_CV = cv2.FONT_HERSHEY_SIMPLEX
Key = 0

Dir_Videos = 'C:/WALDEN/Videos/'
Dir_Proyecto = 'C:/WALDEN/Projects/' 
Dir_Data = 'C:/WALDEN/Data/'
Dir_Archivo_PRef = 'C:/WALDEN/Schedules'
Dir_Archivo_Parametros = 'C:/WALDEN/Config/'
Dir_Archivo_Datos = 'C:/WALDEN/Data/'
Dir_Images = 'C:/WALDEN/Images/'


#Dir_Videos = 'C:/Users/Laurent/Documents/WALDEN/Videos/'
#Dir_Proyecto = 'C:/Users/Laurent/Documents/WALDEN/Projects/' 
#Dir_Data = 'C:/Users/Laurent/Documents/WALDEN/Data/'
#Dir_Archivo_PRef = 'C:/Users/Laurent/Documents/WALDEN/Schedules/'
#Dir_Archivo_Parametros = 'C:/Users/Laurent/Documents/WALDEN/Config/'
#Dir_Archivo_Datos = 'C:/Users/Laurent/Documents/WALDEN/Data/'
#Dir_Images = 'C:/Users/Laurent/Documents/WALDEN/Images'



def Fun_AbrirVentanaMenuPrincipal1():
    global Key
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
         Key = 1      
    else:
        messagebox.showinfo("Error Key", "Connect USB Key")


def T_Image():
    myImage = Image.open((os.getcwd() + '\\Interface.png').replace('\\', '/'))
    myImage.show();

def Get_Time():
    return time.time()

def Timer(Time,TempTime,Seconds):
    if Time == 0:
        time.sleep(Seconds)
        Time = Seconds
    else:
        time.sleep(Seconds)
        Time = Time + (time.time() - TempTime)
    Time = round(Time,4)
    return Time  

def Event_Timer(Time,TempTime):
    if Time == 0:
        Time = 0.0001
    else:
        Time = Time + (time.time() - TempTime)
    Time = round(Time,4)
    return Time     

def Pause_Time(Seconds):
    time.sleep(Seconds)
        
    
#Parametros
def Open_Image(): 
    TK = tkinter.Tk()
    file = filedialog.askopenfilename(initialdir = Dir_Proyecto,
                                     title = "Image_Configuration",
                                     filetypes = (("txt","*.txt"),("all files","*.*")))
    global Image_Parameters
    TempFile =open(file,'r')  
    Image_Parameters = TempFile.read().split('\n')    
    TempFile.close()
    #Image
    Image = (float(Image_Parameters[2]),
             float(Image_Parameters[3]),
             float(Image_Parameters[4]),
             float(Image_Parameters[5]),
             int(Image_Parameters[6]),
             int(Image_Parameters[15]),
             int(Image_Parameters[16]))
    #RGB
    if int(Image_Parameters[17]) <= 1:
        RGB = (int(Image_Parameters[8]),
               int(Image_Parameters[9]),
               int(Image_Parameters[10]),
               int(Image_Parameters[11]),
               float(Image_Parameters[12]), )  
    
    TK.destroy()
    TK.mainloop() 
    return RGB, Image

#Parametros
def Open_Image_0(P): 
    file = Dir_Proyecto + P + '/Config_' + P + '.txt'
    global Image_Parameters
    TempFile =open(file,'r')  
    Image_Parameters = TempFile.read().split('\n')    
    TempFile.close()
    #Image
    Image = (int(Image_Parameters[0]),
             float(Image_Parameters[2]),
             float(Image_Parameters[3]),
             float(Image_Parameters[4]),
             float(Image_Parameters[5]),
             int(Image_Parameters[6]),
             int(Image_Parameters[15]),
             int(Image_Parameters[16]),
             int(Image_Parameters[7]))
    #RGB
    if int(Image_Parameters[17]) <= 1:
        RGB = (int(Image_Parameters[8]),
               int(Image_Parameters[9]),
               int(Image_Parameters[10]),
               int(Image_Parameters[11]),
               float(Image_Parameters[12]),
               float(Image_Parameters[13]), 
               float(Image_Parameters[14]))  
    
    return RGB, Image

#WebCam
def Star_WebCam(Parameters):
    WebCam = cv2.VideoCapture(int(Parameters[1][0]))
    WebCam.set(3,Parameters[1][6])
    WebCam.set(3,Parameters[1][7])
    return WebCam
    
def Get_WebCam(WebCam):
    ret, Image = WebCam.read()  
    return Image
    
def Show_WebCam(Image):
    cv2.imshow('WebCam',Image)
    
def Flush_WebCam():
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('')
        
def Stop_WebCam(WebCam):
    WebCam.release()     
    
#Tracking
def Tracking(Image, Parameters):
    
    num_rows, num_cols = Image.shape[:2]
    Mat_Img_Rotada = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), Parameters[1][5], 1)
    Image  = cv2.warpAffine(Image, Mat_Img_Rotada, (num_cols, num_rows))
    Image = Image[round(Image.shape[0]*Parameters[1][3]):round(Image.shape[0]*Parameters[1][4]),
                    round(Image.shape[1]*Parameters[1][1]):round(Image.shape[1]*Parameters[1][2])]

    Mat_WebCam_RGB = np.zeros((Image.shape))
    Mat_WebCam_RGB[(np.where((Image[:,:,2]>=(Parameters[0][0]-Parameters[0][3])) & (Image[:,:,2]<=(Parameters[0][0]+Parameters[0][3])))[0]),
                   (np.where((Image[:,:,2]>=(Parameters[0][0]-Parameters[0][3])) & (Image[:,:,2]<=(Parameters[0][0]+Parameters[0][3])))[1]),0] = 1
    Mat_WebCam_RGB[(np.where((Image[:,:,1]>=(Parameters[0][1]-Parameters[0][3])) & (Image[:,:,1]<=(Parameters[0][1]+Parameters[0][3])))[0]),
                   (np.where((Image[:,:,1]>=(Parameters[0][1]-Parameters[0][3])) & (Image[:,:,1]<=(Parameters[0][1]+Parameters[0][3])))[1]),1] = 1
    Mat_WebCam_RGB[(np.where((Image[:,:,0]>=(Parameters[0][2]-Parameters[0][3])) & (Image[:,:,0]<=(Parameters[0][2]+Parameters[0][3])))[0]),
                   (np.where((Image[:,:,0]>=(Parameters[0][2]-Parameters[0][3])) & (Image[:,:,0]<=(Parameters[0][2]+Parameters[0][3])))[1]),2] = 1          
    Image = Mat_WebCam_RGB  
           
    if int(Parameters[0][5])==1:
        Image = ndimage.gaussian_filter(Image, sigma=3)
    elif int(Parameters[0][5])==2:
        Image = ndimage.gaussian_filter(Image, sigma=5)
    elif int(Parameters[0][5])==3:
        Image =ndimage.uniform_filter(Image, size=2)
    elif int(Parameters[0][5])==4:
        Image =ndimage.uniform_filter(Image, size=11)
    elif int(Parameters[0][5])==5:
        Image = Image
 
    np.place(Image[:,:,:], Image[:,:,:]>=float(Parameters[0][4]) , 1)
    np.place(Image[:,:,:], Image[:,:,:]<float(Parameters[0][4]), 0)
    
    try:
        Mat_Centroide = ndimage.label(Image)[0]
        Centroide = scipy.ndimage.measurements.center_of_mass(Image, Mat_Centroide, [1,2,3])
        Mat_Size = ndimage.label(Image)[0]
        Size = np.sqrt(scipy.ndimage.measurements.sum(Image, Mat_Size, [1,2,3]))
        MinSize = int(np.where(Size == np.min(Size[(Size >= int(Parameters[0][6]))]))[0]) #Check
        cv2.circle(Image,(int(Centroide[MinSize][1]),int(Centroide[MinSize][0])),2,(0,0,255),5)
        X = round(int(Centroide[MinSize][1]) * (Parameters[1][8] / int(Parameters[1][6])),3)
        Y = round(Parameters[1][8] - (int(Centroide[MinSize][0]) * (Parameters[1][8] / int(Parameters[1][7]))),3)
        #print(X,Y)
    except:
        Image = Image
        X = 0
        Y = 0
       
    return Image, X, Y

def Show_WebCam_Tracking(Image, Time, X, Y, Var):
    cv2.putText(Image,('1: ' + str(Time)),(5,15),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('2: ' + str(X)),(5,35),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('3: ' + str(Y)),(5,55),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('4: ' + str(Var)),(5,75),Font_CV, .5,(255,255,255),1)
    cv2.imshow('Tracking1',Image)
    
def Show_WebCam_Tracking_Zone(Image, Time, X, Y, Var, Zone):
    cv2.putText(Image,('1: ' + str(Time)),(5,15),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('2: ' + str(X)),(5,35),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('3: ' + str(Y)),(5,55),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('4: ' + str(Var)),(5,75),Font_CV, .5,(255,255,255),1)
    NZone = [int(i) for i in Zone]
    cv2.rectangle(Image,(NZone[0],NZone[1]),(NZone[2],NZone[3]),(0,255,0),3)
    cv2.imshow('Tracking1',Image)
    
def Show_WebCam_Tracking_Zone_C(Image, Time, X, Y, Var, Zone,Color):
    cv2.putText(Image,('1: ' + str(Time)),(5,15),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('2: ' + str(X)),(5,35),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('3: ' + str(Y)),(5,55),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('4: ' + str(Var)),(5,75),Font_CV, .5,(255,255,255),1)
    NZone = [int(i) for i in Zone]
    cv2.rectangle(Image,(NZone[0],NZone[1]),(NZone[2],NZone[3]),Color,3)
    cv2.imshow('Tracking1',Image)
    
def Show_WebCam_Tracking2(Image, Time, X, Y, Var):
    cv2.putText(Image,('1: ' + str(Time)),(5,15),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('2: ' + str(X)),(5,35),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('3: ' + str(Y)),(5,55),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('4: ' + str(Var)),(5,75),Font_CV, .5,(255,255,255),1)
    cv2.imshow('Tracking2',Image)    
    cv2.moveWindow('Tracking2',500,0);
    
def Show_WebCam_Tracking3(Image, Time, X, Y, Var):
    cv2.putText(Image,('1: ' + str(Time)),(5,15),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('2: ' + str(X)),(5,35),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('3: ' + str(Y)),(5,55),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('4: ' + str(Var)),(5,75),Font_CV, .5,(255,255,255),1)
    cv2.imshow('Tracking3',Image) 
    cv2.moveWindow('Tracking2',500,500);

def Show_WebCam_Tracking4(Image, Time, X, Y, Var):
    cv2.putText(Image,('1: ' + str(Time)),(5,15),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('2: ' + str(X)),(5,35),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('3: ' + str(Y)),(5,55),Font_CV, .5,(255,255,255),1)
    cv2.putText(Image,('4: ' + str(Var)),(5,75),Font_CV, .5,(255,255,255),1)
    cv2.imshow('Tracking4',Image)  
    cv2.moveWindow('Tracking2',0,500);   
    
#Variables
def Distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

#Distance
def Create_Zone (Parameters,x1,y1,x2,y2):
    xx1 = Parameters[1][8] * x1
    xx2 = Parameters[1][8] * x2
    yy1 = ((Parameters[1][7]/Parameters[1][6])*Parameters[1][8]) * y1
    yy2 = ((Parameters[1][7]/Parameters[1][6])*Parameters[1][8]) * y2
    x1 = Parameters[1][6] * x1
    x2 = Parameters[1][6] * x2
    y1 = Parameters[1][7] * y1
    y2 = Parameters[1][7] * y2
    return [int(x1),int(y1),int(x2),int(y2),int(xx1),int(yy1),int(xx2),int(yy2)]

def InZone(Zone,X,Y):
    NZone = [int(i) for i in Zone]
    if ((X >= NZone[4]) & (X <= NZone[6])) & ((Y >= NZone[5]) & (Y <= NZone[7])):
        R = 1
    else:
        R = 0
    return R
        

#Data
def MOTUS(Data,Frame,Time,X,Y,Distance,Events,show):
    Data = (Data + '[' + str(Frame) + ',' + str(Time) +
            ',' + str(X) + ',' + str(Y) + 
            ',' + str(round(Distance,3)) + ',' + str(Events) + ']')
    if show == 1:
        print(str(Frame) + ' , ' + str(Time) +
            ' , ' + str(X) + ' , ' + str(Y) + 
            ' , ' + str(round(Distance,3)) + ' , ' + str(Events))
    return Data

def Data_Transform(Data):
    TempData = ''
    for i in range(0,len(Data)): 
        if Data[i] == '[':
            TempData = TempData
        elif Data[i] == ']':
            TempData += '\n'
        else:
            TempData += Data[i]
            
        
        

def MOTUS_Export(Data):
    
    TK = tkinter.Tk()
    File =  filedialog.asksaveasfilename(initialdir = Dir_Data,
                                         title = "Save Data",
                                         filetypes = (("all files","*.*"), ("txt files","*.txt"))) 
    File_Data = open(File + '.txt','w')
    File_Data.write('MOTUS DATA \n---------------- \n')
    File_Data.write('Frame, Time, X, Y, Distance, Events \n')
    for i in range(0,len(Data)): 
        if Data[i] == '[':
            a = 0
        elif Data[i] == ']':
            File_Data.write('\n')
        else:
            File_Data.write(Data[i])
    
    
    File_Data.close() 
    
    TK.destroy()
    TK.mainloop() 
    
#Arduino

def Check_Connected_Arduinos():
    Serial_Port = list(serial.tools.list_ports.comports())
    print('-------Serial Port---------\n')
    for i in range(0,len(Serial_Port)):
            print(Serial_Port[i].description)
    print('\n---------------------------')
    
def Get_WPI(COM): 
    print('\n')
    Serial = serial.Serial(COM)
    for i in range(0,9): 
        print('.',end = " ")
        Pause_Time(.2)
    print('WPI Ready')
    return Serial
    
def Stop_WPI(WPI):
    WPI.close()
    
def WPI_Out(WPI,Out):
    WPI.flush()
    WPI.write(Out.encode())
    
#Shudel

def Event_Time(Timer,Interval,Duration,WPI,Out1,Out2,Data1,Data2):
    Data = 0
    if Timer >= (Interval + Duration):
        WPI_Out(WPI,Out2)
        Timer = 0
        Data = Data2
    elif Timer >= Interval:
        WPI_Out(WPI,Out1)
        Data = Data1
    return Timer,Data

def Event_Time_End(Timer,Interval,Duration,Duration2,WPI,Out1,Out2,Data1,Data2):
    Data = 0
    if Timer >= (Interval + Duration + Duration2):
        Timer = 0
    elif Timer >= (Interval + Duration):
        WPI_Out(WPI,Out2)
        Data = Data2
    elif Timer >= Interval:
        WPI_Out(WPI,Out1)
        Data = Data1    
    return Timer,Data

def Event_Distance_Response(Counter,Distance, Control):
    if Counter >= Distance:
        Counter = 0
        Control = 1
    return Counter, Control

def Event_Time_Start(Counter,Control,Timer,Interval,Duration,Duration2,Reset,WPI,Out1,Out2,Data1,Data2):
    Data = 0
    if Control == 1:
        if Reset == 1:
            Counter = 0
        if Timer >= (Interval + Duration + Duration2):
            Timer = 0
            Control = 0
        elif Timer >= (Interval + Duration):
            WPI_Out(WPI,Out2)
            Data = Data2
        elif Timer >= Interval:
            WPI_Out(WPI,Out1)
            Data = Data1  
    elif Control == 0:
        Timer = 0
    return Counter,Control,Timer,Data

def Event_Chain(Control1,Control2,Timer):
    if (Control1 == 0) & (Timer == 0):
        Control2 = 1
    elif Control1 == 1:
        Control2 = 0
    return Control1,Control2

    
def Space(Parameters,X1,X2,Y1,Y2):
    X = int(Parameters[1][6])
    Y = int(Parameters[1][7])
    R = int(Parameters[1][8])
    
    
    WebCam = wts.Star_WebCam(Parameters)
    Image0 = wts.Get_WebCam(WebCam)
    Stop_WebCam(WebCam)
    
    num_rows, num_cols = Image0.shape[:2]
    Mat_Img_Rotada = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), Parameters[1][5], 1)
    Image0  = cv2.warpAffine(Image0, Mat_Img_Rotada, (num_cols, num_rows))
    Image0 = Image0[round(Image0.shape[0]*Parameters[1][3]):round(Image0.shape[0]*Parameters[1][4]),
                    round(Image0.shape[1]*Parameters[1][1]):round(Image0.shape[1]*Parameters[1][2])]
    
    TK = tkinter.Tk()
    TK.geometry(str(X)+'x'+str(Y)+'+0+0')
    TK.title('Space')
    TK.config(bg = "#%02x%02x%02x" % (255,255,255))
              
    
    TKC = Canvas(width=X, height=Y)
    
    Image0 = cv2.resize(Image0, dsize=(X*2, Y*2), interpolation=cv2.INTER_CUBIC)
    Temp = ImageTk.PhotoImage(image=Image.fromarray(Image0))
    TKC.create_image(0,0, image=Temp)
    TKC.create_rectangle(X1, Y1, X2, Y2, outline="#%02x%02x%02x" % (255,0,0), width=4)
    TKC.place(x=0,y=0)
    
      
              
    TK.mainloop() 
    

Fun_AbrirVentanaMenuPrincipal1()

    
    
        
    
     
       
    
    
    
    
    
    
    
    