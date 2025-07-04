from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class TipoDedicacion(db.Model):
    __tablename__ = 'tipos_dedicacion'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    observacion = db.Column(db.String(200), nullable=True)
    cargos = db.relationship('Cargo', back_populates='tipo_dedicacion', lazy=True)