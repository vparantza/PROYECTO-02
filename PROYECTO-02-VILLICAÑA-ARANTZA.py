# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 23:26:06 2020

@author: Arantza
"""

import csv
#Antes que nada, declaramos un lista global que usaremos a lo largo de todo el código y no volver a hacer uso del with
datos = []
rutas = []
ruta_auxiliar = []
transporte = []
transporte_count = []
lista_importaciones = []
lista_exportaciones = []
lista_auxiliar = []
promedio_exportaciones = []
promedio_importaciones = []
x = ""
cont = 0

#Abrimos archivo a utilizar
with open("synergy_logistics_database.csv", "r") as archivo:
        reader = csv.reader(archivo)
        #Hacemos uso de un ciclo for para agregar cada linea del archivos de datos a una lista
        for (linea) in reader:
            datos.append(linea)

#Eliminamos el primer indice de la lista datos que contiene el nombre de las columnas
datos.pop(0)

#Definimos funcion que sera ysada para contabilizar rytas
def rutas_def(direccion):
        lista = []
        lista_auxiliar = []
        #Variables contador para contabilizar las veces que aparece esa ruta
        cont = 0
        valor = 0
        #Ciclo for para recorrer cada elemento dentro de la lista datos
        for elemento in datos:
            #Comparamos si el elemento dentro de indice 1 es igual a la direccion
            if elemento[1] == direccion:
                #Almacenamos la ruta actual
                ruta = elemento[2], elemento[3]
                #Comparamos si ruta se encuentra dentro de las listas de rutas auxiliar
                if ruta not in lista_auxiliar:
                    #Nuevamente recorremos cada elemento dentro de la linea de la lista de datos
                    for elemento2 in datos:
                        #Comprobamos que la ruta (indice 2 y 3) sean igual a la ruta que se esta contando y que la direccion sea la misma
                        if [elemento2[2], elemento2[3]] == [ruta[0], ruta[1]] and elemento2[1] == direccion:
                            #Contabilizamos
                            cont += 1
                    #Agregamos la ruta a la lista auxiliar que almacena todas las rutas 
                    lista_auxiliar.append(ruta)
                    #Agregamos ruta, cantidad y direccion para evitar redundancia
                    lista.append([elemento[2], elemento[3], cont, direccion])
                    #igualamos contador a 0 para la nueva iteracion
                    cont = 0
        return lista

#Se define funcion para obtener porcentajes de valor de cada ruta
def valor_def(lista_exportaciones_aux):
    suma_exportaciones = 0
    #definimos lista auxiliar para guardar valores
    promedio_exportaciones_aux = []
    for valor in lista_exportaciones_aux:
        suma_exportaciones += int(valor[2])
    #Para obetener el promedio de cada valor de cada ruta hacemos una regla de tres por cada elemento
    for elemento in lista_exportaciones_aux:
        valor = ((int(elemento[2])) * 100) / suma_exportaciones
        #agregamos a la lista auxiliar ruta
        promedio_exportaciones_aux.append([elemento[0],  valor])
    return promedio_exportaciones_aux

#Definimos funciones para obtener el porcentaje de cada pais
def paises_top(promedio_exportaciones):
    
    total_promedio_exportaciones = []
    total_promedio_exportaciones_aux = []
    suma_aux = 0
    #Recorremos cada elemento de la lista 
    for pais in promedio_exportaciones:
        pais_aux = pais[0]
        #En caso de que el pais no se encuentre en el pais de lista
        if pais_aux not in total_promedio_exportaciones_aux:
            #Hacemos un nuevo for para evaluar todos los paises e ir sumando los valores de cada uno de ellos
            for valor in promedio_exportaciones:
                if valor[0] == pais_aux:
                    suma_aux += valor[1]
            total_promedio_exportaciones_aux.append(pais_aux)
            total_promedio_exportaciones.append([pais_aux, suma_aux])
            suma_aux = 0
    return total_promedio_exportaciones
 
#Funcion para obtener los paises que conforman el 80% de exportaciones e importaciones
def top_80(lista):
    summ = 0
    top_valor_exp = []
    #Por cada valor de cada paises vamor a irlo sumando hasta que menor o igual a 80
    for elemento in lista:
        if summ <= 80:
            summ += elemento[1]
            top_valor_exp.append(elemento)
    return top_valor_exp
#Este va a ser el menú principal para seleccionar las funciones
print("MENU \n1) RUTAS Y VALORES \n2) TRANSPORTE")
v_menu_principal = input("Ingrese a continuacion la opcion eleccionada: ")

if v_menu_principal == '1':
    a = "Exports"
    b = "Imports"
    
    #A continuacion se ven las diversas funciones definidas en la parte superior siendo llamadas
    lista_exportaciones = rutas_def(a)
    #Y se ordenan de mayor  a menos haciendo uso de la funcion sort
    lista_exportaciones_ordenada = sorted(lista_exportaciones, key = lambda x:x[2], reverse=True)
    lista_importaciones = rutas_def(b)
    lista_importaciones_ordenada = sorted(lista_importaciones, key = lambda x:x[2], reverse=True)
    promedio_exportaciones = valor_def(lista_exportaciones)
    promedio_exportaciones_ordenada = sorted(promedio_exportaciones, key = lambda x:x[1], reverse=True)
    promedio_importaciones = valor_def(lista_importaciones)
    promedio_importaciones_ordenada = sorted(promedio_importaciones, key = lambda x:x[1], reverse=True)
    
    sumatoria_exportaciones = paises_top(promedio_exportaciones)
    sumatoria_exportaciones_ordenada = sorted(sumatoria_exportaciones, key = lambda x:x[1], reverse = True)
    top_80_ex = sorted(top_80(sumatoria_exportaciones_ordenada), key = lambda x:x[1], reverse = True)
    
    sumatoria_importaciones = paises_top(promedio_importaciones)
    sumatoria_importaciones_ordenada = sorted(sumatoria_importaciones, key = lambda x:x[1], reverse = True)
    top_80_im = sorted(top_80(sumatoria_importaciones_ordenada), key = lambda x:x[1], reverse = True)
    
elif v_menu_principal == '2':
    #Definimos lista para ordenar la cuenta
    transporte_ordenado = []
    #Hacemos uso de un metodo for para recorrer todos los tipos de transporte en el indice 7
    #Si hay un transporte no existente en la lista de tipos, se agrega
    for r in datos:
        val_transporte = r[7]
        if val_transporte not in transporte:
            transporte.append(val_transporte)
    #Por cada tipo de transporte hacemos un conteo de todos los movimiento realizados
    for tipo in transporte:
        for a in datos:
            if a[7] == tipo:
                cont += 1
        #Se agrega la cuenta final a una nueva lista que incluya el tipo de transporte y su cuenta
        transporte_count.append([tipo, cont])
        cont = 0
    transporte_ordenado = sorted(transporte_count, key = lambda x:x[1], reverse=True)
        
