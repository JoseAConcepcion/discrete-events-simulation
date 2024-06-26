import math
import sys
import csv
import numpy as np
from randomV import Exponential


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
    entryMaintanance:{int,float} = {}
    queue:int = 0
    maxQueueValue:int = 0
    initialTime = Exponential(poissonLambda)
    entryTime = initialTime
    exitTime = math.inf
    
    #todo export to csv to work with statistics later
    while True:
        
        if(entryTime<=exitTime and entryTime <= timeLimit):
            time = entryTime
            numberOfEntries+=1
            queue+=1
            if(queue>maxQueueValue):
                maxQueueValue = queue
            next = Exponential(poissonLambda)
            entryTime = time + next

            if(queue==1):
                ex = Exponential(exponentialLambda)
                exitTime = time+ex
                entryMaintanance[numberOfEntries] = time + ex
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
            entryMaintanance[numberOfExits + 1] = time
        
        if(min(entryTime,exitTime) == entryTime and entryTime>timeLimit):
            entryTime = math.inf
        
            while(queue>0):
                time = exitTime
                numberOfExits+=1
                queue-=1
        
                if(queue>0):
                    exitTime = time + Exponential(exponentialLambda)
        
                Exits[numberOfExits] = time
                entryMaintanance[numberOfExits+1] = time
        
            return (Entries, Exits, maxQueueValue, entryMaintanance)


def Compute(initialCost, partialCost, lambdaE:float, lambdaP:float, topTime:float):
    Entries, Exits, maxQueueValue, entrySys = Simulation(lambdaE, lambdaP, topTime)
    counter = 0
    counterSys = 0
    for i in range(len(Entries)):
        counter += abs(Entries[i+1]-Exits[i+1])
        counterSys += abs(Exits[i+1]-entrySys[i+1])
        # print("costo hasta ahora", counter)
    entryIndex = 1
    repairIndex = 1
    exitIndex = 1
    cs = 0
    cq = 0
    cantS = 0
    cantC = 0
    for i in range(topTime*365):
        while True:
            check = True
            if(entryIndex<len(Entries) and i>=Entries[entryIndex]):
                cantS+=1
                cs += cantS
                entryIndex+=1
                check = False
            if(repairIndex<len(entrySys) and i>=entrySys[repairIndex]):
                cantC += 1
                cq += cantC
                repairIndex+=1
                check = False
            if(exitIndex<len(Exits) and i>=Exits[exitIndex]):
                exitIndex+=1
                cantS -=1
                cantC -= 1
                cs += cantS
                cq += cantC
                check = False
            if(check):
                break
    MeanSysCant = cs/(topTime*365)
    MeanQueueCant = cq/(topTime*365)  
    print('MeanSysCant: ',MeanSysCant)
    print('MeanQueueCant: ',MeanQueueCant)  
    cost = initialCost + counter*partialCost
    meanSysTime = counter/len(Entries.items())
    meanQueueTime = (counter - counterSys)/len(Entries.items())
    meanRepairTime = counterSys/ len(Entries.items())
    print()
    print('CounterSYS: ', str(counterSys))
    print('MeanRepairTime', str(meanRepairTime))
    print()
    # print('Entries: ',Entries)
    # print('Exits: ',Exits)
    # print('RepairEntrances: ', entrySys)
    print('Tiempo promedio en sistema: ', str(meanSysTime))
    print('Tiempo promedio en cola: ', str(meanQueueTime))
    print('Tiempo promedio en reparacion: ', str(meanRepairTime))
    return (cost, maxQueueValue, meanSysTime, meanQueueTime, meanRepairTime)
