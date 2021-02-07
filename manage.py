# manage.py


import os
import unittest
import coverage
import random 

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/config.py',
        'project/server/*/__init__.py'
    ]
)
COV.start()

from project.server import app as application, db
from project.server.models.User import User
from project.server.models.Subscriber import Subscriber
from project.server.models.Donor import Donor
from project.server.models.Hospital import Hospital
from project.server.models.Transfusion import Transfusion
from project.server.models.Donation import Donation
from project.server.models.Deferral import Deferral
from project.server import generate_data

migrate = Migrate(application, db)
application = manager = Manager(application)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def populate_db():
    hospital_ids = []
    sub_ids = []
    don_ids = []
    for _ in range(5):
         hospital_ids.append(generate_data.hospital())
    for _ in range(random.randint(10, 15)):
        if len(don_ids) > 0:
            don_ids.append(generate_data.donor(random.choice(don_ids), random.choice(hospital_ids)))
        else:
            don_ids.append(generate_data.donor(None, random.choice(hospital_ids)))
    for _ in range(random.randint(10, 15)):
        sub_ids.append(generate_data.subscriber(random.choice(hospital_ids)))
    for _ in range(random.randint(3, 7)):
        generate_data.transfusion(random.choice(hospital_ids), random.choice(sub_ids))
    for _ in range(random.randint(50, 80)):
        generate_data.donation(random.choice(hospital_ids), random.choice(don_ids))
    for _ in range(random.randint(2, 5)):
        generate_data.defferal(random.choice(don_ids))

@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()

@manager.command
def add_super_admin():
    """Adds first admin here"""
    email = "tafodinho@gmail.com"
    name = "Tafang Joshua"
    password = "Hacker@101"

    user = User(
                    email=email,
                    name=name,
                    password=password,
                    admin=True
                )
    db.session.add(user)
    db.session.commit()
    

@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()

if __name__ == '__main__':
    manager.run(host='0.0.0.0')
