import flask
import flask_restful as fr
import flask_restful.reqparse as reqparse

from data import db_session
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)


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
        return flask.jsonify({"user": user.to_dict(only=("surname", "name", "age", "email", "position", "speciality", "id"))})

    def delete(self, user_id):
        abort_if_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return flask.jsonify({"success": "OK"})


class UsersListResource(fr.Resource):
    def get(self):
        dbs = db_session.create_session()
        users = dbs.query(User).all()
        return flask.jsonify({"users": [user.to_dict(only=("surname", "name", "age", "position", "speciality", "address", "email", "id")) for user in users]})

    def post(self):
        args = parser.parse_args()
        if not len(args.keys()) or any(key not in ["surname", "name", "age", "position", "speciality", "address", "email"]):
            return flask.make_response(flask.jsonify({"error": "Bad Request"}), 400)
        dbs = db_session.create_session()
        user = User(
            surname=args["surname"],
            name=args["name"],
            age=args["age"],
            position=args["position"],
            speciality=args["speciality"],
            address=args["address"],
            email=args["email"]
        )
        user.set_password(args["password"])
        dbs.add(user)
        dbs.commit()
        return flask.jsonify({"id": user.id})
