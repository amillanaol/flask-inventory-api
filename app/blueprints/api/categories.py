from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Category

api_categories = Blueprint("api_categories", __name__, url_prefix="/api/categories")


@api_categories.route("", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])


@api_categories.route("", methods=["POST"])
def create_category():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing field: name"}), 400

    existing = Category.query.filter_by(name=data["name"]).first()
    if existing:
        return jsonify({"error": "Category name already exists"}), 400

    category = Category(name=data["name"], description=data.get("description", ""))

    db.session.add(category)
    db.session.commit()

    return jsonify(category.to_dict()), 201


@api_categories.route("/<int:id>", methods=["GET"])
def get_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(category.to_dict())


@api_categories.route("/<int:id>", methods=["PUT"])
def update_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "name" in data:
        existing = Category.query.filter(
            Category.name == data["name"], Category.id != id
        ).first()
        if existing:
            return jsonify({"error": "Category name already exists"}), 400
        category.name = data["name"]

    if "description" in data:
        category.description = data["description"]

    db.session.commit()

    return jsonify(category.to_dict())


@api_categories.route("/<int:id>", methods=["DELETE"])
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    if category.products.count() > 0:
        return jsonify(
            {"error": "Cannot delete category with associated products"}
        ), 400

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category deleted successfully"}), 200
