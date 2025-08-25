from flask import Blueprint, request, jsonify
from app.services.alumno_service import AlumnoService
from app.mapping.alumno_mapping import AlumnoMapping
from app.validators.alumno_validator import validate_alumno

alumno_bp = Blueprint('alumno', __name__)
alumno_mapping = AlumnoMapping()

@alumno_bp.route('/alumnos', methods=['GET'])
def read_all():
    alumnos = AlumnoService.buscar_todos()
    return alumno_mapping.dump(alumnos, many=True), 200

@alumno_bp.route('/alumno/<hashid:id>', methods=['GET'])
def read_by_id(id: int):
    alumno = AlumnoService.buscar_por_id(id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return alumno_mapping.dump(alumno), 200

@alumno_bp.route('/alumno', methods=['POST'])
def create():
    data = request.get_json()
    errors = validate_alumno(data)
    if errors:
        return jsonify({'errors': errors}), 400
    try:
        nuevo_alumno = AlumnoService.crear_alumno(data)
        return alumno_mapping.dump(nuevo_alumno), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@alumno_bp.route('/alumno/<hashid:id>', methods=['PUT'])
def update(id: int):
    data = request.get_json()
    errors = validate_alumno(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    alumno_actualizado = AlumnoService.actualizar_alumno(id, data)
    if not alumno_actualizado:
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    return alumno_mapping.dump(alumno_actualizado), 200

@alumno_bp.route('/alumno/<hashid:id>', methods=['DELETE'])
def delete(id: int):
    eliminado = AlumnoService.borrar_alumno(id)
    if not eliminado:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return jsonify({"message": "Alumno eliminado"}), 200