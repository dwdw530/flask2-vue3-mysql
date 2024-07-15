from flask import Blueprint, jsonify, request
from app.services.user_service import UserService

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
