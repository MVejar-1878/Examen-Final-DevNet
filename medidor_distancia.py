#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Consumo de API Pública GraphHopper
- Mide distancia entre ciudades de Chile y Argentina
- Solicita Ciudad de Origen y Destino
- Muestra distancia en km y millas, duración del viaje
- Muestra narrativa paso a paso
- Permite elegir medio de transporte
- Permite salir con la letra 'v'
"""

import os
import sys
import requests

GRAPHOPPER_BASE = "https://graphhopper.com/api/1"
API_KEY = "e12507cf-aafc-4664-88af-1335124587c3"

session = requests.Session()

def ms_a_horas_min(ms):
    s = ms // 1000
    h = s // 3600
    m = (s % 3600) // 60
    return f"{h:02d}:{m:02d}"

def metros_a_km_mi(m):
    km = m / 1000
    mi = km * 0.621371
    return km, mi

def geocodificar(ciudad):
    url = f"{GRAPHOPPER_BASE}/geocode"
    params = {
        "q": ciudad,
        "limit": 1,
        "locale": "es",
        "key": API_KEY
    }
    r = session.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    if not data.get("hits"):
        return None
    p = data["hits"][0]["point"]
    return p["lat"], p["lng"]

def calcular_ruta(origen, destino, medio):
    url = f"{GRAPHOPPER_BASE}/route"
    params = {
        "point": [f"{origen[0]},{origen[1]}", f"{destino[0]},{destino[1]}"],
        "profile": medio,
        "locale": "es",
        "instructions": "true",
        "points_encoded": "false",
        "key": API_KEY
    }
    r = session.get(url, params=params, timeout=30)
    r.raise_for_status()
    path = r.json()["paths"][0]
    return path

def elegir_medio():
    print("Medios disponibles: car, bike, foot")
    medio = input("Seleccione medio de transporte o 'v' para salir: ").lower()
    if medio == "v":
        return None
    if medio not in ["car", "bike", "foot"]:
        print("Medio no válido, se usará 'car'")
        return "car"
    return medio

def main():
    print("=== Medición de distancia entre ciudades ===")
    print("Ingrese 'v' para salir\n")

    origen_txt = input("Ciudad de Origen: ")
    if origen_txt.lower() == "v":
        return

    destino_txt = input("Ciudad de Destino: ")
    if destino_txt.lower() == "v":
        return

    medio = elegir_medio()
    if medio is None:
        return

    origen = geocodificar(origen_txt)
    destino = geocodificar(destino_txt)

    if not origen or not destino:
        print("No se pudieron obtener coordenadas.")
        return

    ruta = calcular_ruta(origen, destino, medio)

    km, mi = metros_a_km_mi(ruta["distance"])
    duracion = ms_a_horas_min(ruta["time"])

    print("\n=== Resultado ===")
    print(f"Origen: {origen_txt}")
    print(f"Destino: {destino_txt}")
    print(f"Medio: {medio}")
    print(f"Distancia: {km:.2f} km / {mi:.2f} millas")
    print(f"Duración estimada: {duracion}")

    print("\n--- Narrativa del viaje ---")
    for i, inst in enumerate(ruta["instructions"], 1):
        d_km, d_mi = metros_a_km_mi(inst["distance"])
        print(f"{i}. {inst['text']} ({d_km:.2f} km / {d_mi:.2f} mi)")

if __name__ == "__main__":
    main()