"""
Walden Modular Equipment 2019
Spyder introduction
"""

# Esto es un comentario 
# Para comentar líneas de código puedes introducir el símbolo 


# Import as 
# te permitiera importar librerías y asignarles un nombre 
# En este caso importaremos la librería WaldenTrackingSystem - como wts
import WaldenTrackingSystem as wts

# El código del programa lo deberá escribir en la ventana script
# En la ventana variables, podrás ver el valor de las variables
# En la ventana Command podrás imprimir valores de las variables, 
# hacer pruebas, observar el progreso del código y ver errores
wts.T_Image()

# print(str)
# Con esta función podrás imprimir String en la ventana comand. 
# Los String se declaran entre comillas ‘’
print('Hola Mundo')

# Declarar variables 
# Para declara variables se utiliza el símbolo =, 
# Integer o int son valores enteros
X = 7
Y = 13
Suma = X + Y
# str te permite transformar un int en str
print(str(Suma)) 
#String o str son cadenas de caracteres
Operacion = 'Suma : '
print(Operacion + str(Suma))

# Sentencias condicionales 
# Te permiten comparar los valores de distintas variables, ==,> ,<, ¡=
# *NOTA: Es importante respetar las tabulaciones 
# *NOTA1: El código corre de arriba abajo 

# if
if X < Y:
    print('Es menor')
    
# if else
if X > Y:
    print('Es mayor')
else:
    print('No es mayor')

# if elif else
if X > Y:
    print('Es mayor')
elif X < Y:
    print('Es menor')
else:
    print('No es mayor ni menor')
    
# And y or
X = 1
Y = 10
Z = 20
# And, se tienen que cumplir ambas condiciones
if (Y < Z) & (Y > X):
    print('Y es menor a Z y mayor X')
# Or, se tiene que cumplir al menos una condición
if (Y < Z) | (Y > X):
    print('Y es menor a Z o mayor X')

# Bucles
    
#While, iterara el código siempre y cuando la condición sea cierta 
# *NOTA: Es importante respetar las tabulaciones 
i = 0
Fin = 10
while(i<=Fin):
    print(i)
    i = i + 1

#For, the code will iterate a finite number of times
for i in range(0, 10):
    print(i)







