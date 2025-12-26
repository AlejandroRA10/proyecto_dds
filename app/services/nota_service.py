from app.repositories.nota_repositorio import NotaRepository
from app.models.nota import Nota
from app import db

class NotaService:
    @staticmethod
    def buscar_todos():
        return NotaRepository.buscar_todos()

    @staticmethod
    def buscar_filtrado_paginado(filters: dict = None, page: int = 1, per_page: int = 20):
        return NotaRepository.buscar_filtrado_paginado(filters or {}, page, per_page)

    @staticmethod
    def buscar_por_id(id: int):
        return NotaRepository.buscar_por_id(id)

    @staticmethod
    def crear(data):
        nueva_nota = Nota(**data)
        db.session.add(nueva_nota)
        db.session.commit()
        return nueva_nota

    @staticmethod
    def actualizar(id: int, data):
        nota = NotaRepository.buscar_por_id(id)
        if not nota:
            return None
        for key, value in data.items():
            setattr(nota, key, value)
        db.session.commit()
        return nota

    @staticmethod
    def borrar_por_id(id: int):
        nota = NotaRepository.buscar_por_id(id)
        if not nota:
            return None
        db.session.delete(nota)
        db.session.commit()
        return nota
