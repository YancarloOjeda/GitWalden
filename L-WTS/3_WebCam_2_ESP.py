# -*- coding: utf-8 -*-
"""
Walden Modular Equipment 2019
WebCam_2_ESP
"""

import WaldenTrackingSystem as wts

#Variables
Tiempo = 5
ContadorTiempo = 0

#Configuracion y Dispositivos
Parametros = wts.Open_Image_0('C')
WebCam = wts.Star_WebCam(Parametros)

# Get_Time()
# Esta función te permitirá obtener el tiempo real
TempTiempo = wts.Get_Time()

while(ContadorTiempo <= Tiempo):
    
    wts.Flush_WebCam()
    Imagen = wts.Get_WebCam(WebCam)
    wts.Show_WebCam(Imagen)
    
    # Timer(Contador,TiempoReal,Pausa)
    # Esta función te permitirá calcular el tiempo y agregar una pausa en 
    # segundos para controlar el número de frames 
    # *NOTA: es importante obtener el tiempo real después de utilizar esta 
    # función 
    ContadorTiempo = wts.Timer(ContadorTiempo,TempTiempo,.05)
    print(ContadorTiempo)
    TempTiempo = wts.Get_Time()
    
wts.Stop_WebCam(WebCam)
