import flask
import flask_wtf
import wtforms
import sqlalchemy_serializer


class DepartmentForm(flask_wtf.FlaskForm, sqlalchemy_serializer.SerializerMixin):
    title = wtforms.StringField("Название департамента", validators=[wtforms.validators.DataRequired()])
    chief = wtforms.IntegerField("Id руководителя", validators=[wtforms.validators.DataRequired()])
    members = wtforms.StringField("Id работников департамента")
    email = wtforms.EmailField("Email департамента", validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField("Применить")