# -*- coding: utf-8 -*-
"""
Walden Modular Equipment 2019
Tracking_2_ESP
"""

import WaldenTrackingSystem as wts

#Variables
Tiempo = 5
ContadorTiempo = 0
ContadorDistancia = 0
X = 0
Y = 0
TempX = 0
TempY = 0

#Configuracion y Dispositivos
Parametros = wts.Open_Image_0('C')
WebCam = wts.Star_WebCam(Parametros)

TempTiempo = wts.Get_Time()

while(ContadorTiempo <= Tiempo):
    
    wts.Flush_WebCam()
    Imagen = wts.Get_WebCam(WebCam)
    
    Imagen, X, Y = wts.Tracking(Imagen, Parametros)

    wts.Show_WebCam_Tracking(Imagen, ContadorTiempo,X,Y,ContadorDistancia)
    
    # Distance(X1,Y1,X1,Y2)
    # Esta función te permitirá calcular la distancia entre dos puntos. En este
    # ejemplo particular la posición presente respecto de la posición pasada 
    # *NOTA: es importante actualizar la posición pasada 
    Distancia = wts.Distance(X,Y,TempX,TempY)
    TempX = X
    TempY = Y
    ContadorDistancia = round(ContadorDistancia + Distancia,3)
    # *NOTA: La función round(numero, decimales) te permite redondear un numero  


    ContadorTiempo = wts.Timer(ContadorTiempo,TempTiempo,.01)
    TempTiempo = wts.Get_Time()
    
wts.Stop_WebCam(WebCam)
