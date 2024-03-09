import flask
from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint("jobs_api", __name__, template_folder="templates")


@blueprint.route("/api/jobs")
def get_jobs():
    dbs = db_session.create_session()
    jobs = dbs.query(Jobs).all()
    return flask.jsonify({"jobs": [job.to_dict() for job in jobs]})


@blueprint.route("/api/jobs/<int:job_id>")
def get_job(job_id):
    dbs = db_session.create_session()
    job = dbs.query(Jobs).get(job_id)
    if not job:
        return flask.make_response(flask.jsonify({"error": "Not Found"}), 404)
    return flask.jsonify({"job": job.to_dict()})


@blueprint.route("/api/jobs", methods=["POST"])
def add_job():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({"error": "Empty Request"}), 400)
    elif not all(key in flask.request.json for key in ["team_leader", "job", "work_size", "collaborators", "is_finished"]):
        return flask.make_response(flask.jsonify({"error": "BadRequest"}), 400)
    dbs = db_session.create_session()
    job = Jobs(
        team_leader=flask.request.json["team_leader"],
        job=flask.request.json["job"],
        work_size=flask.request.json["work_size"],
        collaborators=flask.request.json["collaborators"],
        # start_date=flask.request.json["start_date"],
        # end_date=flask.request.json["end_date"],
        is_finished=flask.request.json["is_finished"]
    )
    dbs.add(job)
    dbs.commit()
    return flask.jsonify({"id": job.id})