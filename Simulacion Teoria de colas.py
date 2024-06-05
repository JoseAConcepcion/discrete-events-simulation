import math
import sys
import csv
import numpy as np
from VariablesAleatorias import Exponential


#Descripcion del problema donde el tiempo de servicio posee una distribucion
#Exponencial y el tiempo de llegada una distribucion de Poisson. Ademas se tiene
#un costo inicial del programa y un costo por hora para cada ordenador inactivo


def Simulation(exponentialLambda:float, poissonLambda:float, timeLimit:float):
    time:float = 0
    entryTime:float = 0
    exitTime:float = 0
    numberOfEntries:int = 0
    numberOfExits:int = 0
    Entries:{int,float} = {}
    Exits:{int,float} = {}
    queue:int = 0
    initialTime = Exponential(poissonLambda)
    entryTime = initialTime
    exitTime = math.inf
    
    #todo export to csv to work with statistics later
    while True:
        # print('General Time: ' + str(time))
        # print('Entry Time: ' + str(entryTime)) 
        # print('Exit Time: ' + str(exitTime)) 
        # print('Top Time: ' + str(timeLimit)) 
        # print('Number of Actives: ' + str(queue))
        # print('Total de ordenadores: ' + str(len(Entries.keys())))
        # print()
        
        if(entryTime<=exitTime and entryTime <= timeLimit):
            time = entryTime
            numberOfEntries+=1
            queue+=1
            next = Exponential(poissonLambda)
            entryTime = time + next

            if(queue==1):
                ex = Exponential(exponentialLambda)
                exitTime = time+ex
            Entries[numberOfEntries] = time #? esto deberia subirse
        
        if(exitTime<entryTime):
            time = exitTime
            numberOfExits+=1
            queue-=1

            if(queue==0): 
                exitTime = math.inf
            else:
                next = Exponential(exponentialLambda)
                exitTime = time+next
            Exits[numberOfExits] = time
        
        if(min(entryTime,exitTime) == entryTime and entryTime>timeLimit):
            entryTime = math.inf
        
            while(queue>0):
                time = exitTime
                numberOfExits+=1
                queue-=1
        
                if(queue>0):
                    exitTime = time + Exponential(exponentialLambda)
        
                Exits[numberOfExits] = time
        
            return (Entries,Exits)


def Compute(initialCost, partialCost, lambdaE:float, lambdaP:float, topTime:float):
    Entries, Exits = Simulation(lambdaE, lambdaP,topTime)
    counter = 0
    for i in range(len(Entries)):
        counter += abs(Entries[i+1]-Exits[i+1])
        # print("costo hasta ahora", counter)
    cost = initialCost + counter*partialCost
    return cost

# sys.stdout = open("output.txt", 'w')
# CostoA = Compute(750000, 150*24, 4, 3,365)
# # sys.stdout.close() 

# # sys.stdout = open("output2.txt", 'w')
# CostoB = Compute(1000000,150*24, 8, 3, 365)
# # sys.stdout.close() 

# print(CostoA)
# print(CostoB)
# print(CostoA-CostoB)


# sys.stdout = open("Datos auxiliares.txt", 'w')

cant = 0
promM = 0
promG = 0
promH = 0
promHom = 0
promMaq = 0
CostoHombre_total = 0
CostoMaq_total = 0

data = []

# Calcular y guardar los datos de cada iteración
for i in range(500):
    CostoHombre = Compute(750000, 150*24, 4, 3, 60)
    CostoMaq = Compute(1000000, 150*24, 8, 3, 60)
    promHom += CostoHombre
    promMaq += CostoMaq
    CostoHombre_total += CostoHombre
    CostoMaq_total += CostoMaq
    if CostoHombre - CostoMaq < 0:
        cant += 1
        promM += abs(CostoHombre - CostoMaq)
    else:
        promH += abs(CostoHombre - CostoMaq)
    promG += abs(CostoHombre - CostoMaq)
    
    data.append([i+1, CostoHombre, CostoMaq, abs(CostoHombre - CostoMaq)])

# Calcular promedios y guardar en archivo CSV
with open('datos.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    # Escribir encabezados
    writer.writerow(['Iteración', 'Costo Hombre', 'Costo Maquina', 'Diferencia'])

    # Escribir los datos de cada iteración
    writer.writerows(data)

    # Calcular promedios
    promM = promM / cant if cant != 0 else 0
    promH = promH / (500 - cant)
    promG = promG / 500
    CostoHombre_promedio = CostoHombre_total / 500
    CostoMaq_promedio = CostoMaq_total / 500

    # Escribir los totales y promedios al final del archivo
    writer.writerow([])
    writer.writerow(['Promedio de las Hombres', promM])
    writer.writerow(['Promedio de los Maquinas', promH])
    writer.writerow(['Promedio General', promG])
    writer.writerow(['Cantidad', cant])
    writer.writerow(['Costo promedio de Hombres', CostoHombre_promedio])
    writer.writerow(['Costo promedio de Maquinas', CostoMaq_promedio])


for i in range(500): 
    CostoHombre = Compute(750000, 150*24, 4, 3, 60) # i va a depender del criterio de parada y i >= 30
    CostoMaq = Compute(1000000,150*24, 8, 3, 60)
    promHom += CostoHombre
    promMaq += CostoMaq
    if(CostoHombre-CostoMaq<0): 
        cant+=1
        promM += abs(CostoHombre-CostoMaq)
    else:
        promH += abs(CostoHombre - CostoMaq)
    promG += abs(CostoHombre-CostoMaq) #esta es la eperanza de la muestra

if(cant!=0):
    print('Promedio de las Hombres', str(promM/cant))

print('Promedio de los Maquinas: ',str(promH/(500-cant)))
print('Promedio General: ',str(promG/500))
print(cant)
print('Costo promedio de Hombres: ', str(CostoHombre/500))
print('Costo promedio de Maquinas: ', str(CostoMaq/500))


sys.stdout.close()