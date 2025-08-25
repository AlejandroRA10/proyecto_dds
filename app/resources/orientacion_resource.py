from flask import Blueprint, request, jsonify
from app.services.orientacion_service import OrientacionService
from app.models.orientacion import Orientacion
from app import db
from app.validators.orientacion_validator import validate_orientacion
from app.mapping.orientacion_mapping import OrientacionMapping

orientacion_blueprint = Blueprint('orientacion', __name__)
orientacion_mapping = OrientacionMapping()

@orientacion_blueprint.route('/orientaciones', methods=['GET'])
def get_all_orientaciones():
    orientaciones = OrientacionService.buscar_todos()
    return jsonify([orientacion.to_dict() for orientacion in orientaciones]), 200

@orientacion_blueprint.route('/orientacion/<hashid:id>', methods=['GET'])
def get_orientacion_by_id(id: int):
    orientacion = OrientacionService.buscar_por_id(id)
    if not orientacion:
        return jsonify({"error": "Orientación no encontrada"}), 404
    return jsonify(orientacion.to_dict()), 200

@orientacion_blueprint.route('/orientacion', methods=['POST'])
def create_orientacion():
    data = request.get_json()
    if not data or 'nombre' not in data:
        return jsonify({"error": "Datos inválidos"}), 400
    try:
        nueva_orientacion = OrientacionService.crear_orientacion(data)
        return jsonify(nueva_orientacion.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@orientacion_blueprint.route('/orientacion/<hashid:id>', methods=['PUT'])
def update(id: int):
    data = request.get_json()
    errors = validate_orientacion(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    orientacion_actualizado = OrientacionService.actualizar_orientacion(id, data)
    if not orientacion_actualizado:
        return jsonify({"error": "Orientacion no encontrada"}), 404
    
    return orientacion_mapping.dump(orientacion_actualizado), 200

@orientacion_blueprint.route('/orientacion/<hashid:id>', methods=['DELETE'])
def delete_orientacion(id: int):
    eliminado = OrientacionService.borrar_orientacion(id)
    if not eliminado:
        return jsonify({"error": "Orientación no encontrada"}), 404
    return jsonify({"message": "Orientación eliminada"}), 200
