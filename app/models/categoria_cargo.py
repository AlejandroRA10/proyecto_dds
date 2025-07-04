from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class CategoriaCargo(db.Model):
    __tablename__ = 'categorias_cargo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    cargos = db.relationship('Cargo', back_populates='categoria_cargo', lazy=True)