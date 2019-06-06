#!/usr/bin/env python
# project/api/views.py


from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import User
from project import db


users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()

    # handle empty request json
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

    # get data from response json
    username = post_data.get('username')
    email = post_data.get('email')

    try:
        user = User.query.filter_by(email=email).first()
        # handle request with correct data
        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': f'{email} was added!'
            }

            return jsonify(response_object), 201
        else:
            # handle request with existing email
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That email already exists.'
            }
            return jsonify(response_object), 400

    except exc.IntegrityError as e:
        # handling incomplete requests
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get single user details"""

    response_object = {
        'status': 'fail',
        'message': 'User does not exist.'
    }

    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404

@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    users = User.query.all()
    user_list = []
    for user in users:
        user_obj = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }
        user_list.append(user_obj)
    response_object = {
        'status': 'success',
        'data': {
            'users': user_list
        }
    }
    return jsonify(response_object), 200