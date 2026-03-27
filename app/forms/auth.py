from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar Sesión")


class RegisterForm(FlaskForm):
    username = StringField(
        "Usuario",
        validators=[
            DataRequired(),
            Length(
                min=3, max=64, message="El usuario debe tener entre 3 y 64 caracteres"
            ),
        ],
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email("Ingresa un email válido")]
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            Length(min=6, message="La contraseña debe tener al menos 6 caracteres"),
        ],
    )
    confirm_password = PasswordField(
        "Confirmar Contraseña",
        validators=[
            DataRequired(),
            EqualTo("password", message="Las contraseñas deben coincidir"),
        ],
    )
    submit = SubmitField("Registrarse")
