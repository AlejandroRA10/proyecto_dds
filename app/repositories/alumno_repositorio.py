from app.models.alumno import Alumno
from app import db

class AlumnoRepository:
    @staticmethod
    def crear(alumno):
        db.session.add(alumno)
        db.session.commit()
        return alumno

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Alumno).filter_by(id=id).first()

    @staticmethod
    def buscar_todos():
        return db.session.query(Alumno).all()

    @staticmethod
    def actualizar(alumno):
        alumno_existente = db.session.merge(alumno)
        db.session.commit()
        return alumno_existente

    @staticmethod
    def borrar_por_id(id: int):
        alumno = db.session.query(Alumno).filter_by(id=id).first()
        if not alumno:
            return None
        db.session.delete(alumno)
        db.session.commit()
        return alumno