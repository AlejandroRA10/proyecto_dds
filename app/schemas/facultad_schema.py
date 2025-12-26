from app import ma
from app.models.facultad import Facultad


class FacultadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Facultad
        load_instance = True
        include_fk = True
