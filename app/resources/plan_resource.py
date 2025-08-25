from flask import Blueprint, request, jsonify
from app.services.plan_service import PlanService
from app.mapping.plan_mapping import PlanMapping
from app.validators.plan_validator import validate_plan

plan_bp = Blueprint('plan', __name__)
plan_mapping = PlanMapping()

@plan_bp.route('/planes', methods=['GET'])
def read_all():
    planes = PlanService.buscar_todos()
    return plan_mapping.dump(planes, many=True), 200

@plan_bp.route('/plan/<hashid:id>', methods=['GET'])
def read_by_id(id: int):
    plan = PlanService.buscar_por_id(id)
    if not plan:
        return jsonify({"error": "Plan no encontrado"}), 404
    return plan_mapping.dump(plan), 200

@plan_bp.route('/plan', methods=['POST'])
def create():
    data = request.get_json()
    try:
        nuevo_plan = PlanService.crear_plan(data)
        return plan_mapping.dump(nuevo_plan), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@plan_bp.route('/plan/<hashid:id>', methods=['PUT'])
def update(id: int):
    data = request.get_json()
    errors = validate_plan(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    plan_actualizado = PlanService.actualizar_plan(id, data)
    if not plan_actualizado:
        return jsonify({"error": "Plan no encontrado"}), 404
    
    return plan_mapping.dump(plan_actualizado), 200

@plan_bp.route('/plan/<hashid:id>', methods=['DELETE'])
def delete(id: int):
    eliminado = PlanService.borrar_plan(id)
    if not eliminado:
        return jsonify({"error": "Plan no encontrado"}), 404
    return jsonify({"message": "Plan eliminado"}), 200

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    app.register_blueprint(plan_bp)
    app.run(debug=True)