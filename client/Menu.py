def menuLogin():
    while True:
        menuLoginPrint()
        # to do implementar funciones para cada opcion.
        print("Ingrese una opcion a continuación: ")
        opcion = input()
        try:
            opcion = int(opcion)
            if opcion > 0 and opcion < 5:
                print('\033c')
                return opcion
        except:
            pass
        print("Opcion invalida\n")


def menuLoginPrint():
    print("----Menu de Login----")
    print("1 - Ingresar")
    print("2 - Registrarse ")
    print("3 - Reestablecer contraseña")
    print("4 - Salir")


def menu():
    while True:
        menuPrint()
        # to do implementar funciones para cada opcion
        print("Ingrese una opcion a continuación: ")
        opcion = input()
        try:
            opcion = int(opcion)
            if opcion > 0 and opcion < 8:
                print('\033c')
                return opcion
        except:
            pass
        print("Opcion invalida\n")


def menuPrint():
    print("----Menu de aplicación----")
    print("1 - Subir un nuevo archivo ")
    print("2 - Compartir un archivo propio con un tercero")
    print("3 - Descargar archivo propio")
    print("4 - Descargar archivo de un tercero")
    print("5 - Cambiar mi contraseña")
    print("6 - Salir")
