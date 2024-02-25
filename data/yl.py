import sqlalchemy
import sqlalchemy.orm as orm
import datetime
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()
db_file = input()
global_init(db_file)
dbs = create_session()
colonists = dbs.query(User).filter(
    User.id.in_(int(i) for i in dbs.query(Department).filter(Department.id == 1).first().members.split(", ")))
jobs = dbs.query(Jobs).filter(Jobs.work_size > 25)
ids = list()
for job in jobs:
    ids.extend(int(i) for i in job.collaborators.split(", "))
ids = set(ids)
for col in colonists:
    if col.id in ids:
        print(col.surname, col.name)
