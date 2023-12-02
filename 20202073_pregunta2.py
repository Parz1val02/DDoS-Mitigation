#!/usr/bin/python
#codigo: 20202073

class Alumno:
    def __init__(self, nombre, PC):
        self.nombre = nombre
        self.PC = PC
        print(f'Alumno creado con nombre {self.nombre} y PC {self.PC}')
        print('-------------------------------------------------------------------------------')
class Servicio:
    def __init__(self, nombre, protocolo, puerto):
        self.nombre = nombre
        self.protocolo = protocolo
        self.puerto = puerto
        print(f'Servicio creado con nombre {self.nombre}, protocolo {self.protocolo} y puerto {self.puerto}')
        print('-------------------------------------------------------------------------------')
class Servidor:
    def __init__(self, nombre, IP, servicios):
        self.nombre = nombre
        self.IP = IP
        self.servicios = servicios
        print(f'Servidor creado con nombre {self.nombre}, IP {self.IP}')
        print('Lista de servicios:')
        for i in self.servicios:
            print(f'Servicio con nombre {i.nombre}, protocolo {i.protocolo} y puerto {i.puerto}')

    def agregarServicio(self, servicio):
        self.servicios.append(servicio)
        print(f"{servicio.nombre} agregado a la lista de servicios")
        print("Lista de servicios actualizada:")
        for i in self.servicios:
            print(f'Servicio con nombre {i.nombre}, protocolo {i.protocolo} y puerto {i.puerto}')

class Curso:
    def __init__(self, nombre, estado, alumnos, servidores):
        self.nombre = nombre
        self.estado = estado
        self.alumnos = alumnos
        self.servidores = servidores
        print(f'Curso creado con nombre {self.nombre} y estado {self.estado}')
        print('Lista de alumnos:')
        for i in self.alumnos:
            print(f'Alumno con nombre {i.nombre} y PC {i.PC}')

    def borrarAlumno(self, alumno):
        self.alumnos.remove(alumno)
        print(f"{alumno.nombre} borrado de la lista de alumnos del curso {self.nombre}")
        print("Lista de alumnos actualizada:")
        for i in self.alumnos:
            print(f'Alumno con nombre {i.nombre} y PC {i.PC}')
    def agregarAlumno(self, alumno):
        self.alumnos.append(alumno)
        print(f"{alumno.nombre} agregado a la lista de alumnos del curso {self.nombre}")
        print("Lista de alumnos actualizada:")
        for i in self.alumnos:
            print(f'Alumno con nombre {i.nombre} y PC {i.PC}')
    def agregarServidor(self, servidor):
        self.servidores.append(servidor)
        print(f"{servidor.nombre} agregado a la lista de servidores")

if __name__ == '__main__':
    alumno1 = Alumno("Rodrigo", "02:42:ac:11:00:02")
    alumno2 = Alumno("Bruno", "00:1A:2B:3C:4D:5E")
    alumno3 = Alumno("Fernanda", "08:00:27:13:69:D6")

    servicio1 = Servicio("REST API", "HTTP", 4444)
    servicio2 = Servicio("MariaDB", "TCP", 3306)

    alumnos = [alumno1,alumno2,alumno3]
    servicios = [servicio1,servicio2]

    servicio3 = Servicio("SSH", "TCP", 22)
    servidor1 = Servidor("Hackbox", "192.168.10.10", servicios)
    servidor1.agregarServicio(servicio3)

    servidores = [servidor1]

    curso = Curso("SDN", "En curso", alumnos, servidores)
    alumno4 = Alumno("Kori", "08:00:27:13:69:D6")
    curso.agregarAlumno(alumno4)
    curso.borrarAlumno(alumno1)