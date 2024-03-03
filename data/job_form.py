from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
import datetime


class JobForm(FlaskForm):
    team_leader = IntegerField("Id руководителя", validators=[DataRequired()])
    job = StringField("Название работы", validators=[DataRequired()])
    collaborators = StringField("Список id работников", validators=[DataRequired()])
    work_size = IntegerField("Длительность работы в часах")
    # start_date = DateTimeField("Время начала работы", default=datetime.datetime.now())
    # end_date = DateTimeField("Время окончания работы", default=datetime.datetime.now())
    is_finished = BooleanField("Выполнена ли работы", default=False)
    submit = SubmitField("Применить")