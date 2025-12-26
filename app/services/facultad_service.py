from app.models import Facultad
from app.repositories.facultad_repositorio import FacultadRepository

class FacultadService:
   
    @staticmethod
    def crear_facultad(facultad: Facultad):
        FacultadRepository.crear(facultad)
    
    @staticmethod
    def buscar_por_id(id: int) -> Facultad:
        return FacultadRepository.buscar_por_id(id)
    
    @staticmethod
    def buscar_todos(page: int = None, per_page: int = None, q: str = None):
        """Si se pasan page/per_page o q devuelve paginación {'page','per_page','total','items'},
        si no, devuelve la lista completa de facultades para compatibilidad hacia atrás.
        """
        if page is not None or per_page is not None or q is not None:
            # normalizar valores
            page = int(page) if page is not None else 1
            per_page = int(per_page) if per_page is not None else 10
            items, total = FacultadRepository.buscar_filtrados(page=page, per_page=per_page, q=q)
            return {
                'page': page,
                'per_page': per_page,
                'total': total,
                'items': items
            }

        return FacultadRepository.buscar_todos()
    
    @staticmethod
    def actualizar_facultad(id: int, facultad: Facultad) -> Facultad:
        facultad_existente = FacultadRepository.buscar_por_id(id)
        if not facultad_existente:
            return None
        facultad_existente.nombre = facultad.nombre
        facultad_existente.abreviatura = facultad.abreviatura
        facultad_existente.directorio = facultad.directorio
        facultad_existente.sigla = facultad.sigla
        facultad_existente.codigo_postal = facultad.codigo_postal
        facultad_existente.ciudad = facultad.ciudad
        facultad_existente.domicilio = facultad.domicilio
        facultad_existente.telefono = facultad.telefono
        facultad_existente.contacto = facultad.contacto
        return facultad_existente
        
    @staticmethod
    def borrar_por_id(id: int) -> Facultad:
        facultad = FacultadRepository.buscar_por_id(id)
        if not facultad:
            return None
        return facultad