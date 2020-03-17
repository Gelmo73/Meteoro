import os
import marshal
from colorama import init, Fore
import webbrowser

init()

upath = os.environ['USERPROFILE'] + '/Desktop/'
spath = 'C:/Metheor'
meteoritos = []


if not os.path.exists(spath):
    os.mkdir(spath)

if os.path.exists(spath + '/storage.bin'):
    with open(spath + '/storage.bin', 'rb') as f:
        meteoritos = marshal.load(f)


def limpiar():
    os.system('cls')


def mostrar():

    for registro in meteoritos:
        print(
            Fore.RED, 'Regitro: ', meteoritos.index(registro) + 1,
            Fore.WHITE, '\nNombre: ', registro['Nombre'],
            '\nTipo: ', registro['Tipo'],
            '\nPais: ', registro['Pais'],
            '\nLongitud: ', registro['Lon'],
            '\nLatitud: ', registro['Lat']
        )
        print()


def mostrarRegistro(registro):
    limpiar()
    print(
        'Nombre: ', registro['Nombre'],
        '\nTipo: ', registro['Tipo'],
        '\nPais: ', registro['Pais'],
        '\nLongitud: ', registro['Lon'],
        '\nLatitud: ', registro['Lat']
    )
    print()


def agregar():
    limpiar()

    print('Agregando...')
    try:
        temp = {
            'Nombre': input('Nombre: '),
            'Fecha': input('Fecha: '),
            'Tipo': input('Tipo: '),
            'Pais': input('Pais: '),
            'Lon': int(input('Longitud: ')),
            'Lat': int(input('Latitud: '))
        }
    except ValueError:
        print('Por favor, colocar numeros en Longitud y Latitud')
        return

    meteoritos.append(temp)
    print('Registro agregado')


def agregarExistente(registro):
    limpiar()

    try:
        temp = {
            'Nombre': input('Nombre: '),
            'Fecha': input('Fecha: '),
            'Tipo': input('Tipo: '),
            'Pais': input('Pais: '),
            'Lon': int(input('Longitud: ')),
            'Lat': int(input('Latitud: '))
        }
    except ValueError:
        print('Por favor, colocar numeros en Longitud y Latitud')
        return 0

    return temp


def modificar():

    if len(meteoritos) == 0:
        print('Sin registros...')
        return
    limpiar()
    mostrar()

    try:
        op = int(input('Elija el registro a modificar: ')) - 1
    except ValueError:
        print('Opcion no valida...')
        return

    if 0 <= op < len(meteoritos):
        mostrarRegistro(meteoritos[op])
    else:
        print('Fuera de los limites...')
        return

    des = True

    while des:
        opt = input('''
[ U ] Modificar un unico campo 
[ T ] Modificar todo el  registro 
[ C ] Cancelar Modificacion
''').upper().strip()

        print()  # Espaciado

        if opt == 'U':

            des2 = True
            while des2:
                l = input(
                    'Escriba el campo que desee modificar: ').capitalize().strip()

                if not l in meteoritos[op]:
                    print('Registro no existente')
                    input()
                else:
                    meteoritos[op][l] = input(l + ': ')
                    des2 = False

            des = False

        elif opt == 'T':
            result = agregarExistente(meteoritos[op])
            if not result == 0:
                meteoritos[op] = result
                des = False
        elif opt == 'C':
            print('Modificacion cancelada...')
        else:
            print('Opcion no valida')
            input()
            limpiar()
            mostrarRegistro(meteoritos[op])

    print('Dato modificado...')


def borrar():
    if len(meteoritos) == 0:
        print('Sin registros...')
        return
    limpiar()
    mostrar()

    try:
        op = int(input('Elija el registro a borrar: ')) - 1
    except ValueError:
        print('Opcion no valida...')
        return

    if 0 <= op < len(meteoritos):
        mostrarRegistro(meteoritos[op])
    else:
        print('Fuera de los limites...')
        return

    des = True
    while des:
        limpiar()
        mostrarRegistro(meteoritos[op])

        opt = input(
            'Seguro que desea eliminar este registro [S/N]').upper().strip()

        if opt == 'S':
            meteoritos.pop(op)
            print('Reagistro eliminado...')
            des = False
        elif opt == 'N':
            print('Eliminacion cancelada...')
            des = False
        else:
            print('Elija una opcion valida')
            input()


def guardar():
    with open(spath + '/storage.bin', 'wb') as f:
        marshal.dump(meteoritos, f)
    print('Datos guardados...')


def exportar():

    if len(meteoritos) == 0:
        print('Sin registros...')
        return

    limpiar()

    with open('mapa.html', 'r') as f:
        html = f.read()

    markers = []
    for registro in meteoritos:
        tmp = '''
L.marker(['''+str(registro['Lat'])+''', '''+str(registro['Lon'])+'''])
        .addTo(map)
        .bindPopup("'''+registro['Nombre']+'''")
        .openPopup();    
        '''
        markers.append(tmp)

    html = html.replace('//MARCADORES', '\n'.join(markers))

    nombre = input('Pongale un nombre: ')
    file = upath + nombre + '.html'

    if os.path.exists(file):
        print('Este archivo ya existe...')
        return

    with open(file, 'w') as f:
        f.write(html)
        print(nombre, 'ahora se encuentra en el escritorio')

    if input('Escriba [A] si desea visualizar su mapa inmediatamente: ').upper().strip() == 'A':
        webbrowser.open(file)


def menu():
    limpiar()
    print('''
1- Agregar
2- Modificar
3- Borrar
4- Guardar
5- Exportar
6- Salir
    ''')

    op = input('Elija una opcion: ')

    if op == '1':
        agregar()
        input()
        menu()
    elif op == '2':
        modificar()
        input()
        menu()
    elif op == '3':
        borrar()
        input()
        menu()
    elif op == '4':
        guardar()
        input()
        menu()
    elif op == '5':
        exportar()
        input()
        menu()
    elif op == '6':
        pass
    else:
        print('Debe seleccionar una opcion...')
        input()
        menu()


menu()
