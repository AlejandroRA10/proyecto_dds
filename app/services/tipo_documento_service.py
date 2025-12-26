from app.models.tipo_documento import TipoDocumento
from app.repositories.tipo_documento_repositorio import TipoDocumentoRepository

class TipoDocumentoService:
    @staticmethod
    def crear_tipo_documento(tipo_documento: TipoDocumento):
        return TipoDocumentoRepository.crear(tipo_documento)

    @staticmethod
    def buscar_por_id(id: int) -> TipoDocumento:
        return TipoDocumentoRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[TipoDocumento]:
        return TipoDocumentoRepository.buscar_todos()

    @staticmethod
    def actualizar_tipo_documento(id: int, tipo_documento: TipoDocumento) -> TipoDocumento:
        tipo_documento_existente = TipoDocumentoRepository.buscar_por_id(id)
        if not tipo_documento_existente:
            return None
        tipo_documento_existente.nombre = tipo_documento.nombre
        return tipo_documento_existente

    @staticmethod
    def borrar_por_id(id: int) -> TipoDocumento:
        return TipoDocumentoRepository.borrar_por_id(id)