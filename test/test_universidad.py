import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_simple_app(config_name='testing'):
    from flask import Flask
    from app.config import config
    
    app = Flask(__name__)
    config_class = config.get(config_name, config['default'])
    app.config.from_object(config_class)
    from app import db
    db.init_app(app)
    return app

from flask import current_app
from app.models.universidad import Universidad
from app.models.facultad import Facultad
from app.repositories.universidad_repositorio import UniversidadRepository
from app import db

class UniversidadTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_simple_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self): 
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_universidad_creation(self):
        universidad = self.__nuevaUniversidad()
        self.assertIsNotNone(universidad)
        self.assertEqual(universidad.nombre, "Universidad Nacional de La Plata")
        self.assertEqual(universidad.sigla, "UNLP")
        self.assertIsNotNone(universidad.nombre)
        self.assertIsNotNone(universidad.sigla)
        
    def test_crear_universidad(self):
        universidad = self.__nuevaUniversidad()
        UniversidadRepository.crear(universidad)
        self.assertIsNotNone(universidad)
        self.assertIsNotNone(universidad.id)
        self.assertGreaterEqual(universidad.id, 1)
        self.assertEqual(universidad.nombre, "Universidad Nacional de La Plata")
        self.assertEqual(len(universidad.facultades), 2)  
        
    def test_universidad_busqueda(self):
        universidad = self.__nuevaUniversidad()
        UniversidadRepository.crear(universidad)
        universidad_encontrada = UniversidadRepository.buscar_por_id(universidad.id)
        self.assertIsNotNone(universidad_encontrada)
        self.assertEqual(universidad_encontrada.nombre, "Universidad Nacional de La Plata")
        self.assertEqual(universidad_encontrada.sigla, "UNLP")
    
    def test_buscar_universidades(self):
        universidad1 = self.__nuevaUniversidad()
        universidad2 = self.__nuevaUniversidad()
        UniversidadRepository.crear(universidad1)
        UniversidadRepository.crear(universidad2)
        universidades = UniversidadRepository.buscar_todos()
        self.assertIsNotNone(universidades)
        self.assertEqual(len(universidades), 2)
        
    def test_actualizar_universidad(self):
        universidad = self.__nuevaUniversidad()
        UniversidadRepository.crear(universidad)
        universidad.nombre = "Universidad Nacional de Buenos Aires"
        universidad_actualizada = UniversidadRepository.actualizar(universidad)
        self.assertEqual(universidad_actualizada.nombre, "Universidad Nacional de Buenos Aires")
        
    def test_borrar_universidad(self):
        universidad = self.__nuevaUniversidad()
        UniversidadRepository.crear(universidad)
        
        for facultad in universidad.facultades:
            db.session.delete(facultad)
        db.session.commit()
        
        UniversidadRepository.borrar_por_id(universidad.id)
        universidad_borrada = UniversidadRepository.buscar_por_id(universidad.id)
        self.assertIsNone(universidad_borrada)
        
    def __nuevaUniversidad(self):
        universidad = Universidad()
        universidad.nombre = "Universidad Nacional de La Plata"
        universidad.sigla = "UNLP"
        
        db.session.add(universidad)
        db.session.flush()
        
        facultad1 = self.__nuevafacultad()
        facultad2 = self.__nuevafacultad2()
        
        facultad1.universidad_id = universidad.id
        facultad2.universidad_id = universidad.id
        
        universidad.facultades.append(facultad1)
        universidad.facultades.append(facultad2)
        
        return universidad
    
    
    def __nuevafacultad(self):
        facultad = Facultad()
        facultad.nombre = "Facultad de Ingenieria"
        facultad.abreviatura = "FI"
        facultad.directorio = "ingenieria"
        facultad.sigla = "FI"
        facultad.email = "ingenieria@test.edu"
        return facultad

    def __nuevafacultad2(self):
        facultad = Facultad()
        facultad.nombre = "Facultad de Ciencias Exactas"
        facultad.abreviatura = "FCE"
        facultad.directorio = "exactas"
        facultad.sigla = "FCE"
        facultad.email = "exactas@test.edu"
        return facultad
    
if __name__ == '__main__':
    unittest.main()