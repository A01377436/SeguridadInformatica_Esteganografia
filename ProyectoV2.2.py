#       Seguridad Informática
#       Integrantes:
#           David Alejandro Nicolás Palos
#           Daniel Córdova Bermúdez
#           Guillermo Fidel Navarro Vega
#
#       Implementación de Esteganografía en Python
#
#       Nuestro programa pregunta por una imagen JPG a utilizar
#       Y un texto en consola para ocultar en la imagen
#
#       El método utilizado es el del bit menos significativo, se oculta la información reemplazando cada bit por los del texto
#       Al sér únicamente el último bit el que se modifica, la imágen cambia de manera imperceptible.
#
#       Una vez oculta la información crea un archivo PNG con el nombre Output
#
#       Se puede tambien revelar información oculta en una imagen introduciendo la imagen en PNG e indicando la longitud del mensaje que se ocultó


from PIL import Image #PIL o PILLOW utilizado para la manipulación de imagenes
import numpy as np #Numpy es utilizado para traducir una lista a un arreglo de tuplas

def getPixelesBinarios(pixeles3): #Función encargada de transformar valores enteros a su correspondiente en binario de 7 bits de largo (ASCII)

    #Esto hace posible las operaciones en un bit aislado
    #Recibe una lista 1D de enteros, regresa una lista 1D de binarios

    pixelesBinarios=[]
    for number in pixeles3:
        pixelesBinarios.append((bin(number)[2:]).zfill(7))
    return pixelesBinarios

def getPixeles3(pixeles): #Función encargada de unificar la lista con información de color (Lista de 2 dimensiones) a una lista contunua de 1 dimensión

    #De esta manera trabajar con la información de color se vuelve más sencillo
    #Recibe una lista 2D de enteros, regresa una lista 1D de enteros

    pixeles3=[]
    for pixel in pixeles:
        tempPixel=list(pixel)
        for color in tempPixel:
            pixeles3.append(color)
    return pixeles3

def ocultarInformacion(imageName,texto):#Función principal para ocultar información

    #Abre la imagen, extrae la información, la compara, la modifica y crea una imagen nueva llamada Output.png
    #Imprime la longitud del mensaje guardado, esta información se necesita para el proceso de revelado

    image = Image.open(imageName)
    a = ''.join(format(ord(x), 'b').zfill(7) for x in texto)

    binarios = []
    for letra in a:
        binarios.append(letra)

    X = image.size[0]
    Y = image.size[1]

    espacio = X * Y * 3
    aOcupar = len(binarios)

    if (espacio < aOcupar):
        print("Falta espacio en la imagen")
        return
    else:
        print("Ocultando información en imagen",end="")
        print(".",end="")

    pixeles = list(image.getdata())

    pixeles3 = getPixeles3(pixeles)
    print(".", end="")

    pixelesBinarios = getPixelesBinarios(pixeles3)
    print(".", end="")

    for i in range(0, len(binarios)):
        pixelesBinarios[i] = pixelesBinarios[i][:-1]
        pixelesBinarios[i] = pixelesBinarios[i] + binarios[i]
    print(".", end="")

    pixelesEnteros = []

    for i in range(0, len(pixelesBinarios)):
        pixelesEnteros.append(int(pixelesBinarios[i], 2))

    print(".", end="")

    pixeles4 = [pixelesEnteros[i:i + 3] for i in range(0, len(pixelesEnteros), 3)]
    print(".", end="")

    pixeles5 = []
    for i in range(0, image.size[1]):
        temp = []
        for j in range(0, image.size[0]):
            temp.append(pixeles4[image.size[0] * i + j])
        pixeles5.append(temp)

    print(".")
    print("")

    array = np.array(pixeles5, dtype=np.uint8)
    new_image = Image.fromarray(array)
    new_image.save('Output.png', format='png')
    new_image.close()
    print("Imagen guardada como 'Output.png'\n"+"Longitud del mensaje guardado: "+ str(aOcupar)+"\n")

def revelarInformacion(imageName,aOcupar): #Función principal para revelar información, necesita la longitud del mensaje
    #Abre la imagen, extrae la información, aisla el mensaje oculto, lo imprime en consola.
    image = Image.open(imageName)

    pixeles = list(image.getdata())

    pixeles3 = getPixeles3(pixeles)
    print("Revelando información en imagen", end="")
    print(".", end="")

    pixelesBinarios = getPixelesBinarios(pixeles3)

    print(".", end="")

    mensajeBinario = []
    for i in range(0, aOcupar):
        mensajeBinario.append(pixelesBinarios[i][-1])

    print(".", end="")

    mensajeBinario2 = []

    for i in range(0, int(len(mensajeBinario) / 7)):
        temp = []
        for k in range(0, 7):
            temp.append(mensajeBinario[7 * i + k])
        mensajeBinario2.append(temp)

    print(".", end="")

    for i in range(0, len(mensajeBinario2)):
        mensajeBinario2[i] = "".join(mensajeBinario2[i])

    print(".")

    mensaje = []
    print("\nMensaje encontrado: ",end="")

    for element in mensajeBinario2:
        temp = int(element, 2)
        mensaje.append(chr(temp))
        print(chr(temp), end="")

    print("\n")

def main():#ciclo principal, para realizar más de una tarea hasta que se indique Exit.

    ejecutar=True

    while ejecutar:
        print("Seleccione una ocpción para continuar")
        print("1: Ocultar información en imagen \n2: Revelar información en imagen \n3: Salir")
        seleccion=int(input("Selección: "))

        if seleccion==3:
            ejecutar=False
        elif(seleccion==1):
            imageName=input("Nombre de la imagen en formato JPG con extensión (Ejemplo.jpg): ")
            texto=input("Texto a ocultar: ")
            ocultarInformacion(imageName,texto)
        elif(seleccion==2):
            imageName=input("Nombre de la imagen a revelar en formato PNG con extensión (Ejemplo.png): ")
            aOcupar=int(input("Tamaño del mensaje a revelar: "))
            revelarInformacion(imageName,aOcupar)

main()