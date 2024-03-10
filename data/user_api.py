import flask
from data import db_session
from data.users import User

blueprint = flask.Blueprint("user_api", __name__, template_folder="templates")


@blueprint.route("/api/users")
def get_users():
    dbs = db_session.create_session()
    users = dbs.query(User).all()
    return flask.jsonify({"users": [user.to_dict() for user in users]})


@blueprint.route("/api/users/<int:user_id>")
def get_user(user_id):
    dbs = db_session.create_session()
    user = dbs.query(User).get(user_id)
    if not user:
        return flask.make_response(flask.jsonify({"error": "Not Found"}), 404)
    return flask.jsonify({"user": user.to_dict()})


@blueprint.route("/api/users", methods=["POST"])
def add_user():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({"error": "Empty Request"}), 400)
    elif not all(key in flask.request.json for key in ["surname", "name", "age", "position", "speciality", "address", "email", "password"]):
        return flask.make_response(flask.jsonify({"error": "BadRequest"}), 400)
    dbs = db_session.create_session()
    user = User(
        surname=flask.request.json["surname"],
        name=flask.request.json["name"],
        age=flask.request.json["age"],
        position=flask.request.json["position"],
        speciality=flask.request.json["speciality"],
        address=flask.request.json["address"],
        email=flask.request.json["email"]
    )
    user.set_password(flask.request.json["password"])
    dbs.add(user)
    dbs.commit()
    return flask.jsonify({"id": user.id})


@blueprint.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    dbs = db_session.create_session()
    user = dbs.query(User).get(user_id)
    if not user:
        return flask.make_response(flask.jsonify({"error": "Not Found"}), 404)
    dbs.delete(user)
    dbs.commit()
    return flask.jsonify({"success": "OK"})


@blueprint.route("/api/users/<int:user_id>", methods=["POST"])
def edit_user(user_id):
    dbs = db_session.create_session()
    user = dbs.query(User).get(user_id)
    if not user:
        return flask.make_response(flask.jsonify({"error": "Not Found"}), 404)
    for key in flask.request.json.keys():
        if key == "surname":
            user.surname = flask.request.json[key]
        if key == "name":
            user.name = flask.request.json[key]
        if key == "age":
            user.age = flask.request.json[key]
        if key == "position":
            user.position = flask.request.json[key]
        if key == "speciality":
            user.speciality = flask.request.json[key]
        if key == "address":
            user.address = flask.request.json[key]
        if key == "email":
            user.email = flask.request.json[key]
        if key == "password":
            user.set_password(flask.request.json[key])
    dbs.commit()
    return flask.jsonify({"success": "OK"})