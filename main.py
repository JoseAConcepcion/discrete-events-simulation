from simulation import *
from stats import *
import csv
import sys

cant = 0
promM = 0
promG = 0
promH = 0
promHom = 0
promMaq = 0
CostoHombre_total = 0
CostoMaq_total = 0
colaHombres = 0
colaMaquinas = 0

data = []
iterations = 30
days = 300
# Calcular y guardar los datos de cada iteración
for i in range(iterations):
    CostoHombre, maxquee1, meanSysTime1, meanQueueTime1, meanRepairTime1s = Compute(750000, days*24, 4, 3, 60) # 
    CostoMaq, maxquee2, meanSysTime, meanQueueTime, meanRepairTime= Compute(1000000, days*24, 8, 3, 60)
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
    
    data.append([i+1, CostoHombre, maxquee1, CostoMaq, maxquee2, CostoHombre - CostoMaq])

# Calcular promedios y guardar en archivo CSV
with open(f'datos en {days}.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Headers
    headers = ['Número de Simulación', 'Costo de Hombres',
             'Máximo número en colas Hombres', 'Costo de Máquinas', 
             'Máximo número en cola Máquinas', 'Diferencia']
    headers_with_days = [f'{header} en {days} días' for header in headers]
    writer.writerow(headers_with_days)
     # Escribir los datos de cada iteración
    writer.writerows(data)

with open(f'datos extra en {days}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)  
    # Calcular promedios
    promM = promM / cant if cant != 0 else 0
    promH = promH / (iterations - cant) if cant != iterations else 0
    promG = promG / iterations
    CostoHombre_promedio = CostoHombre_total / iterations
    CostoMaq_promedio = CostoMaq_total / iterations

    # Escribir los totales y promedios al final del archivo
    writer.writerow([])
    writer.writerow(['Promedio de las Hombres', promM])
    writer.writerow(['Promedio de los Maquinas', promH])
    writer.writerow(['Promedio General', promG])
    writer.writerow(['Cantidad', cant])
    writer.writerow(['Costo promedio de Hombres', CostoHombre_promedio])
    writer.writerow(['Costo promedio de Maquinas', CostoMaq_promedio])


for i in range(iterations): 
    CostoHombre, maxquee1, meanSysTime, meanQueueTime, meanRepairTime = Compute(750000, days*24, 4, 3, 60) # i va a depender del criterio de parada y i >= 30
    CostoMaq,maxque,emeanSysTime, meanQueueTime, meanRepairTime2 = Compute(1000000,days*24, 8, 3, 60)
    promHom += CostoHombre
    promMaq += CostoMaq
    if(CostoHombre-CostoMaq<0): 
        cant+=1
        promM += abs(CostoHombre-CostoMaq)
    else:
        promH += abs(CostoHombre - CostoMaq)
    promG += abs(CostoHombre-CostoMaq) #esta es la eperanza de la muestra

    colaHombres += maxquee1
    colaMaquinas += maxquee2

if(cant!=0):
    print('Promedio de las Hombres', str(promM/cant))

# print('Promedio de los Maquinas: ',str(promH/(iterations-cant)))
print('Promedio General: ',str(promG/iterations))
print(cant)
print('Costo promedio de Hombres: ', str(CostoHombre/iterations))
print('Costo promedio de Maquinas: ', str(CostoMaq/iterations))
print('Promedio de la cola de Hombres: ', str(colaHombres/iterations))
print('Promedio de la cola de Maquinas: ', str(colaMaquinas/iterations))



data_csv = pd.read_csv(f'datos en {days}.csv')
create_and_save_plots(data_csv, 29, days)
