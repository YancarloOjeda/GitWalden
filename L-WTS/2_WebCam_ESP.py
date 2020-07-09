# -*- coding: utf-8 -*-
"""
Walden Modular Equipment 2019
WebCam_ESP
"""

import WaldenTrackingSystem as wts

# Open_Image_0(Proyecto_Config)
# Esta función te permitirá cargar los parámetros del proyecto (Interfaz)
# Es importante que tu archivo se encuentre en la carpeta proyectos  
Parametros = wts.Open_Image_0('C')

# Star_WebCam(Parametros)
# Esta función te permitirá iniciar la webcam
WebCam = wts.Star_WebCam(Parametros)

# Flush_WebCam()
# Esta función te permitirá reiniciar la imagen de la WebCam
wts.Flush_WebCam()

# Get_WebCam(WebCam)
# Esta función te permitirá captura un frame, recuerda el argumento de la 
# función deberá ser el que declaraste anteriormente como webcam
Imagen = wts.Get_WebCam(WebCam)

# Show_WebCam(Imagen)
# Esta función ter permitirá mostrar la imagen en pantalla 
wts.Show_WebCam(Imagen)

# Stop_WebCam(WebCam)
# Para utilizar la webcam en el futuro deberás detenerla. En su defecto 
# deberás cerrar la terminal que se encuentra en la ventana command 
wts.Stop_WebCam(WebCam)
