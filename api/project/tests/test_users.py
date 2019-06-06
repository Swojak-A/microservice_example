#!/usr/bin/env python
# project/tests/test_users.py


import json

from project import db
from project.tests.base import BaseTestCase
from project.api.models import User


# helper functions
def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user




class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure adding new user to db works properly."""
        response = self.client.post('/users',
                                    data=json.dumps(dict(
                                        username='test_user',
                                        email='test.user@example.com'
                                    )),
                                    content_type='application/json',
                                    )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('test.user@example.com was added!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error if the JSON object is empty"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Ensure error if the JSON object does not have a username key."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    email='test.user@example.com'
                )),
                content_type='application/json',)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_user(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post('/users',
                             data=json.dumps(dict(
                                 username='test_user',
                                 email='test.user@example.com'
                             )),
                             content_type='application/json',
                             )
            response = self.client.post('/users',
                                        data=json.dumps(dict(
                                            username='test_user',
                                            email='test.user@example.com'
                                        )),
                                        content_type='application/json',
                                        )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user works properly"""
        user = add_user(username='test_user', email='test.user@example.com')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('test_user', data['data']['username'])
            self.assertIn('test.user@example.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error if id not provided"""
        with self.client:
            response = self.client.get('/users/str-not-int')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error if it does not exist"""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all user works properly"""
        add_user('test_user1', 'test.user1@example.com')
        add_user('test_user2', 'test.user2@example.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertIn('test_user1', data['data']['users'][0]['username'])
            self.assertIn('test.user1@example.com', data['data']['users'][0]['email'])
            self.assertIn('test_user2', data['data']['users'][1]['username'])
            self.assertIn('test.user2@example.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])