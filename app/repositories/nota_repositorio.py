from app.models.nota import Nota
from app import db

class NotaRepository:
    @staticmethod
    def crear(nota: Nota) -> Nota:
        db.session.add(nota)
        db.session.commit()
        return nota

    @staticmethod
    def buscar_todos():
        return db.session.query(Nota).all()

    @staticmethod
    def buscar_filtrado_paginado(filters: dict, page: int = 1, per_page: int = 20):
        """
        Aplica filtros simples sobre Nota y devuelve (items, total)
        filtros soportados en `filters`: inscripcion_id, valor_min, valor_max
        """
        query = db.session.query(Nota)

        if not filters:
            filters = {}

        inscripcion_id = filters.get('inscripcion_id')
        if inscripcion_id is not None:
            try:
                inscripcion_id = int(inscripcion_id)
                query = query.filter(Nota.inscripcion_id == inscripcion_id)
            except (TypeError, ValueError):
                pass

        valor_min = filters.get('valor_min')
        if valor_min is not None:
            try:
                valor_min = float(valor_min)
                query = query.filter(Nota.valor >= valor_min)
            except (TypeError, ValueError):
                pass

        valor_max = filters.get('valor_max')
        if valor_max is not None:
            try:
                valor_max = float(valor_max)
                query = query.filter(Nota.valor <= valor_max)
            except (TypeError, ValueError):
                pass

        total = query.count()

        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 20

        offset = (page - 1) * per_page
        items = query.offset(offset).limit(per_page).all()

        return items, total

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Nota).filter_by(id=id).first()
    
    @staticmethod
    def actualizar(nota: Nota) -> Nota:
        nota_existente = db.session.merge(nota)
        db.session.commit()
        return nota_existente
    
    @staticmethod
    def borrar_por_id(id: int) -> Nota:
        nota = db.session.query(Nota).filter_by(id=id).first()
        if nota:
            db.session.delete(nota)
            db.session.commit()
        return nota
