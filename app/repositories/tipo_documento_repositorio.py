from app import db
from app.models.tipo_documento import TipoDocumento


class TipoDocumentoRepository:
    @staticmethod
    def crear(tipo_documento: TipoDocumento) -> TipoDocumento:
        db.session.add(tipo_documento)
        db.session.commit()
        return tipo_documento

    @staticmethod
    def buscar_por_id(id: int) -> TipoDocumento:
        return db.session.query(TipoDocumento).filter_by(id=id).first()

    @staticmethod
    def buscar_todos() -> list[TipoDocumento]:
        return db.session.query(TipoDocumento).all()

    @staticmethod
    def actualizar(tipo_documento: TipoDocumento) -> TipoDocumento:
        tipo_documento_existente = db.session.merge(tipo_documento)
        db.session.commit()
        return tipo_documento_existente

    @staticmethod
    def borrar_por_id(id: int) -> TipoDocumento:
        tipo_documento = db.session.query(
            TipoDocumento).filter_by(id=id).first()
        if not tipo_documento:
            return None
        db.session.delete(tipo_documento)
        db.session.commit()
        return tipo_documento
