"""
Walden Modular Equipment 2019
Arduino_Out_2_ESP
"""

import WaldenTrackingSystem as wts

#Variables
Tiempo = 10
ContadorTiempo = 0
TiempoOn = 2
TiempoOff = 4
ContadorEvento = 0

#Configuracion y Dispositivos
WPI = wts.Get_WPI('COM19')


TempTiempo = wts.Get_Time()

while(ContadorTiempo <= Tiempo):
    
    if ContadorEvento >= TiempoOff:
        wts.WPI_Out(WPI,'b')
        ContadorEvento = 0
    elif ContadorEvento >= TiempoOn:
        wts.WPI_Out(WPI,'a')

    ContadorTiempo = wts.Timer(ContadorTiempo,TempTiempo,.05)
    # Event_Timer(TimeCounter,TempEvent)
    # Esta función te permitirá programar contadores extras para controlar 
    # los tiempos de los eventos 
    ContadorEvento = wts.Event_Timer(ContadorEvento,TempTiempo)
    print(ContadorEvento)
    TempTiempo = wts.Get_Time()
    

# *NOTA: es importante al finalizar el programa apagar los dispositivos  
wts.WPI_Out(WPI,'b')
wts.Stop_WPI(WPI)