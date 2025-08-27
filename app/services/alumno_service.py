import datetime
from io import BytesIO
import json
from typing import Dict, Any

from app.models import Alumno
from app.repositories import AlumnoRepository
# Importamos directamente desde el módulo específico para evitar la importación circular
from app.services.documentos_office_service import Document, obtener_tipo_documento, DOCXDocument, PDFDocument, ODTDocument

class AlumnoService:

    @staticmethod
    def crear(alumno):
        AlumnoRepository.crear(alumno)

    @staticmethod
    def buscar_por_id(id: int) -> Alumno:        
        return AlumnoRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Alumno]:
        return AlumnoRepository.buscar_todos()
    
    @staticmethod
    def actualizar(id: int, alumno: Alumno) -> Alumno:
        alumno_existente = AlumnoRepository.buscar_por_id(id)
        if not alumno_existente:
            return None
        alumno_existente.nombre = alumno.nombre
        alumno_existente.apellido = alumno.apellido
        alumno_existente.nrodocumento = alumno.nrodocumento
        alumno_existente.tipo_documento = alumno.tipo_documento
        alumno_existente.fecha_nacimiento = alumno.fecha_nacimiento
        alumno_existente.sexo = alumno.sexo
        alumno_existente.nro_legajo = alumno.nro_legajo
        alumno_existente.fecha_ingreso = alumno.fecha_ingreso
        return alumno_existente
        
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return AlumnoRepository.borrar_por_id(id)
    
    @staticmethod
    def generar_certificado_alumno_regular(id: int, tipo: str) -> BytesIO:
        alumno = AlumnoRepository.buscar_por_id(id)
        if not alumno:
            return None
        
        context = AlumnoService.__obtener_alumno(alumno)

        documento = obtener_tipo_documento(tipo)
        if not documento:
            return None

        return documento.generar(
            carpeta='certificado',
            plantilla=f'certificado_{tipo}',
            context=context
        )

    @staticmethod
    def __obtener_fecha_actual():
        fecha_actual = datetime.datetime.now()
        fecha_str = fecha_actual.strftime('%d de %B de %Y')
        return fecha_str

    @staticmethod
    def __obtener_alumno(alumno: Alumno) -> dict:
        especialidad = alumno.especialidad
        facultad = especialidad.facultad
        universidad = facultad.universidad
        return {
            "alumno": alumno,
            "especialidad": especialidad,
            "facultad": facultad,
            "universidad": universidad,
            "fecha": AlumnoService.__obtener_fecha_actual()
        }

    @staticmethod
    def generar_ficha_alumno_pdf(id: int):
        """Genera la ficha del alumno en formato PDF"""
        alumno = AlumnoRepository.buscar_por_id(id)
        if not alumno:
            return None
        
        context = AlumnoService.__obtener_alumno(alumno)
        
        documento = PDFDocument()
        return documento.generar(
            carpeta='ficha',
            plantilla='ficha_alumno',
            context=context
        )

    @staticmethod
    def generar_ficha_alumno_json(id: int):
        """Genera la ficha del alumno en formato JSON"""
        alumno = AlumnoRepository.buscar_por_id(id)
        if not alumno:
            return None
        
        context = AlumnoService.__obtener_alumno(alumno)
        
        # Estructura específica para la ficha JSON
        ficha_json = {
            "alumno": {
                "nro_legajo": alumno.nro_legajo,
                "apellido": alumno.apellido,
                "nombre": alumno.nombre,
                "nro_documento": alumno.nro_documento,
                "fecha_nacimiento": alumno.fecha_nacimiento,
                "fecha_ingreso": alumno.fecha_ingreso
            },
            "facultad": {
                "nombre": context["facultad"].nombre,
                "abreviatura": context["facultad"].abreviatura,
                "sigla": context["facultad"].sigla
            },
            "especialidad": {
                "nombre": context["especialidad"].nombre
            },
            "universidad": {
                "nombre": context["universidad"].nombre
            },
            "fecha_generacion": context["fecha"]
        }
        
        return ficha_json

    @staticmethod
    def generar_ficha_alumno(id: int, formato: str = 'json'):
        """Genera la ficha del alumno en el formato especificado"""
        if formato.lower() == 'pdf':
            return AlumnoService.generar_ficha_alumno_pdf(id)
        elif formato.lower() == 'json':
            return AlumnoService.generar_ficha_alumno_json(id)
        else:
            raise ValueError(f"Formato no soportado: {formato}")
