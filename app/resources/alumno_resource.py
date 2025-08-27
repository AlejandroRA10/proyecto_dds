from flask import Blueprint, request, jsonify
from app.services.alumno_service import AlumnoService
from app.mapping.alumno_mapping import AlumnoMapping
from app.validators.alumno_validator import validate_alumno

#Pregunta 4 - #6
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

@alumno_bp.route('/alumno/<hashid:id>/ficha', methods=['GET'])
def generar_ficha_alumno(id: int):
    """Genera la ficha del alumno en formato PDF o JSON según el parámetro 'formato'"""
    formato = request.args.get('formato', 'json').lower()
    
    try:
        if formato == 'pdf':
            ficha_pdf = AlumnoService.generar_ficha_alumno_pdf(id)
            if not ficha_pdf:
                return jsonify({"error": "Alumno no encontrado"}), 404
            
            from flask import send_file
            return send_file(
                ficha_pdf,
                as_attachment=True,
                download_name=f"ficha_alumno_{id}.pdf",
                mimetype='application/pdf'
            )
            
        elif formato == 'json':
            ficha_json = AlumnoService.generar_ficha_alumno_json(id)
            if not ficha_json:
                return jsonify({"error": "Alumno no encontrado"}), 404
            
            return jsonify(ficha_json), 200
            
        else:
            return jsonify({"error": "Formato no soportado. Use 'pdf' o 'json'"}), 400
            
    except Exception as e:
        return jsonify({"error": f"Error al generar la ficha: {str(e)}"}), 500
