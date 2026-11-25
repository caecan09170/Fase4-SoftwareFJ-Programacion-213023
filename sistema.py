"""Administración en memoria y registro de eventos."""
import logging
from excepciones import DatosInvalidosError

logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

class SistemaSoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        if any(c.id == cliente.id for c in self.clientes):
            raise DatosInvalidosError(f"Ya existe el cliente con ID {cliente.id}.")
        self.clientes.append(cliente)
        logging.info("Cliente registrado: %s", cliente.id)
        return cliente

    def registrar_servicio(self, servicio):
        if any(s.id == servicio.id for s in self.servicios):
            raise DatosInvalidosError(f"Ya existe el servicio con ID {servicio.id}.")
        self.servicios.append(servicio)
        logging.info("Servicio registrado: %s", servicio.id)
        return servicio

    def crear_reserva(self, reserva):
        if any(r.id == reserva.id for r in self.reservas):
            raise DatosInvalidosError(f"Ya existe la reserva con ID {reserva.id}.")
        self.reservas.append(reserva)
        logging.info("Reserva creada: %s", reserva.id)
        return reserva

    def listar_clientes(self):
        return [c.describir() for c in self.clientes]

    def listar_servicios(self):
        return [s.describir() for s in self.servicios]

    def listar_reservas(self):
        return [r.describir() for r in self.reservas]
