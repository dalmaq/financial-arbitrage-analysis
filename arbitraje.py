import requests 
import csv 
import os 
from datetime import datetime
def obtener_cotizacion(url):
    respuesta = requests.get(url, timeout = 10)
    respuesta.raise_for_status()
    datos = respuesta.json()
    return datos 
oficial = obtener_cotizacion("https://dolarapi.com/v1/dolares/oficial")
print (oficial)

oficial = obtener_cotizacion("https://dolarapi.com/v1/dolares/oficial")
blue = obtener_cotizacion("https://dolarapi.com/v1/dolares/blue")
mep = obtener_cotizacion("https://dolarapi.com/v1/dolares/bolsa")
cripto = obtener_cotizacion("https://dolarapi.com/v1/dolares/cripto")
tarjeta = obtener_cotizacion("https://dolarapi.com/v1/dolares/tarjeta")

print("Ultima actualizacion de Oficial:", oficial["fechaActualizacion"])
print("Ultima actualizacion de Blue", blue["fechaActualizacion"])
print("Ultima actualizacion de Mep", mep["fechaActualizacion"])
print("Ultima actualizacion de Cripto", cripto["fechaActualizacion"])
print("Ultima actualizacion de Tarjeta", tarjeta["fechaActualizacion"])

print ("Arbitraje financiero")
dolar_oficial_compra = oficial["compra"]
dolar_oficial_venta = oficial["venta"]

dolar_blue_compra = blue["compra"]
dolar_blue_venta = blue["venta"]

dolar_mep_compra = mep["compra"]
dolar_mep_venta = mep["venta"]

dolar_cripto_compra = cripto["compra"]
dolar_cripto_venta = cripto["venta"]

dolar_tarjeta_compra = tarjeta["compra"]
dolar_tarjeta_venta = tarjeta["venta"]

diferencia_oficial = dolar_oficial_venta - dolar_oficial_compra
print ("Diferencia dolar oficial:", diferencia_oficial)

diferencia_blue = dolar_blue_venta - dolar_blue_compra
print ("Diferencia dolar blue:", diferencia_blue)

diferencia_mep = dolar_mep_venta - dolar_mep_compra
print ("Diferencia dolar Mep:", diferencia_mep)

diferencia_cripto = dolar_cripto_venta - dolar_cripto_compra
print ("Diferencia dolar cripto:", round(diferencia_cripto, 2))

diferencia_tarjeta = dolar_tarjeta_venta - dolar_tarjeta_compra
print ("Diferencia dolar tarjeta:", diferencia_tarjeta)

pesos_iniciales = 1000000
dolares_comprados = pesos_iniciales / dolar_oficial_venta
print ("Dolares comprados:", round(dolares_comprados,2))

pesos_finales = dolares_comprados * dolar_blue_compra
print ("Pesos finales", round(pesos_finales,2))

ganancia = pesos_finales - pesos_iniciales
print ("Ganancia o perdida:", round(ganancia,2))

comision = 0.01

costo_comision = pesos_finales * comision
print ("Costo de comision:", round(costo_comision,2))

resultado_final = ganancia - costo_comision
print ("Resultado final:", round(resultado_final,2))

dolares_comprados_mep = pesos_iniciales / dolar_oficial_venta
pesos_finales_mep = dolares_comprados_mep * dolar_mep_compra
ganancia_mep = pesos_finales_mep - pesos_iniciales

print ("Ganancia ruta oficial a Mep:", round(ganancia_mep,2))

def calcular_arbitraje(precio_compra, precio_venta, monto, comisiones=0.01):
    dolares = monto / precio_compra
    pesos = dolares * precio_venta 
    costo_comision = pesos * comisiones
    resultado = pesos - costo_comision - monto
    return resultado 

resultado_blue = calcular_arbitraje(
    dolar_oficial_venta,
    dolar_blue_compra,
    pesos_iniciales
)

print ("Resultado arbitraje oficial a blue:", round(resultado_blue,2))

