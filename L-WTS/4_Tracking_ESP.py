# -*- coding: utf-8 -*-
"""
Walden Modular Equipment 2019
WebCam_ESP
"""

import WaldenTrackingSystem as wts


#Variables
X = 0
Y = 0

#Configuracion y Dispositivos
Parametros = wts.Open_Image_0('C')
WebCam = wts.Star_WebCam(Parametros)


wts.Flush_WebCam()
Imagen = wts.Get_WebCam(WebCam)

# Tracking(Image, Parameters)
# Esta función te permitirá transformar la imagen y obtener la posición X,Y 
# en función de los parámetros obtenidos.
Imagen, X, Y = wts.Tracking(Imagen, Parametros)

# Show_WebCam_Tracking(Imagen, X,Y,0,0)
# Esta función ter permitirá mostrar la imagen en pantalla  y mostrar cuatro 
# variables en pantalla 
wts.Show_WebCam_Tracking(Imagen, X,Y,0,0)


wts.Stop_WebCam(WebCam)



