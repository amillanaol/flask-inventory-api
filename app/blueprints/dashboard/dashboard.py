from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from app.extensions import db
from app.models import Product, Movement, Category

dashboard = Blueprint("dashboard", __name__, url_prefix="/")


@dashboard.route("/")
@dashboard.route("/dashboard")
@login_required
def index():
    total_products = Product.query.filter_by(is_active=True).count()

    low_stock_products = Product.query.filter(
        Product.is_active == True, Product.stock <= Product.min_stock
    ).count()

    recent_movements = (
        Movement.query.order_by(Movement.created_at.desc()).limit(5).all()
    )

    total_value = (
        db.session.query(func.sum(Product.stock * Product.price))
        .filter(Product.is_active == True)
        .scalar()
        or 0
    )

    total_categories = Category.query.count()
    total_stock = (
        db.session.query(func.sum(Product.stock))
        .filter(Product.is_active == True)
        .scalar()
        or 0
    )

    return render_template(
        "dashboard/index.html",
        total_products=total_products,
        low_stock_products=low_stock_products,
        recent_movements=recent_movements,
        total_value=total_value,
        total_categories=total_categories,
        total_stock=total_stock,
    )
