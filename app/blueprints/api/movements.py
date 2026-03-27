from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, current_user
from app.extensions import db
from app.models import Movement, Product

api_movements = Blueprint("api_movements", __name__, url_prefix="/api/movements")


@api_movements.route("", methods=["GET"])
def get_movements():
    movements = Movement.query.order_by(Movement.created_at.desc()).all()
    return jsonify([m.to_dict() for m in movements])


@api_movements.route("", methods=["POST"])
def create_movement():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["product_id", "movement_type", "quantity"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    if data["movement_type"] not in ["entry", "exit"]:
        return jsonify(
            {"error": 'Invalid movement_type. Must be "entry" or "exit"'}
        ), 400

    product = Product.query.get(data["product_id"])
    if not product:
        return jsonify({"error": "Product not found"}), 404

    quantity = data["quantity"]

    if data["movement_type"] == "exit" and product.stock < quantity:
        return jsonify(
            {"error": f"Insufficient stock. Current stock: {product.stock}"}
        ), 400

    movement = Movement(
        product_id=product.id,
        user_id=1,
        movement_type=data["movement_type"],
        quantity=quantity,
        notes=data.get("notes", ""),
    )

    if data["movement_type"] == "entry":
        product.stock += quantity
    else:
        product.stock -= quantity

    db.session.add(movement)
    db.session.commit()

    return jsonify(movement.to_dict()), 201
