from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app,
)
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Product, Movement
from app.forms import MovementForm

movements = Blueprint("movements", __name__, url_prefix="/movements")


@movements.route("/")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("ITEMS_PER_PAGE", 10)

    product_id = request.args.get("product", type=int)
    movement_type = request.args.get("type", "")

    query = Movement.query

    if product_id:
        query = query.filter(Movement.product_id == product_id)

    if movement_type:
        query = query.filter(Movement.movement_type == movement_type)

    movements = query.order_by(Movement.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    products = Product.query.filter_by(is_active=True).order_by(Product.name).all()

    return render_template(
        "movements/index.html",
        movements=movements,
        products=products,
        selected_product=product_id,
        selected_type=movement_type,
    )


@movements.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = MovementForm()

    products = Product.query.filter_by(is_active=True).order_by(Product.name).all()
    form.product_id.choices = [
        (p.id, f"{p.name} (SKU: {p.sku}) - Stock: {p.stock}") for p in products
    ]

    if form.validate_on_submit():
        product = Product.query.get(form.product_id.data)

        if not product:
            flash("Producto no encontrado", "danger")
            return render_template("movements/create.html", form=form)

        quantity = form.quantity.data

        if form.movement_type.data == "exit" and product.stock < quantity:
            flash(f"No hay suficiente stock. Stock actual: {product.stock}", "danger")
            return render_template("movements/create.html", form=form)

        movement = Movement(
            product_id=product.id,
            user_id=current_user.id,
            movement_type=form.movement_type.data,
            quantity=quantity,
            notes=form.notes.data,
        )

        if form.movement_type.data == "entry":
            product.stock += quantity
        else:
            product.stock -= quantity

        db.session.add(movement)
        db.session.commit()

        flash(
            f"Movimiento registrado: {form.movement_type.data.upper()} de {quantity} unidades",
            "success",
        )
        return redirect(url_for("movements.index"))

    return render_template("movements/create.html", form=form)
