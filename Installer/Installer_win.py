#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 19:19:24 2020

@author: yan
"""
import os 
import time

#%%-----------LIBRARIES--------------------------------------------------------
from tkinter import Button, Frame, INSERT, LEFT, RIGHT, Label
from tkinter import  Scrollbar, Text, Tk, TOP, X, Y, filedialog
from PIL import Image, ImageTk
import PIL.Image
from tkinter import *
import cv2
from screeninfo import get_monitors
import tkinter
import os 
import time


#%%-----------COLORS-----------------------------------------------------------
def Fun_Rgb(RGB):
    return "#%02x%02x%02x" % RGB  

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


#%%-----------DIRECTORIES------------------------------------------------------
Dir_Images = ''


#%%-----------GLOBAL VARIABLES------------------------------------------------
global path_file
path_file = ''


#%%-----------HEIGHT AND WEIGHT OF MONITOR------------------------------------
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


#%%-----------FUN SIZE---------------------------------------------------------
def Fun_Size(img, size):
    img = PIL.Image.open(img)
    size_1 = img.size
    width = int(size_1[0]*size)
    height = int(size_1[1]*size)
    img = img.resize((width, height))
    img = ImageTk.PhotoImage(img)
    return img

#%%-----------TOOL TIP---------------------------------------------------------
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

#%%-----------PRINCIPAL WINDOW-------------------------------------------------
root = Tk()
root.title('WTS-2.01 Installer')
root.geometry(str(int(aux_width_monitor*8))+'x'+str(int(aux_height_monitor*8))+'+'+
              str(int(aux_width_monitor*3.5))+'+'+str(int(aux_height_monitor*3.5))) 
root.config(bg = Fun_Rgb(C_Pal3))
root.isStopped = False


#%%-----------FUN SHOW TEXT-------------------------------------------------
def show_text(icon_msg):
    """
    Get a string as parameter and display it in the Text widget 
    """
    text.insert(INSERT, str(icon_msg)+'\n')
    
    
def cmd_Next_4():
    """
    Save the data.txt file in the current directory
    The data.txt will be read for the WTS to get all the directories
    See line 85 to 95 in WTS-2.01.py file
    """
    global path_file
    dataFile = open(path_file + '/data.txt','w')
    dataFile.write(str(path_file))
    dataFile.close()
    dataFile = open(path_file + '/WTS-2.01/WTS-2.01/Config/data.txt','w')
    dataFile.write(str(path_file))
    dataFile.close()
    root.destroy()
    os.system('python '+path_file+'/WTS-2.01/WTS-2.01/Config/WTS-2.01.py')
    
    

def cmd_Next_3():
    """
    Upload Python libraries
    """
    text.delete('1.0', END)
    btnCancel.destroy()
    root.update()
    show_text('\n   Uploading Python libraries')
    
#######------LIBRARIES LIST------############################################
    PList = ['serial',
              'pyfirmata', 
              'opencv-python',
              'python-tk',
              'random',
              'matplotlib',
              'time' ]
#######------FOR WINDOWS------##########################################
    for i in PList:
         installPythonPackage = 'pip install ' + i
         os.system('start cmd /c ' + installPythonPackage)
         root.update()
         text.insert(INSERT, '    '+str(i) +'...ok\n')
    
#######------FOR LINUX------############################################
#    for i in PList:
#        installPythonPackage = 'pip install ' + i
#        os.system(installPythonPackage)
#        time.sleep(1)
#        root.update()
#        text.insert(INSERT, '    '+str(i) +'...ok\n')
        
    show_text('\n  Python libraries have been uploading.')
    
    btnNext = tkinter.Button(root,  bd=0, fg = Fun_Rgb(C_Pal5),
                                  bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                  highlightbackground=Fun_Rgb(C_Pal5),
                                  text = 'Finish', command = cmd_Next_4)
    btnNext.config(font = ("Arial",15))
    btnNext.place(x=aux_width_monitor*7, y=aux_height_monitor*7)   
    root.update()



def cmd_Next_2():
    """
    Show a message to Upload Python libraries
    """
    text.delete('1.0', END)
    root.update()
    
    txtLibraries = "\n  The next Python libraries will be upload: \n" + '   -serial\n' + '   -pyfirmata\n'+'   -opencv-python\n'+ '   -python-tk\n'+'   -random\n'+'   -matplotlib\n'+'   -time\n'
    txtAnun = "\n  Press Next to continue installation"
    
    string = txtLibraries + txtAnun
    
    show_text(string)
    
    btnNext = tkinter.Button(root,  bd=0, fg = Fun_Rgb(C_Pal5),
                                  bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                  highlightbackground=Fun_Rgb(C_Pal5),
                                  text = 'Next', command = cmd_Next_3)
    btnNext.config(font = ("Arial",15))
    btnNext.place(x=aux_width_monitor*7, y=aux_height_monitor*7)
    
    btnSkip = tkinter.Button(root,  bd=0, fg = Fun_Rgb(C_Pal5),
                                  bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                  highlightbackground=Fun_Rgb(C_Pal5),
                                  text = 'Skip', command = cmd_Next_4)
    btnSkip.config(font = ("Arial",15))
    btnSkip.place(x=aux_width_monitor*4.5, y=aux_height_monitor*7)


def cmd_Next():
    """
    Download all the files selected by the user and try to unzip it
    """
    global path_file
    path_file = filedialog.askdirectory(title = "Save Data")
    
    canvas.destroy()
    text.delete('1.0', END)
    lblDownloads.destroy()
    checkWTS.destroy()
    checkL_WTS.destroy()
    checkL_Waldenpy.destroy()
    checkL_Waldino.destroy()
    checkL_Arduino.destroy()
    show_text('\n  Downloading packages... \n')
    root.update()
    
    if WTS.get() == 1:
#        os.system('wget -P '+path_file +' https://github.com/YancarloOjeda/WTS-2.01/archive/master.zip')
        os.system('wget -P '+path_file +' http://walden-me.com/Resources/WTS-2.01.zip')
        show_text('   Download WTS-2.01\n')
        root.update()
        try:
            os.system('unzip '+path_file +'/master.zip')
            os.system('mv WTS-2.01-master WTS-2.01')
            os.system('unzip '+path_file +'/WTS-2.01.zip')
        except NameError: 
            show_text(NameError)
            
        
    
    if L_WTS.get() == 1:
        os.system('wget -P '+path_file +' http://walden-me.com/Resources/L-WTS.zip')
        show_text('   Download WTS Libraries\n')
        root.update()
        try:
            os.system('unzip '+path_file +'/L-WTS.zip')
        except NameError: 
            show_text(NameError)
    
    if Waldenpy.get() == 1:
        os.system('wget -P '+path_file +' http://walden-me.com/Resources/Waldenpy.zip')
        show_text('   Download Waldenpy Libraries\n')
        root.update()
        try:
            os.system('unzip '+path_file +'/Waldenpy.zip')
        except NameError: 
            show_text(NameError)
        
    if Waldino.get() == 1:
        os.system('wget -P '+path_file +' http://walden-me.com/Resources/Waldino.zip')
        show_text('   Download Walduino Libraries\n')
        root.update()
        try:
            os.system('unzip '+path_file +'/Waldino.zip')
        except NameError: 
            show_text(NameError)
    
    if Arduino.get() == 1:
        os.system('wget -P '+path_file +' http://walden-me.com/Resources/arduino-1.8.12-windows.zip')
        show_text('   Download Arduino Libraries\n')
        root.update()
        try:
            os.system('unzip '+path_file +'/arduino-1.8.12-windows.zip')
        except NameError: 
            show_text(NameError)
    
    
    text.insert(INSERT, '  Download completed. Press Next to continue \n')
    
    btnNext = tkinter.Button(root,  bd=0, fg = Fun_Rgb(C_Pal5),
                                  bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                  highlightbackground=Fun_Rgb(C_Pal5),
                                  text = 'Next', command = cmd_Next_2)
    btnNext.config(font = ("Arial",15))
    btnNext.place(x=aux_width_monitor*7, y=aux_height_monitor*7)
    
        
    root.update()
    
     
    
def cmd_Cancel():
    root.destroy()

#%%------------TEXT SPACE----------------------------------------------------------
text = Text(root, width = int(aux_width_monitor*8), height = int(aux_height_monitor*8))
text.config(font=("Arial",15))
text.pack()


#%%------------CHECK BUTTONS----------------------------------------------------------
WTS = tkinter.IntVar()      
L_WTS = tkinter.IntVar() 
Waldenpy = tkinter.IntVar()
Waldino = tkinter.IntVar() 
Arduino = tkinter.IntVar()     

lblDownloads = tkinter.Label(root, text="Select all package to download", 
                             background=Fun_Rgb(C_Pal5),  borderwidth=1,
                             font = ("Arial",18, "normal"))
lblDownloads.place(x=aux_width_monitor * .2, y=aux_height_monitor*.5)


checkWTS = tkinter.Checkbutton(root, text="WTS-2.01", variable=WTS, 
            onvalue=1, offvalue=0, background=Fun_Rgb(C_Pal5),  borderwidth=0,
            font = ("Arial",15, "normal"), bd=0, highlightthickness=0)
checkWTS.place(x=aux_width_monitor * .3, y=aux_height_monitor*1.2)

checkL_WTS = tkinter.Checkbutton(root, text="WTS libraries",variable=L_WTS, 
            onvalue=1, offvalue=0, background=Fun_Rgb(C_Pal5),  borderwidth=0,
            font = ("Arial",15, "normal"), bd=0, highlightthickness=0)
checkL_WTS.place(x=aux_width_monitor * .3, y=aux_height_monitor*1.9)

checkL_Waldenpy = tkinter.Checkbutton(root, text="Waldenpy",variable=Waldenpy, 
            onvalue=1, offvalue=0, background=Fun_Rgb(C_Pal5),  borderwidth=0,
            font = ("Arial",15, "normal"), bd=0, highlightthickness=0)
checkL_Waldenpy.place(x=aux_width_monitor * .3, y=aux_height_monitor*2.6)

checkL_Waldino = tkinter.Checkbutton(root, text="Waldino ",variable=Waldino, 
            onvalue=1, offvalue=0, background=Fun_Rgb(C_Pal5),  borderwidth=0,
            font = ("Arial",15, "normal"), bd=0, highlightthickness=0)
checkL_Waldino.place(x=aux_width_monitor * .3, y=aux_height_monitor*3.3)

checkL_Arduino = tkinter.Checkbutton(root, text="Arduino",variable=Arduino, 
            onvalue=1, offvalue=0, background=Fun_Rgb(C_Pal5),  borderwidth=0,
            font = ("Arial",15, "normal"), bd=0, highlightthickness=0)
checkL_Arduino.place(x=aux_width_monitor * .3, y=aux_height_monitor*4)


#%%------------BUTTONS NEXT AND CANCEL----------------------------------------------------------
btnNext = tkinter.Button(root,  bd=0, fg = Fun_Rgb(C_Pal5),
                                  bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                  highlightbackground=Fun_Rgb(C_Pal5),
                                  text = 'Next', command = cmd_Next)
btnNext.config(font = ("Arial",15))
btnNext.place(x=aux_width_monitor*7, y=aux_height_monitor*7)
CreateToolTip(btnNext, text = 'Press Next to install libraries')

btnCancel = tkinter.Button(root,  bd=0, fg = Fun_Rgb(C_Pal5),
                                  bg = Fun_Rgb(C_Pal2), activebackground=Fun_Rgb(C_Pal4),
                                  highlightbackground=Fun_Rgb(C_Pal5),
                                  text = 'Cancel', command = cmd_Cancel)
btnCancel.config(font = ("Arial",15))
btnCancel.place(x=aux_width_monitor*5.5, y=aux_height_monitor*7)
CreateToolTip(btnCancel, text = 'Press Cancel to abort installation')

#%%------------WALDEN IMAGES----------------------------------------------------------
imgLogo = Fun_Size(Dir_Images  +'interfaz-01.png',.2*aux_size)
lblLogo = Label(root, bg = Fun_Rgb(C_White), 
                                    image = imgLogo)
lblLogo.place(x=aux_width_monitor*.1,y=aux_height_monitor*6.5)


canvas = tkinter.Canvas(root, bg = Fun_Rgb(C_White), bd=0, highlightthickness=0) # use canvas
canvas.place(x=aux_width_monitor*4,y=aux_height_monitor*.5)


#images
my_images = []
my_images.append(Fun_Size(Dir_Images  +'Menu_1.png',.4*aux_size))
my_images.append(Fun_Size(Dir_Images  +'Menu_2.png',.4*aux_size))
my_images.append(Fun_Size(Dir_Images  +'Menu_3.png',.4*aux_size))
my_images.append(Fun_Size(Dir_Images  +'Menu_4.png',.4*aux_size))
my_image_number = 0


#%%------------ANIMATION----------------------------------------------------------
def animation(x_move, y_move):
    global my_image_number
    image_on_canvas = canvas.create_image(150,100, image=my_images[my_image_number])
    canvas.move(image_on_canvas, x_move, y_move) # movement
    canvas.update()
    canvas.after(1500) # milliseconds in wait time, this is 50 fps
  
    my_image_number += 1
    if my_image_number == len(my_images):
        my_image_number = 0
        
    canvas.after(20, animation, x_move, y_move)# loop variables and animation, these are updatable variables
    

animation(20, 20)


root.mainloop()
