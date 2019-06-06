#!/usr/bin/env python
# project/tests/test_config.py

import unittest
import os

from flask import current_app
from flask_testing import TestCase

from project import create_app


# variables
docker_build = True if os.environ.get("DOCKER_BUILD") else False

app = create_app()

# test cases
class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] == "my_precious")
        self.assertTrue(app.config['DEBUG'] is True)
        # self.assertTrue(current_app is None)
        if docker_build is True:
            self.assertTrue(app.config["SQLALCHEMY_DATABASE_URI"] == 'postgres://postgres:postgres@db:5432/users_dev')
        else:
            self.assertTrue(app.config["SQLALCHEMY_DATABASE_URI"] == 'postgres://postgres:postgres@0.0.0.0:5432/users_dev')



class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        if docker_build is True:
            self.assertTrue(app.config["SQLALCHEMY_DATABASE_URI"] == 'postgres://postgres:postgres@db:5432/users_tests')
        else:
            self.assertTrue(app.config["SQLALCHEMY_DATABASE_URI"] == 'postgres://postgres:postgres@0.0.0.0:5432/users_tests')


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()