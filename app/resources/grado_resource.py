from flask import Blueprint, request, jsonify
from app.services.grado_service import GradoService
from app.mapping.grado_mapping import GradoMapping
from app.validators.grado_validator import validate_grado

grado_bp = Blueprint('grado', __name__)
grado_mapping = GradoMapping()

@grado_bp.route('/grados', methods=['GET'])
def read_all():
    grados = GradoService.buscar_todos()
    return grado_mapping.dump(grados, many=True), 200

@grado_bp.route('/grado/<hashid:id>', methods=['GET'])
def read_by_id(id: int):
    grado = GradoService.buscar_por_id(id)
    if not grado:
        return jsonify({"error": "Grado no encontrado"}), 404
    return grado_mapping.dump(grado), 200

@grado_bp.route('/grado', methods=['POST'])
def create():
    data = request.get_json()
    try:
        nuevo_grado = GradoService.crear_grado(data)
        return grado_mapping.dump(nuevo_grado), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@grado_bp.route('/grado/<hashid:id>', methods=['PUT'])
def update(id: int):
    data = request.get_json()
    errors = validate_grado(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    grado_actualizado = GradoService.actualizar_grado(id, data)
    if not grado_actualizado:
        return jsonify({"error": "Grado no encontrado"}), 404
    
    return grado_mapping.dump(grado_actualizado), 200

@grado_bp.route('/grado/<hashid:id>', methods=['DELETE'])
def delete(id: int):
    eliminado = GradoService.borrar_grado(id)
    if not eliminado:
        return jsonify({"error": "Grado no encontrado"}), 404
    return jsonify({"message": "Grado eliminado"}), 200
