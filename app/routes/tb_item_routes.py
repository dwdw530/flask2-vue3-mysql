from flask import Blueprint,jsonify, request

from app.models import TbItem
from app.services import TbItemService
from app.queryParams import TbItemQueryDTO
from flask_jwt_extended import jwt_required

tb_item_bp = Blueprint('tb_item_bp', __name__)

@tb_item_bp.route('/tb_items/queryPage', methods=['POST'])
def get_tb_items():
    # 从请求的 JSON 数据中获取 page、per_page 和 other_data
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    other_data = data.get('other_data', {})  # 假设 other_data 是一个对象，如果不存在，则默认为一个空字典

    # 创建一个 TbItemQueryDTO 对象
    query_dto = TbItemQueryDTO(page, per_page, other_data)

    # 将 TbItemQueryDTO 对象传递给 TbItemService.get_tb_items 方法
    result = TbItemService.get_tb_items(query_dto)

    return jsonify(result)

@tb_item_bp.route('/tb_items/category_name', methods=['POST'])
def get_tb_items_by_category_name():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    category_name = data.get('other_data', {})

    query_dto = TbItemQueryDTO(page, per_page, category_name)

    result = TbItemService.get_items_with_categories(query_dto)

    return jsonify(result)

@tb_item_bp.route('/tb_items/category_name2', methods=['POST'])
def get_tb_items_by_category_name2():
    data = request.get_json()
    page = data.get('page', 1)
    per_page = data.get('per_page', 10)
    category_name = data.get('other_data', {})

    query_dto = TbItemQueryDTO(page, per_page, category_name)

    result = TbItemService.get_items_with_categories_raw_sql(query_dto)

    return jsonify(result)


@tb_item_bp.route('/tb_items', methods=['POST'])
def create_tb_item():
    data = request.get_json()
    new_tb_item = TbItemService.create_tb_item(data['name'], data['category_id'])
    return jsonify({'message': 'Item created successfully!', 'tb_item': new_tb_item}), 201

@tb_item_bp.route('/tb_items/<id>', methods=['PUT'])
def update_tb_item(id):
    data = request.get_json()
    updated_tb_item = TbItemService.update_tb_item(id, data['name'])
    if updated_tb_item:
        return jsonify({'message': 'Item updated successfully!', 'tb_item': updated_tb_item})
    else:
        return jsonify({'message': 'Item not found'}), 404

@tb_item_bp.route('/tb_items/<id>', methods=['DELETE'])
def delete_tb_item(id):
    success = TbItemService.delete_tb_item(id)
    if success:
        return jsonify({'message': 'Item deleted successfully!'})
    else:
        return jsonify({'message': 'Item not found'}), 404


# 获取商品订单列表
@tb_item_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    items = TbItem.query.all()
    items_list = [{"id": item.id, "name": item.name, "price": item.price} for item in items]
    return jsonify({"orders": items_list}), 200
