"""Excepciones personalizadas del sistema Software FJ."""

class ErrorSistema(Exception):
    """Clase base para errores controlados de la aplicación."""

class DatosInvalidosError(ErrorSistema):
    """Se presenta cuando los datos suministrados no cumplen las reglas."""

class ServicioNoDisponibleError(ErrorSistema):
    """Se presenta cuando un servicio no está disponible."""

class ReservaInvalidaError(ErrorSistema):
    """Se presenta cuando una reserva no puede crearse o procesarse."""

class OperacionNoPermitidaError(ErrorSistema):
    """Se presenta cuando una operación contradice el estado del objeto."""
