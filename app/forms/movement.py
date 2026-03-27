from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class MovementForm(FlaskForm):
    product_id = SelectField("Producto", coerce=int, validators=[DataRequired()])
    movement_type = SelectField(
        "Tipo de Movimiento",
        choices=[("entry", "Entrada"), ("exit", "Salida")],
        validators=[DataRequired()],
    )
    quantity = IntegerField(
        "Cantidad",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="La cantidad debe ser mayor a 0"),
        ],
    )
    notes = TextAreaField("Notas", validators=[])
    submit = SubmitField("Registrar")
