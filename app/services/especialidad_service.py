from app.models.especialidad import Especialidad
from app.repositories.especialidad_repositorio import EspecialidadRepository

class EspecialidadService:
    @staticmethod
    def crear_especialidad(especialidad: Especialidad):
        return EspecialidadRepository.crear(especialidad)

    @staticmethod
    def buscar_por_id(id: int) -> Especialidad:
        return EspecialidadRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Especialidad]:
        return EspecialidadRepository.buscar_todos()

    @staticmethod
    def actualizar_especialidad(id: int, especialidad: Especialidad) -> Especialidad:
        especialidad_existente = EspecialidadRepository.buscar_por_id(id)
        if not especialidad_existente:
            return None
        especialidad_existente.nombre = especialidad.nombre
        especialidad_existente.letra = especialidad.letra
        especialidad_existente.observacion = especialidad.observacion
        especialidad_existente.tipo_especialidad_id = especialidad.tipo_especialidad_id
        return especialidad_existente

    @staticmethod
    def borrar_por_id(id: int) -> Especialidad:
        return EspecialidadRepository.borrar_por_id(id)