from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Product

api_products = Blueprint("api_products", __name__, url_prefix="/api/products")


@api_products.route("", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


@api_products.route("", methods=["POST"])
def create_product():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["sku", "name", "price", "stock", "min_stock"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    existing = Product.query.filter_by(sku=data["sku"]).first()
    if existing:
        return jsonify({"error": "SKU already exists"}), 400

    product = Product(
        sku=data["sku"],
        name=data["name"],
        description=data.get("description", ""),
        price=data["price"],
        stock=data["stock"],
        min_stock=data["min_stock"],
        category_id=data.get("category_id"),
        is_active=data.get("is_active", True),
    )

    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


@api_products.route("/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict())


@api_products.route("/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "sku" in data:
        existing = Product.query.filter(
            Product.sku == data["sku"], Product.id != id
        ).first()
        if existing:
            return jsonify({"error": "SKU already exists"}), 400
        product.sku = data["sku"]

    if "name" in data:
        product.name = data["name"]
    if "description" in data:
        product.description = data["description"]
    if "price" in data:
        product.price = data["price"]
    if "stock" in data:
        product.stock = data["stock"]
    if "min_stock" in data:
        product.min_stock = data["min_stock"]
    if "category_id" in data:
        product.category_id = data["category_id"]
    if "is_active" in data:
        product.is_active = data["is_active"]

    db.session.commit()

    return jsonify(product.to_dict())


@api_products.route("/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"}), 200
