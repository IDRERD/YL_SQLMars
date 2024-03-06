import flask
import flask_restful as fr

from data import db_session
from data.users import User


def abort_if_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        fr.abort(404, message=f"User {user_id} not found")


class UsersResource(fr.Resource):
    def get(self, user_id):
        abort_if_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return flask.jsonify({"user": user.to_dict(only=("surname", "name", "age", "email", "position", "speciality"))})

    def delete(self, user_id):
        abort_if_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return flask.jsonify({"success": "OK"})