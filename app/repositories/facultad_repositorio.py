from app import db
from app.models import Facultad
from sqlalchemy import or_
from app.utils.pagination import apply_pagination


class FacultadRepository:
    @staticmethod
    def crear(facultad):
        db.session.add(facultad)
        db.session.commit()
        return facultad

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Facultad).filter_by(id=id).first()

    @staticmethod
    def buscar_todos():
        return db.session.query(Facultad).all()

    @staticmethod
    def buscar_filtrados(page: int = 1, per_page: int = 10, q: str = None):
        """Devuelve una tupla (items, total) aplicando filtro por nombre, abreviatura o sigla y paginación."""
        query = db.session.query(Facultad)
        if q:
            likeq = f"%{q}%"
            query = query.filter(
                or_(
                    Facultad.nombre.ilike(likeq),
                    Facultad.abreviatura.ilike(likeq),
                    Facultad.sigla.ilike(likeq)
                )
            )

        # reutilizar helper de paginación
        if page and per_page:
            return apply_pagination(query, page, per_page)

        items = query.all()
        total = len(items)
        return items, total

    @staticmethod
    def actualizar_facultad(facultad) -> Facultad:

        facultad_existente = db.session.merge(facultad)
        if not facultad_existente:
            return None
        return facultad_existente

    @staticmethod
    def borrar_por_id(id: int) -> Facultad:
        facultad = db.session.query(Facultad).filter_by(id=id).first()
        if not facultad:
            return None
        db.session.delete(facultad)
        db.session.commit()
        return facultad

#Respondida en Issue #5 Pregunta 3

# from abc import ABC, abstractmethod
# from app.models import Facultad

# class FacultadRepository(ABC):
#     @abstractmethod
#     def crear(self, facultad: Facultad) -> Facultad:
#         pass
    
#     @abstractmethod
#     def buscar_por_id(self, id: int) -> Facultad:
#         pass
    
#     @abstractmethod
#     def buscar_todos(self) -> list[Facultad]:
#         pass
    
#     @abstractmethod
#     def actualizar(self, facultad: Facultad) -> Facultad:
#         pass
    
#     @abstractmethod
#     def borrar_por_id(self, id: int) -> Facultad:
#         pass