#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Test de Primalidad Probabilístico Miller-Rabin
    Copyright (C) 2012 Darío López Padial (@bukosabino) y César Aguilera (@Cs4r)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

################################################################################
#
#   Ejecución: 
#		$ ./golomb.py <secuencia.txt>
#
#   Objetivo: Dado un ﬁchero conteniendo una secuencia de 0's y 1's determina 
#               que postulados de Golomb cumple.
#
################################################################################
from collections import deque
import sys

# Lectura del archivo
f = open(sys.argv[1], "r")
li = list(f.read())
f.close()
# Borramos caracteres finales como puedan ser '\n' ó '\r'.
while(li[-1] not in ['0','1']):
    li.pop()


################################################################################
# Primer Postulado
################################################################################

if abs(li.count('1') - li.count('0') ) <= 1:
    print "Cumple el postulado 1 de Golomb"
else:
    print "NO Cumple el postulado 1 de Golomb"

################################################################################
# Segundo Postulado
################################################################################

# A la hora de buscar rachas hacer que el primer y último bit sean diferentes
longitud = len(li)
veces = 0
while li[0] == li[-1] and veces != longitud:
    li = li[1:] + li[0:1]
    veces +=1

cont = 1
rachas = {}
# Recorremos todo el periodo, anotando en un diccionario el tamaño de las rachas y el número de cada una encontrada.
# Por ejemplo:
# 000111101011001
# rachas == {1:4, 2:2, 3:1, 4:1}
# Significaría que hay 4 rachas de tamaño 1, 2 rachas de tamaño 2 y 1 de tamaño 3 y 4.
for i in range(longitud-1):
    if li[i] == li[i+1]:
        cont+=1
    else:
        try:
            rachas[cont]+=1
        except KeyError:
            rachas.update({cont: 1})
        cont = 1
    
    # Trato especial para la última racha
    if longitud == i+2:
        try:
            rachas[cont]+=1
        except KeyError:
            rachas.update({cont: 1})

k_max = max(rachas.keys())
try:
    # Si Hay 1 racha de longitud k y 1 racha de lontigud k-1
    postulado2 = (rachas[k_max] == 1) and (rachas[k_max-1] == 1) 
    
    # Comprobar 1 racha longitud k_max-1, 2 rachas longitud k_max-2, 4 rachas longitud k_max-3...
    for k in range(k_max-1,1,-1): # Empieza en k_max-1
        if rachas[k] != rachas[k-1]>>1:
            postulado2 = False
            break
except KeyError:
    postulado2 = False


if postulado2 == True:
    print "Cumple el postulado 2 de Golomb"
else:
    print "NO Cumple el postulado 2 de Golomb"


################################################################################
# Tercer Postulado
################################################################################


distancia_hamming = lambda list1, list2: sum(map(lambda (a,b): a != b, zip(list1,list2)))
desplazada = deque(li)
desplazada.rotate(1)
dist = distancia_hamming(li, desplazada)
postulado3 = True
veces = 1
while veces < longitud-1:
    # Rota una posición 
    desplazada.rotate(1)
    veces+=1
    sig_dist = distancia_hamming(li, desplazada) 
    if dist != sig_dist : # Si la distancia de Hamming no se ha cumplido en alguna comparación, no se cumple el tercer postulado
        postulado3 = False
        break

if postulado3 == True:
    print "Cumple el postulado 3 de Golomb"
else:
    print "NO Cumple el postulado 3 de Golomb"

