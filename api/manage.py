#!/usr/bin/env python
# manage.py


from flask_script import Server, Manager
import unittest

from project import create_app, db
from project.api.models import User


app = create_app()
manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", port=3300))

@manager.command
def recreate_db():
    """Recreates a database"""
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def seed_db():
    """Seeds the database"""
    db.session.add(User(username="test_user_seed1", email="test.user.seed1@example.com"))
    db.session.add(User(username="test_user_seed2", email="test.user.seed2@example.com"))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
