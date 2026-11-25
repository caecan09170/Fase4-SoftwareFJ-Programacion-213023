"""Ejecución demostrativa del sistema integral Software FJ."""
import logging
from modelos import Cliente, ReservaSala, AlquilerEquipo, Asesoria, Reserva
from sistema import SistemaSoftwareFJ
from excepciones import ErrorSistema, DatosInvalidosError, ServicioNoDisponibleError

def ejecutar_prueba(numero, descripcion, accion):
    """Ejecuta cada caso de forma independiente para que un error no detenga el programa."""
    print(f"\nPRUEBA {numero}: {descripcion}")
    try:
        resultado = accion()
        if resultado is not None:
            print("Resultado:", resultado)
    except ErrorSistema as error:
        logging.exception("Error controlado en prueba %s", numero)
        print("Error controlado:", error)
    except Exception as error:
        logging.exception("Error inesperado en prueba %s", numero)
        print("Error inesperado registrado:", error)
    else:
        print("Ejecución finalizada sin excepciones.")
    finally:
        print("Fin de la prueba", numero)

def main():
    sistema = SistemaSoftwareFJ()

    # Objetos de servicios que se usarán en las pruebas.
    sala = ReservaSala("S01", "Sala de reuniones", 50000, 12)
    equipo = AlquilerEquipo("E01", "Portátil", 15000, 8)
    asesoria = Asesoria("A01", "Asesoría contable", 80000, "Contabilidad")

    cliente_1 = Cliente("C01", "Laura Gómez", "laura@email.com", "3001234567")
    cliente_2 = Cliente("C02", "Andrés Ruiz", "andres@email.com", "3107654321")

    ejecutar_prueba(1, "Registrar cliente válido", lambda: sistema.registrar_cliente(cliente_1).describir())
    ejecutar_prueba(2, "Registrar segundo cliente válido", lambda: sistema.registrar_cliente(cliente_2).describir())
    ejecutar_prueba(3, "Intentar registrar cliente con correo inválido",
                    lambda: Cliente("C03", "Pedro Díaz", "correo-invalido", "3001234567"))
    ejecutar_prueba(4, "Intentar duplicar un cliente",
                    lambda: sistema.registrar_cliente(Cliente("C01", "Otra Persona", "otra@email.com", "3001234567")))
    ejecutar_prueba(5, "Registrar sala de reuniones", lambda: sistema.registrar_servicio(sala).describir())
    ejecutar_prueba(6, "Registrar alquiler de equipos", lambda: sistema.registrar_servicio(equipo).describir())
    ejecutar_prueba(7, "Registrar asesoría especializada", lambda: sistema.registrar_servicio(asesoria).describir())
    ejecutar_prueba(8, "Intentar crear servicio con tarifa negativa",
                    lambda: ReservaSala("S02", "Sala inválida", -1000, 10))
    ejecutar_prueba(9, "Crear reserva válida de sala",
                    lambda: sistema.crear_reserva(Reserva("R01", cliente_1, sala, 2, personas=5)).describir())

    reserva_1 = sistema.reservas[0]
    ejecutar_prueba(10, "Intentar procesar reserva sin confirmar", lambda: reserva_1.procesar())
    ejecutar_prueba(11, "Confirmar reserva", lambda: reserva_1.confirmar())
    ejecutar_prueba(12, "Procesar reserva con impuesto del 19%", lambda: f"${reserva_1.procesar():,.2f}")
    ejecutar_prueba(13, "Calcular costo con descuento del 10%",
                    lambda: f"${sala.calcular_costo(2, 0.19, 0.10):,.2f}")

    servicio_suspendido = Asesoria("A02", "Asesoría temporal", 60000, "Sistemas", disponible=False)
    ejecutar_prueba(14, "Intentar reservar servicio no disponible",
                    lambda: Reserva("R02", cliente_2, servicio_suspendido, 1))
    ejecutar_prueba(15, "Crear y cancelar reserva de equipo",
                    lambda: sistema.crear_reserva(Reserva("R03", cliente_2, equipo, 3)).cancelar())
    ejecutar_prueba(16, "Intentar cancelar nuevamente la reserva cancelada",
                    lambda: sistema.reservas[-1].cancelar())
    ejecutar_prueba(17, "Listar clientes", lambda: "\n".join(sistema.listar_clientes()))
    ejecutar_prueba(18, "Listar servicios", lambda: "\n".join(sistema.listar_servicios()))
    ejecutar_prueba(19, "Listar reservas", lambda: "\n".join(sistema.listar_reservas()))

    print("\nProceso terminado. Revise el archivo logs.txt para consultar los eventos y errores.")

if __name__ == "__main__":
    main()
