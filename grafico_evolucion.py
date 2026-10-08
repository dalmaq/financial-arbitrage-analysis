import csv
import matplotlib.pyplot as plt

# Guardamos los datos de cada ruta
fechas = {}
rendimientos = {}
# Leemos el archivo CSV 
with open ("resultados_arbitraje.csv", "r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        # Ignoramos posibles filas de encabezado repetidas 
        if fila ["Fecha y hora"] == "Fecha y hora":
           continue 

        ruta = fila["Ruta"]
        fecha = fila["Fecha y hora"]
        rendimiento = float(fila["Rendimiento"])

        if ruta not in fechas:
            fechas[ruta] = []

        if ruta not in rendimientos:
            rendimientos[ruta] = []  

        fechas[ruta].append (fecha)
        rendimientos[ruta].append (rendimiento)

    # Creamos el grafico
    plt.figure(figsize=(12,7))    

    for ruta in rendimientos:
        ejecuciones = range (1, len (rendimientos[ruta]) + 1)
        plt.step(
            fechas [ruta],
            rendimientos [ruta],
            where="post",
            marker="o",
            markersize=5,
            linewidth=2,
            label=ruta
        )

    # Titulo y etiquetas
    plt.title(
        "Evolucion del rendimiento de las rutas de arbitraje",
        fontsize=16,
        fontweight="bold"
    )
    plt.xlabel("Numero de ejecucion", fontsize=11)
    plt.ylabel("Rendimiento (%)", fontsize=11)
    # Cuadricula suave
    plt.grid (
        axis="y",
        linestyle="--",
        alpha=0.3
    )
    # Leyenda
    plt.legend (
        title="Ruta",
        loc="best"
    )
    # Giramos las fechas para que sean legibles
    plt.xticks (
        rotation=45,
        ha="right"
    )
    # Ajustamos automaticamente los espacios
    plt.savefig (
        "grafico_evolucion.png",
        dpi=300,
        bbox_inches="tight"
    )
    # Mostramos el grafico
    plt.show ()
    





    