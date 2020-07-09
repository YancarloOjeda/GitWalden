"""
Walden Modular Equipment 2019
Zone_ESP
"""

import WaldenTrackingSystem as wts

#Variables
Tiempo = 20

#Variables Control
ContadorTiempo = 0
ContadorFrames = 0
ContadorDistancia = 0
X = 0
Y = 0
TempX = 0
TempY = 0

#Variables registro
Datos = ''
DatoZona = 0 

#Configuracion y Dispositivos
Parametros = wts.Open_Image_0('d')
WebCam = wts.Star_WebCam(Parametros)
Zona = wts.Create_Zone(Parametros,.5,0,1,1)
#WPI = wts.Get_WPI('COM19')

TempTiempo = wts.Get_Time()

while(ContadorTiempo <= Tiempo):
    
    wts.Flush_WebCam()
    Imagen = wts.Get_WebCam(WebCam)
    Imagen, X, Y = wts.Tracking(Imagen, Parametros)
    
    #Mostrar Zona
    wts.Show_WebCam_Tracking_Zone(Imagen,round(ContadorTiempo,2),int(X),int(Y),DatoZona,Zona)
    
    #Distancia
    Distancia = wts.Distance(X,Y,TempX,TempY)
    TempX = X
    TempY = Y
    ContadorDistancia = round(ContadorDistancia + Distancia,3)
    
    #Zona
    DatoZona = wts.InZone(Zona,X,Y)
    
    #Datos 
    Eventos = str(DatoZona)
    Datos = wts.MOTUS(Datos,ContadorFrames,ContadorTiempo,X,Y,Distancia,Eventos,0)
    ContadorFrames += 1
    DatoRespuesta = 0;

    #Timer
    ContadorTiempo = wts.Timer(ContadorTiempo,TempTiempo,.01)
#    print(ContadorHabituacion)
    TempTiempo = wts.Get_Time()
    
    
wts.Stop_WebCam(WebCam)
wts.MOTUS_Export(Datos)