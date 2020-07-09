"""
Walden Modular Equipment 2019
A2_ESP
MOTUS(Leon, 2019)
"""

import WaldenTrackingSystem as wts

#Variables
Tiempo = 10
Aproximacion = 5
TiempoConsecuencia = 3
ContadorDistancia = 0
ContadorConsecuencia = 0
ControlConsecuencia = 0
ContadorTiempo = 0
ContadorFrames = 0
X = 0
Y = 0
TempX = 0
TempY = 0
Eventos = ''
Distancia = 0
Datos_S1 = ''
Datos_S2 = ''

#Configuracion y Dispositivos
#*NOTA: Para rastrear dos objetos es necesario cargar dos archivos de 
# configuración.
Parametros_S1 = wts.Open_Image_0('A1')
Parametros_S2 = wts.Open_Image_0('A2')
#*NOTA: para utilizar la Webcam solo es necesarios un archivo de configuración 
WebCam = wts.Star_WebCam(Parametros_S1)
WPI = wts.Get_WPI('COM19')

TempTiempo = wts.Get_Time()

while(ContadorTiempo <= Tiempo):
    
    wts.Flush_WebCam()
    Imagen = wts.Get_WebCam(WebCam)
    # *NOTA: para rastrear ambos sujetos deberás utilizar dos veces la función
    # Tracking
    Imagen_S1, X_S1, Y_S1 = wts.Tracking(Imagen, Parametros_S1)
    Imagen_S2, X_S2, Y_S2 = wts.Tracking(Imagen, Parametros_S2)
    # *NOTA: para visualizar ambos sujetos deberás agregar un numero en la 
    # función Show_WebCam_Tracking2
    wts.Show_WebCam_Tracking(Imagen_S1, ContadorTiempo,Distancia,ContadorConsecuencia,0)
    wts.Show_WebCam_Tracking2(Imagen_S2, ContadorTiempo,0,0,0)
    
    Distancia = round(wts.Distance(X_S1,Y_S1,X_S2,Y_S2),3)
    


    if ControlConsecuencia == 1:
        if ContadorConsecuencia >= TiempoConsecuencia:
            wts.WPI_Out(WPI,'b')
            ContadorDistancia = 0
            ControlConsecuencia = 0
            Eventos = '0'
    elif Distancia <= Aproximacion:
        wts.WPI_Out(WPI,'a')
        ControlConsecuencia = 1
        ContadorConsecuencia = 0  
        Eventos = '1'   



    Datos_S1 = wts.MOTUS(Datos_S1,ContadorFrames,ContadorTiempo,X_S1,Y_S1,0,Eventos,0)
    Datos_S2 = wts.MOTUS(Datos_S2,ContadorFrames,ContadorTiempo,X_S2,Y_S2,0,Eventos,0)

    ContadorTiempo = wts.Timer(ContadorTiempo,TempTiempo,.01)
    ContadorConsecuencia = wts.Event_Timer(ContadorConsecuencia,TempTiempo)
    TempTiempo = wts.Get_Time()
    
    
wts.Stop_WebCam(WebCam)
wts.WPI_Out(WPI,'b')
wts.Stop_WPI(WPI)
wts.MOTUS_Export(Datos_S1)
wts.MOTUS_Export(Datos_S2)