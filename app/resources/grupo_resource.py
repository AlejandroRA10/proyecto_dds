from flask import Blueprint, request, jsonify
from app.services.grupo_service import GrupoService
from app.models.grupo import Grupo
from app import db
from app.validators.grupo_validator import validate_grupo
from app.mapping.grupo_mapping import GrupoMapping


grupo_blueprint = Blueprint('grupo', __name__)
grupo_mapping = GrupoMapping()

@grupo_blueprint.route('/grupos', methods=['GET'])
def get_all_grupos():
    grupos = GrupoService.buscar_todos()
    return jsonify([grupo.to_dict() for grupo in grupos]), 200

@grupo_blueprint.route('/grupo/<hashid:id>', methods=['GET'])
def get_grupo_by_id(id: int):
    grupo = GrupoService.buscar_por_id(id)
    if not grupo:
        return jsonify({"error": "Grupo no encontrado"}), 404
    return jsonify(grupo.to_dict()), 200

@grupo_blueprint.route('/grupo', methods=['POST'])
def create_grupo():
    data = request.get_json()
    errors = validate_grupo(data)
    if errors:
        return jsonify({'errors': errors}), 400
    try:
        nuevo_grupo = GrupoService.crear_grupo(data)
        return jsonify(nuevo_grupo.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@grupo_blueprint.route('/grupo/<hashid:id>', methods=['PUT'])
def update(id: int):
    data = request.get_json()
    errors = validate_grupo(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    grupo_actualizado = GrupoService.actualizar_grupo(id, data)
    if not grupo_actualizado:
        return jsonify({"error": "Grupo no encontrado"}), 404
    
    return grupo_mapping.dump(grupo_actualizado), 200

@grupo_blueprint.route('/grupo/<hashid:id>', methods=['DELETE'])
def delete_grupo(id: int):
    eliminado = GrupoService.borrar_grupo(id)
    if not eliminado:
        return jsonify({"error": "Grupo no encontrado"}), 404
    return jsonify({"message": "Grupo eliminado"}), 200