# -*- coding: utf-8 -*-
"""
Walden Modular Equipment 2019
Tracking_MOTUS_ESP
MOTUS(Leon, 2019)
"""

import WaldenTrackingSystem as wts

#Variables
Tiempo = 5
ContadorTiempo = 0
ContadorDistancia = 0
ContadorFrames = 0
X = 0
Y = 0
TempX = 0
TempY = 0
Datos = ''

#Configuracion y Dispositivos
Parametros = wts.Open_Image_0('C')
WebCam = wts.Star_WebCam(Parametros)

TempTiempo = wts.Get_Time()

while(ContadorTiempo <= Tiempo):
    
    wts.Flush_WebCam()
    Imagen = wts.Get_WebCam(WebCam)
    
    Imagen, X, Y = wts.Tracking(Imagen, Parametros)

    wts.Show_WebCam_Tracking(Imagen, ContadorTiempo,X,Y,ContadorDistancia)
    
    Distancia = wts.Distance(X,Y,TempX,TempY)
    TempX = X
    TempY = Y
    ContadorDistancia = round(ContadorDistancia + Distancia,3)
    
    # MOTUS(Data,Frame,Time,X,Y,Distance,Event,Show = 1 or 0)
    # Esta función te permitirá registrar los datos en el formato MOTUS 
    # (Leon, 2019). Deberás cuidar el orden le los argumentos de entrada: 
    # Datos, Frames, Tiempo, X, Y, Distancia, Eventos. El ultimo comando te 
    # permitirá ver en la ventana comando los datos (1 = true, 0 = False)
    Datos = wts.MOTUS(Datos,ContadorFrames,ContadorTiempo,X,Y,Distancia,0,1)

    ContadorTiempo = wts.Timer(ContadorTiempo,TempTiempo,.01)
    TempTiempo = wts.Get_Time()
    
wts.Stop_WebCam(WebCam)

# MOTUS_Export(Data)
# Esta función te permitirá exportar los datos generados por MOTUS (Leon, 2019) 
wts.MOTUS_Export(Datos)
