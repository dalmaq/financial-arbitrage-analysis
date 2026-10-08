import csv
import matplotlib.pyplot as plt 
from datetime import datetime

fechas = {}
rendimientos = {}

with open ("resultados_arbitraje.csv", "r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        if fila["Fecha y hora"] == "Fecha y hora":
            continue 
        ruta = fila["Ruta"]
        fecha = fila["Fecha y hora"]

        rendimiento = float(fila["Rendimiento"])

        if ruta not in fechas:
            fechas[ruta] = []
        if ruta not in rendimientos:
            rendimientos[ruta] = [] 

        fechas[ruta].append(fecha)
        rendimientos[ruta].append(rendimiento)

for ruta in fechas:
    plt.plot(
        fechas[ruta], 
        rendimientos[ruta],
        marker="o",
        label = ruta
    )
plt.title("Evolucion del rendimiento por ruta")  
plt.xlabel("Fecha y hora")  
plt.ylabel("Rendimiento (%)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("grafico rendimientos.png")

plt.show ()
