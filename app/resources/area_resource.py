from flask import Blueprint, request, jsonify
from app.services.area_service import AreaService
from app.mapping.area_mapping import AreaMapping
from app.validators.area_validator import validate_area

area_bp = Blueprint('area', __name__)
area_mapping = AreaMapping()

@area_bp.route('/areas', methods=['GET'])
def read_all():
    areas = AreaService.buscar_todos()
    return area_mapping.dump(areas, many=True), 200

@area_bp.route('/area/<hashid:id>', methods=['GET'])
def read_by_id(id: int):
    area = AreaService.buscar_por_id(id)
    if not area:
        return jsonify({"error": "Área no encontrada"}), 404
    return area_mapping.dump(area), 200

@area_bp.route('/area', methods=['POST'])
def create():
    data = request.get_json()
    try:
        nueva_area = AreaService.crear_area(data)
        return area_mapping.dump(nueva_area), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@area_bp.route('/area/<hashid:id>', methods=['PUT'])
def update(id: int):
    data = request.get_json()
    errors = validate_area(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    area_actualizado = AreaService.actualizar_area(id, data)
    if not area_actualizado:
        return jsonify({"error": "Area no encontrada"}), 404
    
    return area_mapping.dump(area_actualizado), 200

@area_bp.route('/area/<hashid:id>', methods=['DELETE'])
def delete(id: int):
    eliminado = AreaService.borrar_area(id)
    if not eliminado:
        return jsonify({"error": "Área no encontrada"}), 404
    return jsonify({"message": "Área eliminada"}), 200
