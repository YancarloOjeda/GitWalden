"""
Walden Modular Equipment 2019
Arduino_Out_ESP
"""

import WaldenTrackingSystem as wts

# Check_Connected_Arduinos()
# Esta función te permite ver los puertos Serial conectados al ordenador 
wts.Check_Connected_Arduinos()

# Get_WPI('COM')
# Esta función te permite conectar un dispositivo y asignarle un nombre  
# *NOTA: verificar con la función anterior si el puerto COM
WPI = wts.Get_WPI('COM19')

# WPI_Out(WPI,'x')
# Esta función te permitirá enviarle una orden a Arduino. 
# *NOTA: deberás verificar la programación de arduino, que comandos 
# corresponder a que eventos 
wts.WPI_Out(WPI,'a')
    
# Pause_Time(Time)
# Esta función te permitirá detener el programa por un tiempo determinado 
wts.Pause_Time(2)
    
# WPI_Out(WPI,'x')
# Esta función te permitirá enviarle una orden a Arduino. 
wts.WPI_Out(WPI,'b')

#Stop_WPI(WPI) 
# Para utilizar el dispositivo en el futuro deberás detenerlo. En su defecto 
# deberás cerrar la terminal que se encuentra en la ventana command 
wts.Stop_WPI(WPI)