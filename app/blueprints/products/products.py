from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app,
)
from flask_login import login_required
from app.extensions import db
from app.models import Product, Category
from app.forms import ProductForm

products = Blueprint("products", __name__, url_prefix="/products")


@products.route("/")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("ITEMS_PER_PAGE", 10)

    search = request.args.get("search", "")
    category_id = request.args.get("category", type=int)

    query = Product.query

    if search:
        query = query.filter(
            (Product.name.ilike(f"%{search}%")) | (Product.sku.ilike(f"%{search}%"))
        )

    if category_id:
        query = query.filter(Product.category_id == category_id)

    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    categories = Category.query.order_by(Category.name).all()

    return render_template(
        "products/index.html",
        products=products,
        categories=categories,
        search=search,
        selected_category=category_id,
    )


@products.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = ProductForm()

    categories = Category.query.order_by(Category.name).all()
    form.category_id.choices = [(0, "Seleccionar categoría")] + [
        (c.id, c.name) for c in categories
    ]

    if form.validate_on_submit():
        existing = Product.query.filter_by(sku=form.sku.data).first()
        if existing:
            flash("Ya existe un producto con ese SKU", "danger")
            return render_template("products/create.html", form=form)

        product = Product(
            sku=form.sku.data,
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            min_stock=form.min_stock.data,
            category_id=form.category_id.data if form.category_id.data != 0 else None,
            is_active=form.is_active.data,
        )

        db.session.add(product)
        db.session.commit()

        flash("Producto creado exitosamente", "success")
        return redirect(url_for("products.index"))

    return render_template("products/create.html", form=form)


@products.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)

    categories = Category.query.order_by(Category.name).all()
    form.category_id.choices = [(0, "Seleccionar categoría")] + [
        (c.id, c.name) for c in categories
    ]

    if form.validate_on_submit():
        existing = Product.query.filter(
            Product.sku == form.sku.data, Product.id != id
        ).first()

        if existing:
            flash("Ya existe un producto con ese SKU", "danger")
            return render_template("products/edit.html", form=form, product=product)

        product.sku = form.sku.data
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.min_stock = form.min_stock.data
        product.category_id = (
            form.category_id.data if form.category_id.data != 0 else None
        )
        product.is_active = form.is_active.data

        db.session.commit()

        flash("Producto actualizado exitosamente", "success")
        return redirect(url_for("products.index"))

    return render_template("products/edit.html", form=form, product=product)


@products.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    flash("Producto eliminado exitosamente", "success")
    return redirect(url_for("products.index"))
