from flask import Blueprint, request, jsonify
from app.services.departamento_service import DepartamentoService
from app.mapping.departamento_mapping import DepartamentoMapping
from app.validators.departamento_validator import validate_departamento

departamento_bp = Blueprint('departamento', __name__)
departamento_mapping = DepartamentoMapping()

@departamento_bp.route('/departamentos', methods=['GET'])
def read_all():
    departamentos = DepartamentoService.buscar_todos()
    return departamento_mapping.dump(departamentos, many=True), 200

@departamento_bp.route('/departamento/<hashid:id>', methods=['GET'])
def read_by_id(id: int):
    departamento = DepartamentoService.buscar_por_id(id)
    if not departamento:
        return jsonify({"error": "Departamento no encontrado"}), 404
    return departamento_mapping.dump(departamento), 200

@departamento_bp.route('/departamento', methods=['POST'])
def create():
    data = request.get_json()
    errors = validate_departamento(data)
    if errors:
        return jsonify({'errors': errors}), 400
    try:
        nuevo_departamento = DepartamentoService.crear_departamento(data)
        return departamento_mapping.dump(nuevo_departamento), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

def update(id: int):
    data = request.get_json()
    errors = validate_departamento(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    departamento_actualizado = DepartamentoService.actualizar_cargo(id, data)
    if not departamento_actualizado:
        return jsonify({"error": "Departamento no encontrado"}), 404
    
    return departamento_mapping.dump(departamento_actualizado), 200

@departamento_bp.route('/departamento/<hashid:id>', methods=['DELETE'])
def delete(id: int):
    eliminado = DepartamentoService.borrar_departamento(id)
    if not eliminado:
        return jsonify({"error": "Departamento no encontrado"}), 404
    return jsonify({"message": "Departamento eliminado"}), 200