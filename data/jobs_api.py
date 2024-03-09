import flask
from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint("jobs_api", __name__, template_folder="templates")


@blueprint.route("/api/jobs")
def get_jobs():
    dbs = db_session.create_session()
    jobs = dbs.query(Jobs).all()
    return flask.jsonify({"jobs": [job.to_dict() for job in jobs]})