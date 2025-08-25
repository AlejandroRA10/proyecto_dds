from flask import jsonify, Blueprint, request
from app.services import UniversidadService
from app.mapping import UniversidadMapping
from markupsafe import escape
from app.validators.universidad_validator import validate_universidad


universidad_bp = Blueprint('universidad', __name__)
universidad_mapping = UniversidadMapping()


@universidad_bp.route('/universidad', methods=['GET'])
def index():
    universidades = UniversidadService.buscar_todos()
    return universidad_mapping.dump(universidades, many=True), 200


@universidad_bp.route('/universidad/<hashid:id>', methods=['GET'])
def buscar_por_id(id: int):
    universidad = UniversidadService.buscar_por_id(id)
    return universidad_mapping.dump(universidad), 200


@universidad_bp.route('/universidad', methods=['POST'])
def crear_universidad():
    universidad_data = sanitize_universidad_input(request)
    universidad = UniversidadService.crear(universidad_data)
    return universidad_mapping.dump(universidad), 201


@universidad_bp.route('/universidad/<hashid:id>', methods=['DELETE'])
def eliminar_universidad(id: int):
    UniversidadService.eliminar(id)
    return jsonify('Universidad eliminada exitosamente'), 200


@universidad_bp.route('/universidad/<hashid:id>', methods=['PUT'])
def update(id: int):
    data = request.get_json()
    errors = validate_universidad(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    universidad_actualizado = UniversidadService.actualizar_tipo_documento(id, data)
    if not universidad_actualizado:
        return jsonify({"error": "Universidad no encontrada"}), 404
    
    return universidad_mapping.dump(universidad_actualizado), 200


def sanitize_universidad_input(request):
    universidad_data = universidad_mapping.load(request.json())
    universidad_data.nombre = escape(universidad_data.nombre)
    universidad_data.sigla = escape(universidad_data.sigla)
    return universidad_data