resultado_mep = calcular_arbitraje(
    dolar_oficial_venta,
    dolar_mep_compra,
    pesos_iniciales
)
print ("Resultado arbitraje oficial a Mep:", round(resultado_mep,2))

resultado_cripto = calcular_arbitraje(
    dolar_oficial_venta,
    dolar_cripto_compra,
    pesos_iniciales
)
print ("Resultado arbitraje oficial a cripto:", round(resultado_cripto,2))

resultado_tarjeta = calcular_arbitraje (
    dolar_oficial_venta,
    dolar_tarjeta_compra,
    pesos_iniciales
)
print ("Resultado arbitraje oficial a tarjeta:", round(resultado_tarjeta,2))

rutas = []
rutas.append ({
    "nombre": "Oficial a Blue",
    "compra": dolar_oficial_venta,
    "venta": dolar_blue_compra
})
rutas.append ({
    "nombre": "Oficial a Mep",
    "compra": dolar_oficial_venta,
    "venta": dolar_mep_compra
})
rutas.append ({
    "nombre": "Oficial a Cripto",
    "compra": dolar_oficial_venta,
    "venta": dolar_cripto_compra
})
rutas.append ({
    "nombre": "Oficial a Tarjeta",
    "compra": dolar_oficial_venta,
    "venta": dolar_tarjeta_compra
})
rutas_ganadoras = []
for ruta in rutas: 
    print (ruta["nombre"])
    print ("Compra:", ruta["compra"])
    print ("Venta:", ruta["venta"])
    resultado = calcular_arbitraje(
        ruta["compra"],
        ruta["venta"],
        pesos_iniciales
    )
    print ("Resultado:", round(resultado,2))
    if resultado > 0: 
        print ("Ganancia")
        ruta["resultado"] = resultado
        rutas_ganadoras.append(ruta)
    else:
        print ("Perdida")

print ("Rutas Ganadoras:")
for ruta in rutas_ganadoras:
    porcentaje = (ruta["resultado"] / pesos_iniciales) * 100
    print (ruta["nombre"], "Resultado:", round(ruta["resultado"],2), "Porcentaje:", round(porcentaje,2), "%")
mejor_ruta = max (rutas_ganadoras, key=lambda ruta: ruta["resultado"])
print ("Mejor resultado:", mejor_ruta["nombre"])    
print ("Ganancia:", round(mejor_ruta["resultado"],2))
porcentaje_mejor = (mejor_ruta["resultado"] / pesos_iniciales) * 100
print ("Porcentaje:", round(porcentaje_mejor,2), "%")

capital_final = pesos_iniciales + mejor_ruta["resultado"]

print ("Capital inicial:", round(pesos_iniciales,2))
print ("Ganancia neta:", round(mejor_ruta["resultado"],2))
print ("Capital final:", round(capital_final,2))

print ("-----Analisis de Rutas-----")
for ruta in rutas:
    print (ruta["nombre"])

    diferencia = ruta["venta"] - ruta["compra"]

    diferencia_porcentual = (
        diferencia / ruta["compra"]
    ) * 100 
    print ("Precio de compra:", ruta["compra"])
    print ("Precio de venta:", ruta["venta"])
    print ("Diferencia:", round(diferencia, 2))
    print ("Diferencia porcentual:", round(diferencia_porcentual, 2), "%")


    resultado = calcular_arbitraje(
        ruta["compra"],
        ruta["venta"],
        pesos_iniciales
    )
    porcentaje = (resultado / pesos_iniciales) * 100 
    print ("Resultado:", round(resultado, 2))
    print ("Rendimiento:", round(porcentaje, 2), "%")
    if  resultado > 0:
        print ("Ruta rentable:", round(resultado, 2))
    else:
        print ("Ruta no rentable:", round(resultado, 2))  

