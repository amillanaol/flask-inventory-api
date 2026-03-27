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
from app.models import Category
from app.forms import CategoryForm

categories = Blueprint("categories", __name__, url_prefix="/categories")


@categories.route("/")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("ITEMS_PER_PAGE", 10)

    search = request.args.get("search", "")

    query = Category.query

    if search:
        query = query.filter(Category.name.ilike(f"%{search}%"))

    categories = query.order_by(Category.name).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        "categories/index.html", categories=categories, search=search
    )


@categories.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = CategoryForm()

    if form.validate_on_submit():
        existing = Category.query.filter_by(name=form.name.data).first()
        if existing:
            flash("Ya existe una categoría con ese nombre", "danger")
            return render_template("categories/create.html", form=form)

        category = Category(name=form.name.data, description=form.description.data)

        db.session.add(category)
        db.session.commit()

        flash("Categoría creada exitosamente", "success")
        return redirect(url_for("categories.index"))

    return render_template("categories/create.html", form=form)


@categories.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)

    if form.validate_on_submit():
        existing = Category.query.filter(
            Category.name == form.name.data, Category.id != id
        ).first()

        if existing:
            flash("Ya existe una categoría con ese nombre", "danger")
            return render_template("categories/edit.html", form=form, category=category)

        category.name = form.name.data
        category.description = form.description.data

        db.session.commit()

        flash("Categoría actualizada exitosamente", "success")
        return redirect(url_for("categories.index"))

    return render_template("categories/edit.html", form=form, category=category)


@categories.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    category = Category.query.get_or_404(id)

    if category.products.count() > 0:
        flash("No se puede eliminar una categoría con productos asociados", "danger")
        return redirect(url_for("categories.index"))

    db.session.delete(category)
    db.session.commit()

    flash("Categoría eliminada exitosamente", "success")
    return redirect(url_for("categories.index"))
