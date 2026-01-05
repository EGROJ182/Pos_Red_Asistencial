def formatear(celda):
    while True:
        try:
            celda = float(celda.replace(".", "").replace(",", "."))
            print(f"Número formateado: {celda}")
            break
        except ValueError:
            celda = input("Ingrese un número válido: ")

while True:
    try:
        options = int(input("Ingrese una opción:\n1. Formatear número\n2. Salir\n"))
        match options:
            case 1:
                celda = input("Ingrese un número: ")
                formatear(celda)
            case 2:
                print("Saliendo del programa...")
                break
            case _:
                print("Opción no válida. Intente nuevamente.")
    except ValueError:
        print("Por favor, ingrese un número válido.")