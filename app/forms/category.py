from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(
                min=2, max=100, message="El nombre debe tener entre 2 y 100 caracteres"
            ),
        ],
    )
    description = TextAreaField(
        "Descripción",
        validators=[
            Length(max=500, message="La descripción no puede exceder 500 caracteres")
        ],
    )
    submit = SubmitField("Guardar")
