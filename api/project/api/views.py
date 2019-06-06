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


