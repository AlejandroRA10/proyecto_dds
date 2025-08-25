from flask import Blueprint, request, jsonify
from app.services.cargo_service import CargoService
from app.mapping.cargo_mapping import CargoMapping
from app.validators.cargo_validator import validate_cargo

cargo_bp = Blueprint('cargo', __name__)
cargo_mapping = CargoMapping()

@cargo_bp.route('/cargos', methods=['GET'])
def read_all():
    cargos = CargoService.buscar_todos()
    return cargo_mapping.dump(cargos, many=True), 200

@cargo_bp.route('/cargo/<hashid:id>', methods=['GET'])
def read_by_id(id: int):
    cargo = CargoService.buscar_por_id(id)
    if not cargo:
        return jsonify({"error": "Cargo no encontrado"}), 404
    return cargo_mapping.dump(cargo), 200

@cargo_bp.route('/cargo', methods=['POST'])
def create():
    data = request.get_json()
    try:
        nuevo_cargo = CargoService.crear_cargo(data)
        return cargo_mapping.dump(nuevo_cargo), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@cargo_bp.route('/cargo/<hashid:id>', methods=['PUT'])
def update(id: int):
    data = request.get_json()
    errors = validate_cargo(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    cargo_actualizado = CargoService.actualizar_cargo(id, data)
    if not cargo_actualizado:
        return jsonify({"error": "Cargo no encontrado"}), 404
    
    return cargo_mapping.dump(cargo_actualizado), 200

@cargo_bp.route('/cargo/<hashid:id>', methods=['DELETE'])
def delete(id: int):
    eliminado = CargoService.borrar_cargo(id)
    if not eliminado:
        return jsonify({"error": "Cargo no encontrado"}), 404
    return jsonify({"message": "Cargo eliminado"}), 200
