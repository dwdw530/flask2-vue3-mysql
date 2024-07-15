import json

from flask import Blueprint, jsonify, request
from app.services.user_service import UserService
from app import redis_client

test_user_bp = Blueprint('test_user_bp', __name__)


@test_user_bp.route('/test_users', methods=['GET'])
def get_test_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    result = UserService.get_users(page, per_page)
    return jsonify(result)

@test_user_bp.route('/test_users', methods=['POST'])
def create_test_user():
    data = request.get_json()
    new_user = UserService.create_user(data['id'], data['name'])
    return jsonify({'message': 'User created successfully!', 'user': new_user}), 201

@test_user_bp.route('/test_users/<id>', methods=['PUT'])
def update_test_user(id):
    data = request.get_json()
    updated_user = UserService.update_user(id, data['name'])
    if updated_user:
        return jsonify({'message': 'User updated successfully!', 'user': updated_user})
    else:
        return jsonify({'message': 'User not found'}), 404

@test_user_bp.route('/test_users/<id>', methods=['DELETE'])
def delete_test_user(id):
    success = UserService.delete_user(id)
    if success:
        return jsonify({'message': 'User deleted successfully!'})
    else:
        return jsonify({'message': 'User not found'}), 404

@test_user_bp.route('/test_users/<id>', methods=['GET'])
def get_test_user(id):
    try:
        user_dto = redis_client.get(f"user:{id}")
        user_json = user_dto.decode('utf-8')  # 解码为字符串
        if user_json:
            user_dict = json.loads(user_json)  # 将 JSON 字符串解析为字典
            user_dict.pop('pwd', None)
            return jsonify(user_dict), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500