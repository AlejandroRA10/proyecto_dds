from flask import Blueprint, request, jsonify
from app.services.nota_service import NotaService
from app.mapping.nota_mapping import NotaMapping
from app.validators.nota_validator import validate_nota

nota_bp = Blueprint('nota', __name__)
nota_mapping = NotaMapping()

@nota_bp.route('/notas', methods=['GET'])
def read_all():
    notas = NotaService.buscar_todos()
    return nota_mapping.dump(notas, many=True), 200

@nota_bp.route('/nota/<int:id>', methods=['GET'])
def read_by_id(id):
    nota = NotaService.buscar_por_id(id)
    return nota_mapping.dump(nota), 200


# Endpoint para crear una nota
@nota_bp.route('/notas', methods=['POST'])
def create_nota():
    data = request.get_json()
    errors = validate_nota(data)
    if errors:
        return jsonify({'errors': errors}), 400
    nueva_nota = NotaService.crear(data)
    return nota_mapping.dump(nueva_nota), 201

# Endpoint para actualizar una nota
@nota_bp.route('/nota/<int:id>', methods=['PUT'])
def update(id: int):
    data = request.get_json()
    errors = validate_nota(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    nota_actualizado = NotaService.actualizar_nota(id, data)
    if not nota_actualizado:
        return jsonify({"error": "Nota no encontrada"}), 404
    
    return nota_mapping.dump(nota_actualizado), 200