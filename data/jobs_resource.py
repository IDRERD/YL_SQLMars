import flask
import flask_restful as fr
import flask_restful.reqparse as reqparse

from data import db_session
from data.jobs import Jobs

parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('collaborators', required=True)
parser.add_argument('start_date', required=False)
parser.add_argument('end_date', required=False)


def abort_if_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        fr.abort(404, message=f"Job {job_id} not found")


class JobsResource(fr.Resource):
    def get(self, job_id):
        abort_if_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return flask.jsonify({"job": job.to_dict()})

    def delete(self, job_id):
        abort_if_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return flask.jsonify({"success": "OK"})


class JobsListResource(fr.Resource):
    def get(self):
        dbs = db_session.create_session()
        jobs = dbs.query(Jobs).all()
        return flask.jsonify({"jobs": [job.to_dict() for job in jobs]})

    def post(self):
        args = parser.parse_args()
        if not len(args.keys()):
            return flask.male_response(flask.jsonify({"error": "Bad Request"}), 400)
        dbs = db_session.create_session()
        job = Jobs(
            team_leader=args["team_leader"],
            job=args["job"],
            work_size=args["work_size"],
            collaborators=args["collaborators"],
            is_finished=args["speciality"]
        )
        job.set_password(args["password"])
        dbs.add(job)
        dbs.commit()
        return flask.jsonify({"id": job.id})