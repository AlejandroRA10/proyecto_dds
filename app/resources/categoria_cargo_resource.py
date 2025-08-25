from flask import Blueprint, request, jsonify
from app.services.categoria_cargo_service import CategoriaCargoService
from app.mapping.categoria_cargo_mapping import CategoriaCargoMapping
from app.validators.categoria_cargo_validator import validate_categoria_cargo

categoria_cargo_bp = Blueprint('categoria_cargo', __name__)
categoria_cargo_mapping = CategoriaCargoMapping()

@categoria_cargo_bp.route('/categorias_cargo', methods=['GET'])
def read_all():
    categorias_cargo = CategoriaCargoService.buscar_todos()
    return categoria_cargo_mapping.dump(categorias_cargo, many=True), 200

@categoria_cargo_bp.route('/categoria_cargo/<hashid:id>', methods=['GET'])
def read_by_id(id: int):
    categoria_cargo = CategoriaCargoService.buscar_por_id(id)
    if not categoria_cargo:
        return jsonify({"error": "Categoria de cargo no encontrada"}), 404
    return categoria_cargo_mapping.dump(categoria_cargo), 200

@categoria_cargo_bp.route('/categoria_cargo', methods=['POST'])
def create():
    data = request.get_json()
    try:
        nueva_categoria_cargo = CategoriaCargoService.crear_categoria_cargo(
            data)
        return categoria_cargo_mapping.dump(nueva_categoria_cargo), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@categoria_cargo_bp.route('/categoria_cargo/<hashid:id>', methods=['PUT'])

def update(id: int):
    data = request.get_json()
    errors = validate_categoria_cargo(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    categoria_cargo_actualizado = CategoriaCargoService.actualizar_cargo(id, data)
    if not categoria_cargo_actualizado:
        return jsonify({"error": "Categoria cargo no encontrado"}), 404
    
    return categoria_cargo_mapping.dump(categoria_cargo_actualizado), 200

    def test_borrar_grado(self):
        grado = self.__nuevoGrado()
        GradoService.crear_grado(grado)
        resultado = GradoService.borrar_grado(grado.id)
        self.assertTrue(resultado)
        grado_buscado = GradoService.buscar_por_id(grado.id)
        self.assertIsNone(grado_buscado)

@categoria_cargo_bp.route('/categoria_cargo/<hashid:id>', methods=['DELETE'])
def delete(id: int):
    eliminado = CategoriaCargoService.borrar_categoria_cargo(id)
    if not eliminado:
        return jsonify({"error": "Categoria de cargo no encontrada"}), 404
    return jsonify({"message": "Categoria de cargo eliminada"}), 200

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    app.register_blueprint(categoria_cargo_bp)
    app.run(debug=True)
