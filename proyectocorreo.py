from typing import List, Protocol
from datetime import datetime


# ------------------------
# Interfaces
# ------------------------
class PuedeEnviar(Protocol):
    def enviar(self, mensaje: "Mensaje", destinatario: "Usuario") -> None: ...


class PuedeRecibir(Protocol):
    def recibir(self, mensaje: "Mensaje") -> None: ...


class PuedeListar(Protocol):
    def listar(self) -> List[str]: ...


# ------------------------
# Clase Mensaje
# ------------------------
class Mensaje:
    def __init__(self, remitente: str, destinatario: str, asunto: str, cuerpo: str):
        self._remitente = remitente
        self._destinatario = destinatario
        self._asunto = asunto
        self._cuerpo = cuerpo
        self._fecha = datetime.now()

    @property
    def remitente(self): return self._remitente

    @property
    def destinatario(self): return self._destinatario

    @property
    def asunto(self): return self._asunto

    @property
    def cuerpo(self): return self._cuerpo

    @property
    def fecha(self): return self._fecha

    def __str__(self):
        return f"{self.fecha:%Y-%m-%d %H:%M} | {self.remitente} → {self.destinatario}: {self.asunto}"


# ------------------------
# Clase Carpeta
# ------------------------
class Carpeta(PuedeListar):
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._mensajes: List[Mensaje] = []

    @property
    def nombre(self): return self._nombre

    def agregar(self, mensaje: Mensaje) -> None:
        self._mensajes.append(mensaje)

    def listar(self) -> List[str]:
        return [str(m) for m in self._mensajes]


# ------------------------
# Clase Usuario
# ------------------------
class Usuario(PuedeEnviar, PuedeRecibir):
    def __init__(self, nombre: str, correo: str):
        self._nombre = nombre
        self._correo = correo
        self._carpetas = {
            "entrada": Carpeta("Bandeja de Entrada"),
            "salida": Carpeta("Enviados")
        }

    @property
    def nombre(self): return self._nombre

    @property
    def correo(self): return self._correo

    def enviar(self, mensaje: Mensaje, destinatario: "Usuario") -> None:
        self._carpetas["salida"].agregar(mensaje)
        destinatario.recibir(mensaje)

    def recibir(self, mensaje: Mensaje) -> None:
        self._carpetas["entrada"].agregar(mensaje)

    def ver_carpetas(self) -> List[str]:
        return list(self._carpetas.keys())

    def listar(self, carpeta: str) -> List[str]:
        if carpeta in self._carpetas:
            return self._carpetas[carpeta].listar()
        return []


# ------------------------
# Clase ServidorCorreo
# ------------------------
class ServidorCorreo:
    def __init__(self):
        self._usuarios: List[Usuario] = []

    def registrar(self, usuario: Usuario) -> None:
        self._usuarios.append(usuario)

    def buscar(self, correo: str) -> Usuario | None:
        return next((u for u in self._usuarios if u.correo == correo), None)
if __name__ == "__main__":
        # 1. Crear servidor
    servidor = ServidorCorreo()
    # 2. Crear usuarios
    Federico = Usuario("Federico", "federodriguez@mail.com")
    Francisco = Usuario("Francisco", "franflores@mail.com")

    # 3. Registrar usuarios en el servidor
    servidor.registrar(Federico)
    servidor.registrar(Francisco)

    # 4. Crear mensaje de Alice para Bob
    mensaje1 = Mensaje("federodriguez@mail.com","franflores@mail.com", "¡Hola Fran!","¿Todo bien?")

    # 5. Alice envía el mensaje a Bob
    Federico.enviar(mensaje1, Francisco)

    # 6. Revisar mensajes de cada uno
    print("📨 Enviados de Federico:")
    print(Federico.listar("salida"))

    print("\n📥 Entrada de Francisco:")
    print(Francisco.listar("entrada"))


    


    
    

    



    

    

    





   