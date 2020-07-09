"""
Walden Modular Equipment 2019
Zone_ESP
"""

import WaldenTrackingSystem as wts

#Variables
Tiempo = 40

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
ZonaSujeto = 0

#Configuracion y Dispositivos
Parametros = wts.Open_Image_0('e')
WebCam = wts.Star_WebCam(Parametros)
Zona1 = wts.Create_Zone(Parametros,0,0,.45,.45)
Zona2 = wts.Create_Zone(Parametros,.55,0,1,.45)
Zona3 = wts.Create_Zone(Parametros,0,.55,.45,1)
Zona4 = wts.Create_Zone(Parametros,.55,.55,1,1)

TempTiempo = wts.Get_Time()

while(ContadorTiempo <= Tiempo):
    
    wts.Flush_WebCam()
    Imagen = wts.Get_WebCam(WebCam)
    Imagen, X, Y = wts.Tracking(Imagen, Parametros)
    
    #Mostrar Zona
    wts.Show_WebCam_Tracking_Zone_C(Imagen,round(ContadorTiempo,2),int(X),int(Y),ZonaSujeto,Zona1,(0,0,255))
    wts.Show_WebCam_Tracking_Zone_C(Imagen,round(ContadorTiempo,2),int(X),int(Y),ZonaSujeto,Zona2,(0,255,0))
    wts.Show_WebCam_Tracking_Zone_C(Imagen,round(ContadorTiempo,2),int(X),int(Y),ZonaSujeto,Zona3,(255,0,0))
    wts.Show_WebCam_Tracking_Zone_C(Imagen,round(ContadorTiempo,2),int(X),int(Y),ZonaSujeto,Zona4,(0,255,255))
    
    #Distancia
    Distancia = wts.Distance(X,Y,TempX,TempY)
    TempX = X
    TempY = Y
    ContadorDistancia = round(ContadorDistancia + Distancia,3)
    
    #Zona
    DatoZona1 = wts.InZone(Zona1,X,Y)
    DatoZona2 = wts.InZone(Zona2,X,Y)
    DatoZona3 = wts.InZone(Zona3,X,Y)
    DatoZona4 = wts.InZone(Zona4,X,Y)
    if DatoZona1 == 1:
        ZonaSujeto = 1
    elif DatoZona2 == 1:
        ZonaSujeto = 2
    elif DatoZona3 == 1:
        ZonaSujeto = 3
    elif DatoZona4 == 1:
        ZonaSujeto = 4
    else:
        ZonaSujeto = 0
        
        
    
    #Datos 
    Eventos = str(ZonaSujeto)
    Datos = wts.MOTUS(Datos,ContadorFrames,ContadorTiempo,X,Y,Distancia,Eventos,0)
    ContadorFrames += 1
    DatoRespuesta = 0;

    #Timer
    ContadorTiempo = wts.Timer(ContadorTiempo,TempTiempo,.01)
#    print(ContadorHabituacion)
    TempTiempo = wts.Get_Time()
    
    
wts.Stop_WebCam(WebCam)
wts.MOTUS_Export(Datos)