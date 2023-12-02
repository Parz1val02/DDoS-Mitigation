import yaml
import requests
from prettytable import PrettyTable

database=""

class Alumno:
    def __init__(self, nombre, codigo, mac):
        self.nombre = nombre
        self.codigo = codigo
        self.mac = mac
class Curso:
    def __init__(self, nombre, codigo, estado):
        self.nombre = nombre
        self.codigo = codigo
        self.estado = estado
        self.alumnos = []
        self.servidores = []
    def agregar_alumno(self, alumno):
        if alumno not in self.alumnos:
            self.alumnos.append(alumno)
    def remover_alumno(self, alumno):
        if alumno in self.alumnos:
            self.alumnos.remove(alumno)
    def agregar_servidor(self, servidor):
        if servidor not in self.servidores:
            self.servidores.append(servidor)
class Servidor:
    def __init__(self, nombre, ip):
        self.nombre = nombre
        self.ip = ip
        self.servicios = []
    def agregar_servicio(self, servicio):
        if servicio not in self.servicios:
            self.servicios.append(servicio)
class Servicio:
    def __init__(self, nombre, protocolo, puerto):
        self.nombre = nombre
        self.protocolo = protocolo
        self.puerto = puerto

def get_attachment_points(mac,data):
    for row in data:
        if mac in row.get('mac', []):
            a_p = row.get('attachmentPoint',[])[0]
            s_dpid = a_p.get('switchDPID')
            port = a_p.get('port')
            break
    return s_dpid, port

def get_route(dpid_origen, port_origen, dpid_destino, port_destino):
    route_api = f'wm/topology/route/{dpid_origen}/{port_origen}/{dpid_destino}/{port_destino}/json'
    url = f'http://{controller_ip}:8080/{route_api}' 
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        print('SUCCESSFUL REQUEST | STATUS: 200')
        data = response.json()
        return data
    else:
        print(f'FAILED REQUEST | STATUS: {response.status_code}')
        return None

def menu():
    print("######################################")
    print("Network Policy manager de la UPSM")
    print("######################################")
    print("Seleccione una opción")
    print("1) Importar")
    print("2) Exportar")
    print("3) Cursos")
    print("4) Alumnos")
    print("5) Servidores")
    print("6) Políticas")
    print("7) Conexiones")
    print("8) Salir")
    option = input("> ")
    return option

def cursos():
    global database
    if(database!=""):
        while True:
            print("######################################")
            print("Opción 3) Cursos")
            print("######################################")
            print("Seleccione una opción")
            print("1) Crear Curso")
            print("2) Listar Cursos")
            print("3) Mostrar Detalles de Curso")
            print("4) Actualizar Curso")
            print("5) Borrar Curso")
            print("6) Regresar a menú principal")
            curso_op = input("> ")
            match curso_op:
                case "1":
                    nuevo_curso = {
                    'codigo': input("Ingrese el código del nuevo curso: "),
                    'estado': input("Ingrese el estado del nuevo curso: "),
                    'nombre': input("Ingrese el nombre del nuevo curso: "),
                    'alumnos': [],
                    'servidores': []
                    }
                    database['cursos'].append(nuevo_curso)
                case "2":
                    cursos = database.get('cursos', [])
                    print("Lista de todos los cursos:")
                    tabla_cursos = PrettyTable()
                    tabla_cursos.field_names = ["Código", "Estado", "Nombre"]
                    for curso in cursos:
                        codigo = curso['codigo']
                        estado = curso['estado']
                        nombre = curso['nombre']
                        tabla_cursos.add_row([codigo, estado, nombre])
                    print(tabla_cursos)
                case "3":
                    codigo = input("Ingrese el código del curso a detallar: ")
                    for curso in database['cursos']:
                        if curso['codigo'] == codigo:
                            tabla_cursos = PrettyTable()
                            tabla_cursos.field_names = ["Nombre", "Alumnos", "Servidores"]
                            nombre = curso['nombre']
                            alumnos = curso.get('alumnos', [])  
                            servidores = curso['servidores'] 
                            tabla_cursos.add_row([nombre,alumnos,servidores])
                            print(tabla_cursos)
                            break
                    else:
                        print(f"No se encontró un curso con el código {codigo}.")
                case "4":
                    codigo = input("Ingrese el código del curso a editar: ")
                    for curso in database['cursos']:
                        if curso['codigo'] == codigo:
                            print("1) Agregar alumno")
                            print("2) Quitar alumno")
                            opcion = input("Seleccione una opción: ")
                            if opcion == '1':
                                alumnos_codigos = curso.get('alumnos', [])
                                nuevo_alumno_codigo = int(input("Ingrese el código del nuevo alumno a agregar: "))
                                if any(alumno['codigo'] == nuevo_alumno_codigo for alumno in database.get('alumnos', [])):
                                    if nuevo_alumno_codigo not in alumnos_codigos:
                                        alumnos_codigos.append(nuevo_alumno_codigo)
                                        curso['alumnos'] = alumnos_codigos
                                        print(f"El alumno {nuevo_alumno_codigo} ha sido agregado al curso {codigo}.")
                                    else:
                                        print(f"El alumno {nuevo_alumno_codigo} ya está en el curso {codigo}.")
                                else:
                                    print(f"No se encontró un alumno con el código {nuevo_alumno_codigo}.")
                            elif opcion == '2':
                                alumnos_codigos = curso.get('alumnos', [])
                                alumno_a_quitar = int(input("Ingrese el código del alumno a quitar del curso: "))
                                if alumno_a_quitar in alumnos_codigos:
                                    alumnos_codigos.remove(alumno_a_quitar)
                                    curso['alumnos'] = alumnos_codigos
                                    print(f"El alumno {alumno_a_quitar} ha sido quitado del curso {codigo}.")
                                else:
                                    print(f"El alumno {alumno_a_quitar} no está en el curso {codigo}.")
                            break
                    else:
                        print(f"No se encontró un curso con el código {codigo}.")
                case "5":
                    codigo = input("Ingrese el código del curso que desea borrar: ")
                    for curso in database['cursos']:
                        if curso['codigo'] == codigo:
                            database['cursos'].remove(curso)
                            break
                    else:
                        print(f"No se encontró un curso con el código {codigo_a_borrar}.")
                case "6":
                        break
                case _:
                    print("Opción incorrecta. Intente otra vez")
    else:
        print("Primero importar los datos")

