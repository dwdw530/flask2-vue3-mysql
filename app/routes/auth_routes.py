import json

from flask import Blueprint, request, jsonify
from app.models import TestUser
from flask_jwt_extended import create_access_token
from app.services import UserService
from app import redis_client
from app.dto.user_dto import UserDTO

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    pwd = data.get('password')

    if not name or not email or not pwd:
        return jsonify({"message": "Missing required fields"}), 400

    if TestUser.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400
    new_user = UserService.register_user(name=name, email=email, password=pwd)

    access_token = create_access_token(identity=email)
    return jsonify({"token": access_token, "user": {"name": new_user['name'], "email": new_user['email']}}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    pwd = data.get('password')

    user = UserService.login_user(email=email, password=pwd)
    id = user.id
    if user and user.check_password(pwd):
        if(redis_client.get(f"user:{id}")):
            user_dto = redis_client.get(f"user:{id}")
        else:
            user_dto = UserDTO(user)
            user_json = json.dumps(user_dto.to_dict())
            redis_client.set(f"user:{id}", user_json, ex=60*60)
        access_token = create_access_token(identity=email)
        return jsonify({"token": access_token, "user": {"name": user.name, "email": user.email}}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
