from flask import Blueprint, request, jsonify
from app.services.materia_service import MateriaService
from app.models.materia import Materia
from app import db
from app.validators.materia_validator import validate_materia
from app.mapping.materia_mapping import MateriaMapping

materia_mapping = MateriaMapping()
materia_blueprint = Blueprint('materia', __name__)

@materia_blueprint.route('/materias', methods=['GET'])
def get_all_materias():
    materias = MateriaService.buscar_todos()
    return jsonify([materia.to_dict() for materia in materias]), 200

@materia_blueprint.route('/materia/<hashid:id>', methods=['GET'])
def get_materia_by_id(id: int):
    materia = MateriaService.buscar_por_id(id)
    if not materia:
        return jsonify({"error": "Materia no encontrada"}), 404
    return jsonify(materia.to_dict()), 200

@materia_blueprint.route('/materia', methods=['POST'])
def create_materia():
    data = request.get_json()
    if not data or 'nombre' not in data:
        return jsonify({"error": "Datos inválidos"}), 400
    errors = validate_materia(data)
    if errors:
        return jsonify({'errors': errors}), 400
    try:
        nueva_materia = MateriaService.crear_materia(data)
        return jsonify(nueva_materia.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@materia_blueprint.route('/materia/<hashid:id>', methods=['PUT'])
def update(id: int):
    data = request.get_json()
    errors = validate_materia(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    materia_actualizado = MateriaService.actualizar_materia(id, data)
    if not materia_actualizado:
        return jsonify({"error": "Materia no encontrada"}), 404
    
    return materia_mapping.dump(materia_actualizado), 200

@materia_blueprint.route('/materia/<hashid:id>', methods=['DELETE'])
def delete_materia(id: int):
    eliminado = MateriaService.borrar_materia(id)
    if not eliminado:
        return jsonify({"error": "Materia no encontrada"}), 404
    return jsonify({"message": "Materia eliminada"}), 200