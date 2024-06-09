import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
data = pd.read_csv('datos.csv')

def create_and_save_plots(data, ticks_interval):
    for column in data.columns[1:]:
        # Crear una nueva figura
        plt.figure()

        # Crear una gráfica de barras
        plt.bar(data['Número de Simulación'], data[column]) 

        # Mostrar cada n ticks
        plt.xticks(data['Número de Simulación'][::ticks_interval])

        # Establecer el título de la gráfica
        plt.title(column)

        # Establecer los nombres de los ejes
        plt.xlabel('Número de Simulación')
        plt.ylabel(column)

        # Guardar la gráfica como un archivo PDF
        plt.savefig(f'{column}.pdf')

        # Cerrar la figura
        plt.close()