print ("----RESUMEN FINAL----")  
print ("Cantidad de rutas analizadas:", len(rutas))      
print ("Cantidad de rutas rentables:", len(rutas_ganadoras)) 
if len(rutas_ganadoras) == 0: 
    print("No hay rutas rentables")
else:
    print ("Existen rutas rentables") 


print ("---- DETALLE DE RUTAS RENTABLES----")    
for ruta in rutas_ganadoras:
    print ("Ruta:", ruta["nombre"])
    print ("Precio de compra:", ruta["compra"])
    print ("Precio de venta:", ruta["venta"])
    print ("Resultado neto:", round(ruta["resultado"],2))

    porcentaje = (ruta["resultado"] / pesos_iniciales) * 100
    print ("Rendimiento:", round(porcentaje,2), "%")
    print ("-----------------------------")

    print ("----- SIMULACION CON TU CAPITAL -----")
    capital_usuario = float(input("Ingresa el capital inicial:"))
    print ("Capital ingresado:", round(capital_usuario,2))
    for ruta in rutas:
        resultado_usuario = calcular_arbitraje(
            ruta["compra"],
            ruta["venta"],
            capital_usuario
        )
        porcentaje_usuario = (resultado_usuario / capital_usuario) * 100
        print ("Ruta:", ruta["nombre"])
        print ("Resultado:", round(resultado_usuario,2))
        print ("Rendimiento:", round(porcentaje_usuario,2), "%")
        print ("-----------------------------")

print ("-----MEJOR RUTA PARA TU CAPITAL-----")       
mejor_ruta_usuario = None
mejor_resultado_usuario = 0
for ruta in rutas:
    resultado_usuario = calcular_arbitraje(
        ruta["compra"],
        ruta["venta"],
        capital_usuario
    ) 
    if resultado_usuario > mejor_resultado_usuario:
        mejor_resultado_usuario = resultado_usuario
        mejor_ruta_usuario = ruta 
if mejor_ruta_usuario is None:
    print ("No hay ruta rentable")
else:
    porcentaje_mejor_usuario =(
        mejor_resultado_usuario / capital_usuario
    ) * 100
    print ("Ruta:", mejor_ruta_usuario["nombre"])
    print ("Ganancia:", round(mejor_resultado_usuario,2))
    print ("Rendimiento:", round(porcentaje_mejor_usuario,2), "%")

    capital_final = capital_usuario + mejor_resultado_usuario
    print ("Capital inicial:", round(capital_usuario,2))
    print ("Ganancia neta:", round(mejor_resultado_usuario,2))
    print ("Capital final:", round(capital_final,2))

    print ("----- FIN DEL ANALISIS -----") 
    print ("----- Guardando Resultados-----")
    fecha_hora = datetime.now(). strftime("%Y-%m-%d- %H:%M:%S")
    archivo_existe = os.path.exists("resultado_arbitraje.csv")
    with open("resultados_arbitraje.csv", "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)

        if not archivo_existe:
           escritor.writerow([
            "Fecha y hora",
            "Ruta",
            "Precio compra",
            "Precio venta",
            "Diferencia",
            "Diferencia porcentual",
            "Resultado",
            "Rendimiento",
            "Capital inicial",
            "Ganancia",
            "Capital final"
        ])
        for ruta in rutas:
            diferencia = ruta["venta"] - ruta["compra"]

            diferencia_porcentual = (
                diferencia / ruta["compra"]
            ) * 100

            resultado = calcular_arbitraje(
                ruta["compra"],
                ruta["venta"],
                capital_usuario
            )

            rendimiento = (
                resultado / capital_usuario
            ) * 100

            escritor.writerow([
                fecha_hora,
                ruta["nombre"],
                ruta["compra"],
                ruta["venta"],
                round(diferencia, 2),
                round(diferencia_porcentual, 2),
                round(resultado, 2),
                round(rendimiento, 2),
                capital_usuario,
                round(resultado, 2),
                round(capital_usuario + resultado, 2)
            ])
    print ("Resultados guardados en resultados_arbitraje.csv")     




    

    