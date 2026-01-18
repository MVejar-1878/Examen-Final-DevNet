vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= vlan <= 1005:
    print("La VLAN corresponde a un rango NORMAL (1–1005).")
elif 1006 <= vlan <= 4094:
    print("La VLAN corresponde a un rango EXTENDIDO (1006–4094).")
else:
    print("El número ingresado NO corresponde a una VLAN válida.")
    