from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    IntegerField,
    SelectField,
    BooleanField,
    SubmitField,
)
from wtforms.validators import DataRequired, NumberRange, Length, Optional


class ProductForm(FlaskForm):
    sku = StringField(
        "SKU",
        validators=[
            DataRequired(),
            Length(min=1, max=50, message="El SKU debe tener entre 1 y 50 caracteres"),
        ],
    )
    name = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(
                min=2, max=200, message="El nombre debe tener entre 2 y 200 caracteres"
            ),
        ],
    )
    description = TextAreaField(
        "Descripción",
        validators=[
            Length(max=1000, message="La descripción no puede exceder 1000 caracteres")
        ],
    )
    price = DecimalField(
        "Precio",
        validators=[
            DataRequired(),
            NumberRange(min=0, message="El precio debe ser mayor o igual a 0"),
        ],
    )
    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(),
            NumberRange(min=0, message="El stock debe ser mayor o igual a 0"),
        ],
    )
    min_stock = IntegerField(
        "Stock Mínimo",
        validators=[
            DataRequired(),
            NumberRange(min=0, message="El stock mínimo debe ser mayor o igual a 0"),
        ],
    )
    category_id = SelectField("Categoría", coerce=int, validators=[Optional()])
    is_active = BooleanField("Activo")
    submit = SubmitField("Guardar")
