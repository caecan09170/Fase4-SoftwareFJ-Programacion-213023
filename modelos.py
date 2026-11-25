"""Modelos orientados a objetos del sistema Software FJ."""
from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import (
    DatosInvalidosError, ServicioNoDisponibleError,
    ReservaInvalidaError, OperacionNoPermitidaError
)

class Entidad(ABC):
    """Abstracción de una entidad identificable del sistema."""
    def __init__(self, identificador):
        if not identificador or not str(identificador).strip():
            raise DatosInvalidosError("El identificador es obligatorio.")
        self._id = str(identificador).strip()

    @property
    def id(self):
        return self._id

    @abstractmethod
    def describir(self):
        """Cada entidad concreta debe describirse."""


class Cliente(Entidad):
    """Cliente con datos encapsulados y validaciones básicas."""
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self.__nombre = self._validar_texto(nombre, "nombre")
        self.__correo = self._validar_correo(correo)
        self.__telefono = self._validar_telefono(telefono)

    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise DatosInvalidosError(f"El {campo} debe tener al menos 2 caracteres.")
        return valor.strip()

    @staticmethod
    def _validar_correo(correo):
        if not isinstance(correo, str) or "@" not in correo or "." not in correo.split("@")[-1]:
            raise DatosInvalidosError("El correo electrónico no tiene un formato válido.")
        return correo.strip().lower()

    @staticmethod
    def _validar_telefono(telefono):
        digitos = "".join(c for c in str(telefono) if c.isdigit())
        if len(digitos) < 7:
            raise DatosInvalidosError("El teléfono debe contener al menos 7 dígitos.")
        return digitos

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def describir(self):
        return f"Cliente {self.id}: {self.nombre} ({self.correo})"


class Servicio(Entidad, ABC):
    """Clase abstracta que define el comportamiento común de los servicios."""
    def __init__(self, identificador, nombre, tarifa_hora, disponible=True):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise DatosInvalidosError("La tarifa por hora debe ser mayor que cero.")
        self.nombre = nombre.strip()
        self.tarifa_hora = float(tarifa_hora)
        self.disponible = bool(disponible)

    def validar(self, duracion):
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duración debe ser un número mayor que cero.")

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0):
        """Variante flexible: duración obligatoria, impuesto y descuento opcionales."""
        self.validar(duracion)
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise DatosInvalidosError("Impuesto y descuento deben estar entre 0 y 1.")
        subtotal = self.tarifa_hora * duracion
        return round(subtotal * (1 + impuesto) * (1 - descuento), 2)

    @abstractmethod
    def describir(self):
        pass


class ReservaSala(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser un entero positivo.")
        self.capacidad = capacidad

    def validar(self, duracion, personas=1):
        super().validar(duracion)
        if not isinstance(personas, int) or personas <= 0 or personas > self.capacidad:
            raise DatosInvalidosError("La cantidad de personas supera la capacidad o no es válida.")

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0):
        self.validar(duracion)
        return super().calcular_costo(duracion, impuesto, descuento)

    def describir(self):
        return f"Sala: {self.nombre}; capacidad: {self.capacidad}; tarifa/hora: ${self.tarifa_hora:.2f}"


class AlquilerEquipo(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, unidades, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(unidades, int) or unidades <= 0:
            raise DatosInvalidosError("Las unidades disponibles deben ser un entero positivo.")
        self.unidades = unidades

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0):
        self.validar(duracion)
        return super().calcular_costo(duracion, impuesto, descuento)

    def describir(self):
        return f"Equipo: {self.nombre}; unidades: {self.unidades}; tarifa/hora: ${self.tarifa_hora:.2f}"


class Asesoria(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidosError("La especialidad de la asesoría es obligatoria.")
        self.especialidad = especialidad.strip()

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0):
        self.validar(duracion)
        return super().calcular_costo(duracion, impuesto, descuento)

    def describir(self):
        return f"Asesoría: {self.nombre}; especialidad: {self.especialidad}; tarifa/hora: ${self.tarifa_hora:.2f}"


class Reserva(Entidad):
    """Reserva que relaciona cliente, servicio, duración y estado."""
    def __init__(self, identificador, cliente, servicio, duracion, personas=1):
        super().__init__(identificador)
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un servicio válido.")
        try:
            if isinstance(servicio, ReservaSala):
                servicio.validar(duracion, personas)
            else:
                servicio.validar(duracion)
        except Exception as error:
            raise ReservaInvalidaError("No fue posible validar los datos de la reserva.") from error

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = float(duracion)
        self.estado = "Pendiente"
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def confirmar(self):
        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")
        self.estado = "Confirmada"
        return f"Reserva {self.id} confirmada."

    def cancelar(self):
        if self.estado == "Cancelada":
            raise OperacionNoPermitidaError("La reserva ya está cancelada.")
        self.estado = "Cancelada"
        return f"Reserva {self.id} cancelada."

    def procesar(self, impuesto=0.19, descuento=0.0):
        if self.estado != "Confirmada":
            raise OperacionNoPermitidaError("Debe confirmar la reserva antes de procesarla.")
        return self.servicio.calcular_costo(self.duracion, impuesto, descuento)

    def describir(self):
        return (f"Reserva {self.id} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Duración: {self.duracion} h | "
                f"Estado: {self.estado}")
