from flask import Blueprint, request, jsonify
from app.services.nota_service import NotaService
from app.mapping.nota_mapping import NotaMapping
from app.validators.nota_validator import validate_nota

nota_bp = Blueprint('nota', __name__)
nota_mapping = NotaMapping()

@nota_bp.route('/notas', methods=['GET'])
def read_all():
    # Parámetros de paginación y filtrado
    try:
        page = int(request.args.get('page', 1))
    except (TypeError, ValueError):
        page = 1

    try:
        per_page = int(request.args.get('per_page', 20))
    except (TypeError, ValueError):
        per_page = 20

    # Filtros permitidos: inscripcion_id, valor_min, valor_max
    filters = {
        'inscripcion_id': request.args.get('inscripcion_id'),
        'valor_min': request.args.get('valor_min'),
        'valor_max': request.args.get('valor_max')
    }

    items, total = NotaService.buscar_filtrado_paginado(filters, page, per_page)
    notas_serializadas = nota_mapping.dump(items, many=True)

    total_pages = (total + per_page - 1) // per_page if per_page else 1

    meta = {
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages
    }

    return jsonify({'items': notas_serializadas, 'meta': meta}), 200

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
    
    nota_actualizado = NotaService.actualizar(id, data)
    if not nota_actualizado:
        return jsonify({"error": "Nota no encontrada"}), 404
    
    return nota_mapping.dump(nota_actualizado), 200