def alumnos():
    if(database!=""):
        while True:
            print("######################################")
            print("Opción 4) Alumnos")
            print("######################################")
            print("Seleccione una opción")
            print("1) Crear Alumno")
            print("2) Listar Alumno")
            print("3) Mostrar Alumno")
            print("4) Actualizar Alumno")
            print("5) Borrar Alumno")
            print("6) Regresar a menú principal")
            alumno_op = input("> ")
            match alumno_op:
                case "1":
                    nuevo_alumno = {
                    'codigo': int(input("Ingrese el código del nuevo alumno: ")),
                    'mac': input("Ingrese la mac del nuevo alumno: "),
                    'nombre': input("Ingrese el nombre del nuevo alumno: "),
                    }
                    database['alumnos'].append(nuevo_alumno)
                case "2":
                    alumnos = database.get('alumnos', [])
                    print("Listado de todos los alumnos:")
                    tabla_alumnos = PrettyTable()
                    tabla_alumnos.field_names = ["Código"]
                    for alumno in alumnos:
                        codigo = alumno['codigo']
                        tabla_alumnos.add_row([codigo])
                    print(tabla_alumnos)
                case "3":
                    codigo = input("Ingrese el código del alumno a detallar: ")
                    for alumno in database['alumnos']:
                        if alumno['codigo'] == int(codigo):
                            tabla_alumnos = PrettyTable()
                            tabla_alumnos.field_names = ["Nombre", "Código", "MAC"]
                            nombre = alumno['nombre']
                            codigo = alumno['codigo']
                            mac = alumno['mac']
                            tabla_alumnos.add_row([nombre,codigo,mac])
                            print(tabla_alumnos)
                            break
                    else:
                        print(f"No se encontró un alumno con el código {codigo}.")
                case "4":
                    codigo_a_editar = int(input("Ingrese el código del alumno que desea editar: "))
                    alumnos = database.get('alumnos', [])
                    for alumno in alumnos:
                        if alumno['codigo'] == codigo_a_editar:
                            nuevo_nombre = input("Nuevo nombre: ")
                            nueva_mac = input("Nueva MAC: ")
                            alumno_encontrado['nombre'] = nuevo_nombre
                            alumno_encontrado['mac'] = nueva_mac
                            print(f"Información del alumno {codigo_a_editar} actualizada correctamente.")
                            break
                    else:
                        print(f"No se encontró un alumno con el código {codigo_a_editar}.")
                case "5":
                    codigo_a_borrar = int(input("Ingrese el código del alumno que desea borrar: "))
                    alumnos = database.get('alumnos', [])
                    for alumno in alumnos:
                        if alumno['codigo'] == codigo_a_borrar:
                            alumnos.remove(alumno_encontrado)
                            print(f"Alumno {codigo_a_borrar} ha sido borrado correctamente.")
                            break
                    else:
                        print(f"No se encontró un alumno con el código {codigo_a_borrar}.")
                case "6":
                    break
                case _:
                    print("Opción incorrecta. Intente otra vez")
    else:
        print("Primero importar los datos")

