#from typing_extensions import ParamSpecArgs
from principal import *
from configuracion import *
from funcionesSeparador import *

import random
import math
import time
import string
from principal import main

segundos = TIEMPO_MAX - pygame.time.get_ticks()/1000

def lectura(archivo, lista):
    for silaba in archivo:
        lista.append(silaba[:-1])

# Actualizar cumple tres roles: generar una silaba aleatoria en pantalla, hacer
# que dicha silaba baje en la pantalla y eliminarla en caso de que su posicion
# en "y" sea menos de 85

def actualizar(silabasEnPantalla,posiciones,listaDeSilabas):
    nueva = nuevaSilaba(listaDeSilabas)
    silabasEnPantalla.append(nueva)
    x = random.randrange(0, 730)
    y = 16
    pos = [x, y]
    posiciones.append(pos)
    time.sleep(0.5)

    for posicion in range(len(posiciones)-1,-1,-1):
        if posiciones[posicion][1] <= ALTO-85:
            posiciones[posicion][1] = posiciones[posicion][1]+20
        else:
            silabasEnPantalla.pop(posicion)
            posiciones.pop(posicion)

# nuevaSilaba genera una silaba al azar

def nuevaSilaba(listaDeSilabas):
    silabas= random.choice(listaDeSilabas)
    return silabas

# quitar elimina de la pantalla las silabas que son parte la palabra que el
# usuario formo

def quitar(candidata, silabasEnPantalla, posiciones):
    silabasDeCandidata = dameSilabas(candidata)
    for silaba in silabasDeCandidata:
        indice = silabasEnPantalla.index(silaba)
        posiciones.pop(indice)
        silabasEnPantalla.pop(indice)

# dameSilabas hace uso de la funcion separador, la cual coloca entre silabas
# una "-", luego se usa el comando split para separar las silabas

def dameSilabas(candidata):
    silabasSeparadas = separador(candidata)
    silabas = silabasSeparadas.split("-")
    return silabas

# Esta funcion se creo para usarla en esValida, recibe tres listas: revisa los
# elementos de la primer lista y si estan en la segunda los añade a la tercera

def iguales(lista,lista2,lista3):
    for silaba in lista:
        if silaba in lista2:
            i=lista.index(silaba)
            lista3.append(silaba)
            lista2.pop(i)


# esValida usa la funcion iguales, la cual devuelve una lista con las silabas de
# candidata que estan en silabasEnPantalla, luego esValida compara esa lista con
# las silabas de candidata y si estan todas verifica que candidata este en el
# lemario

def esValida(candidata, silabasEnPantalla, lemario):
    silabasDeCandidata=dameSilabas(candidata)
    silabasPantalla=silabasEnPantalla[:]
    silabasEnAmbas=[]
    iguales(silabasDeCandidata, silabasPantalla, silabasEnAmbas)
    if silabasEnAmbas==silabasDeCandidata:
        if candidata in lemario:
            return True
        else:
            return False
    else:
        return False

#  Reccore la palabra candidata por letra y las compara con las vocales, conso-
#  nantes y consonantes dificiles, aumentando el contador de puntos por cada re-
#  lacion encontrada

def Puntos(candidata):
    vocales = ["a", "e", "i", "o", "u"]
    consonantes = ["b","c","d","f","g","h","l","m","n","ñ","p","r","s","t","v"]
    consDificil = ["j", "k", "q", "w", "x", "y", "z"]
    puntos=0
    for letra in candidata:
        for vocal in vocales:
            if vocal == letra:
                puntos += 1
        for consonante in consonantes:
            if consonante == letra:
                puntos += 2
        for consonanteD in consDificil:
            if consonanteD == letra:
                puntos += 5
    return puntos


# Esta funcion llama a otras 3: esValida, quitar y Puntos, si esValida verifica
# la palabra llamara a quitar para que borre las silabas en pantalla y sus po-
# siciones, mientras que llama a Puntos para que esta haga la suma de los pun-
# tos y los devuelva al contador

def procesar(candidata, silabasEnPantalla, posiciones, lemario):
    sonidoCorrecto=pygame.mixer.Sound('efectos/correct-ding.wav')
    sonidoIncorrecto=pygame.mixer.Sound('efectos/incorrecto1.wav')
    if (esValida(candidata, silabasEnPantalla, lemario))==True:
        sonidoCorrecto.play()
        quitar(candidata, silabasEnPantalla, posiciones)
        return (Puntos(candidata))
    else:
        sonidoIncorrecto.play()
        return 0




