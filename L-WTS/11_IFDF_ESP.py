# -*- coding: utf-8 -*-
"""
Walden Modular Equipment 2019
IFDF_ESP
MOTUS(Leon, 2019)
"""

import WaldenTrackingSystem as wts

#Variables
Tiempo = 20
IntervaloFijo = 5
DistanciaFija = 30
TiempoConsecuencia = 3
ContadorDistancia = 0
ContadorConsecuencia = 0
ContadorIntervalo = 0
ControlConsecuencia = 0
ContadorTiempo = 0
ContadorFrames = 0
X = 0
Y = 0
TempX = 0
TempY = 0
EventoA = '0'
EventoB = '0'
EventoC = '0'
Datos = ''

#Configuracion y Dispositivos
Parametros = wts.Open_Image_0('J')
WebCam = wts.Star_WebCam(Parametros)
WPI = wts.Get_WPI('COM19')

TempTiempo = wts.Get_Time()

while(ContadorTiempo <= Tiempo):
    
    wts.Flush_WebCam()
    Imagen = wts.Get_WebCam(WebCam)
    Imagen, X, Y = wts.Tracking(Imagen, Parametros)
    
    wts.Show_WebCam_Tracking(Imagen, ContadorTiempo,ContadorDistancia,ContadorConsecuencia,ContadorIntervalo)
    
    
    Distancia = wts.Distance(X,Y,TempX,TempY)
    TempX = X
    TempY = Y
    ContadorDistancia = round(ContadorDistancia + Distancia,3)
    
    if ContadorIntervalo >= IntervaloFijo:  
        EventoB = '3'  
        EventoC = '4'
        if ControlConsecuencia == 1:
            if ContadorConsecuencia >= TiempoConsecuencia:
#                wts.WPI_Out(WPI,'b')
                ContadorDistancia = 0
                ControlConsecuencia = 0
                ContadorIntervalo = 0
                EventoA = '0'
        elif ContadorDistancia >= DistanciaFija:
#            wts.WPI_Out(WPI,'a')
            ControlConsecuencia = 1
            ContadorConsecuencia = 0 
            EventoA = '1' 
        else:
            ContadorConsecuencia = 0 
    elif ContadorIntervalo < IntervaloFijo:
        ContadorDistancia = 0
        ContadorConsecuencia = 0 
        EventoB = '2'
        EventoC = '5'
            
        
    Eventos = EventoA + ';' + EventoB  +  ';' + EventoC

    Datos = wts.MOTUS(Datos,ContadorFrames,ContadorTiempo,X,Y,Distancia,Eventos,1)

    ContadorTiempo = wts.Timer(ContadorTiempo,TempTiempo,.01)
    ContadorConsecuencia = wts.Event_Timer(ContadorConsecuencia,TempTiempo)
    ContadorIntervalo = wts.Event_Timer(ContadorIntervalo,TempTiempo)
    TempTiempo = wts.Get_Time()
    
    
wts.Stop_WebCam(WebCam)
wts.WPI_Out(WPI,'b')
wts.WPI_Out(WPI,'d')
wts.Stop_WPI(WPI)
wts.MOTUS_Export(Datos)