def servidores():
    if(database!=""):
        while True:
            print("######################################")
            print("Opción 5) Servidores y servicios")
            print("######################################")
            print("Seleccione una opción")
            print("1) Crear Servidor")
            print("2) Listar Servidores") 
            print("3) Mostrar Servicios")
            print("4) Actualizar Servidor")
            print("5) Borrar Servidor")
            print("6) Regresar a menú principal")
            ser_op = input("> ")
            match ser_op:
                case '1':
                    nuevo_servidor = {
                        'nombre': input("Ingrese el nombre del nuevo servidor: "),
                        'ip': input("Ingrese la dirección IP del nuevo servidor: "),
                        'servicios': []
                    }
                    num_servicios = int(input("Ingrese la cantidad de servicios que desea agregar: "))
                    for _ in range(num_servicios):
                        nombre_servicio = input("Ingrese el nombre del servicio: ")
                        protocolo_servicio = input("Ingrese el protocolo del servicio (por ejemplo, TCP o UDP): ")
                        puerto_servicio = int(input("Ingrese el puerto del servicio: "))
                        nuevo_servicio = {
                            'nombre': nombre_servicio,
                            'protocolo': protocolo_servicio,
                            'puerto': puerto_servicio
                        }
                        nuevo_servidor['servicios'].append(nuevo_servicio)
                        database['servidores'].append(nuevo_servidor)
                case '2':
                    servidores = database.get('servidores', [])
                    print("Listado de todos los servidores:")
                    tabla_servidores = PrettyTable()
                    tabla_servidores.field_names = ["Nombre", "IP"]
                    for servidor in servidores:
                        nombre = servidor['nombre']
                        ip = servidor['ip']
                        tabla_servidores.add_row([nombre, ip])
                        print(tabla_servidores)
                case '3':
                    nombre_servidor_buscar = input("Ingrese la IP del servidor para listar sus servicios: ")
                    servidor_encontrado = None
                    for servidor in database.get('servidores', []):
                        if servidor['ip'] == nombre_servidor_buscar:
                            servidor_encontrado = servidor
                            break
                    if servidor_encontrado:
                        print(f"Servicios del servidor {nombre_servidor_buscar}:")
                        tabla_servicios = PrettyTable()
                        tabla_servicios.field_names = ["Nombre", "Protocolo", "Puerto"]
                        for servicio in servidor_encontrado.get('servicios', []):
                            nombre = servicio['nombre']
                            protocolo = servicio['protocolo']
                            puerto = servicio['puerto']
                            tabla_servicios.add_row([nombre,protocolo,puerto])
                        print(tabla_servicios)
                    else:
                        print(f"No se encontró un servidor con el nombre {nombre_servidor_buscar}.")
                case '4':
                    servidores = database.get('servidores', [])
                    print("Listado de servidores:")
                    for idx, servidor in enumerate(servidores):
                        print(f"{idx + 1}) Nombre: {servidor['nombre']}, IP: {servidor['ip']}")
                    try:
                        seleccion = int(input("Seleccione el número de servidor que desea editar: ")) - 1
                        if 0 <= seleccion < len(servidores):
                            servidor_editar = servidores[seleccion]
                            print(f"Editando el servidor: {servidor_editar['nombre']} - {servidor_editar['ip']}")
                            nuevo_nombre = input("Ingrese el nuevo nombre del servidor (deje en blanco para mantener el actual): ")
                            nuevo_ip = input("Ingrese la nueva IP del servidor (deje en blanco para mantener la actual): ")
                            if nuevo_nombre:
                                servidor_editar['nombre'] = nuevo_nombre
                            if nuevo_ip:
                                servidor_editar['ip'] = nuevo_ip
                            servicios = servidor_editar.get('servicios', [])
                            while True:
                                print("\nServicios actuales del servidor:")
                                for idx, servicio in enumerate(servicios):
                                    print(f"{idx + 1}) Nombre: {servicio['nombre']}, Protocolo: {servicio['protocolo']}, Puerto: {servicio['puerto']}")
                                opcion_servicio = input("Seleccione una opción:\n1) Agregar servicio\n2) Quitar servicio\n3) Terminar edición\n>>>")
                                if opcion_servicio == '1':
                                    nombre_servicio = input("Ingrese el nombre del nuevo servicio: ")
                                    protocolo = input("Ingrese el protocolo del servicio: ")
                                    puerto = int(input("Ingrese el puerto del servicio: "))
                                    nuevo_servicio = {
                                        'nombre': nombre_servicio,
                                        'protocolo': protocolo,
                                        'puerto': puerto
                                    }
                                    servicios.append(nuevo_servicio)
                                elif opcion_servicio == '2':
                                    servicio_quitar = int(input("Ingrese el número del servicio que desea quitar: ")) - 1
                                    if 0 <= servicio_quitar < len(servicios):
                                        servicio_quitar_nombre = servicios[servicio_quitar]['nombre']
                                        del servicios[servicio_quitar]
                                        print(f"Se ha quitado el servicio: {servicio_quitar_nombre}")
                                    else:
                                        print("Número de servicio no válido.")
                                elif opcion_servicio == '3':
                                    break
                            servidor_editar['servicios'] = servicios
                            print("Edición del servidor y servicios completada.")
                        else:
                            print("Número de servidor no válido.")
                    except ValueError:
                        print("Por favor, ingrese un número válido.")
                case '5':
                    servidores = database.get('servidores', [])
                    print("Listado de servidores:")
                    for idx, servidor in enumerate(servidores):
                        print(f"{idx + 1}) Nombre: {servidor['nombre']}, IP: {servidor['ip']}")
                    try:
                        seleccion = int(input("Seleccione el número de servidor que desea editar: ")) - 1
                        if 0 <= seleccion < len(servidores):
                            servidor_editar = servidores[seleccion]
                            print(f"Editando el servidor: {servidor_editar['nombre']} - {servidor_editar['ip']}")
                            nuevo_nombre = input("Ingrese el nuevo nombre del servidor (deje en blanco para mantener el actual): ")
                            nuevo_ip = input("Ingrese la nueva IP del servidor (deje en blanco para mantener la actual): ")
                            if nuevo_nombre:
                                servidor_editar['nombre'] = nuevo_nombre
                            if nuevo_ip:
                                servidor_editar['ip'] = nuevo_ip
                            servicios = servidor_editar.get('servicios', [])
                            while True:
                                print("\nServicios actuales del servidor:")
                                for idx, servicio in enumerate(servicios):
                                    print(f"{idx + 1}) Nombre: {servicio['nombre']}, Protocolo: {servicio['protocolo']}, Puerto: {servicio['puerto']}")
                                opcion_servicio = input("Seleccione una opción:\n1) Agregar servicio\n2) Quitar servicio\n3) Terminar edición\n")
                                if opcion_servicio == '1':
                                    nombre_servicio = input("Ingrese el nombre del nuevo servicio: ")
                                    protocolo = input("Ingrese el protocolo del servicio: ")
                                    puerto = input("Ingrese el puerto del servicio: ")
                                    nuevo_servicio = {
                                        'nombre': nombre_servicio,
                                        'protocolo': protocolo,
                                        'puerto': puerto
                                    }
                                    servicios.append(nuevo_servicio)
                                elif opcion_servicio == '2':
                                    servicio_quitar = int(input("Ingrese el número del servicio que desea quitar: ")) - 1
                                    if 0 <= servicio_quitar < len(servicios):
                                        servicio_quitar_nombre = servicios[servicio_quitar]['nombre']
                                        del servicios[servicio_quitar]
                                        print(f"Se ha quitado el servicio: {servicio_quitar_nombre}")
                                    else:
                                        print("Número de servicio no válido.")
                                elif opcion_servicio == '3':
                                    break
                            servidor_editar['servicios'] = servicios
                            print("Edición del servidor y servicios completada.")
                        else:
                            print("Número de servidor no válido.")
                    except ValueError:
                        print("Por favor, ingrese un número válido.")
                case '6':
                    break
                case _:
                    print("Opción incorrecta. Intente otra vez")
    else:
        print("Primero se deben importar los datos")


if __name__ == '__main__':
    while True:
        option = menu()
        match option:
            case "1":
                with open('database.yaml', 'r') as file:
                    database = yaml.safe_load(file)
                    print("Database importada correctamente")
            case "2":
                with open('database.yaml', 'w') as file:
                    yaml.dump(database, file)
                    print("Database exportada correctamente")
            case "3":
                cursos()
            case "4":
                alumnos()
            case "5":
                servidores()
            case "6":
                break
            case "7":
                break
            case "8":
                print("Hasta luego")
                break
            case _:
                print("Opción incorrecta. Intente otra vez")