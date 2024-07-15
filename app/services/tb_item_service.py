import uuid

from app import db, app
from sqlalchemy import text
from app.models.tb_item import TbItem
from app.models.tb_category import TbCategory
from app.dto.tb_item_dto import TbItemDTO

class TbItemService:
    @staticmethod
    def get_tb_items(query_dto):
        # 初始查询
        query = TbItem.query

        # 检查并处理 other_data 中的 id 和 name
        if 'id' in query_dto.other_data and query_dto.other_data['id']:
            query = query.filter(TbItem.id == query_dto.other_data['id'])

        if 'name' in query_dto.other_data and query_dto.other_data['name']:
            query = query.filter(TbItem.name.like(f"%{query_dto.other_data['name']}%"))

        # 使用 query_dto.page 和 query_dto.per_page 替代原来的 page 和 per_page
        pagination = query.paginate(page=query_dto.page, per_page=query_dto.per_page, error_out=False)
        tb_items = pagination.items
        tb_item_dtos = [TbItemDTO(tb_item).to_dict() for tb_item in tb_items]

        return {
            'tb_items': tb_item_dtos,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        }

    @staticmethod
    def get_items_with_categories(query_dto):
        query = db.session.query(TbItem).join(TbCategory)

        if 'id' in query_dto.other_data and query_dto.other_data['id']:
            query = query.filter(TbItem.id == query_dto.other_data['id'])

        if 'name' in query_dto.other_data and query_dto.other_data['name']:
            query = query.filter(TbItem.name.like(f"%{query_dto.other_data['name']}%"))

        if 'category_name' in query_dto.other_data and query_dto.other_data['category_name']:
            query = query.filter(TbCategory.category_name.like(f"%{query_dto.other_data['category_name']}%"))

        total = query.count()
        tb_items = query.offset((query_dto.page - 1) * query_dto.per_page).limit(query_dto.per_page).all()
        tb_item_dtos = [
            {
                'id': tb_item.id,
                'name': tb_item.name,
                'category': tb_item.category.category_name
            }
            for tb_item in tb_items
        ]

        return {
            'tb_items': tb_item_dtos,
            'total': total,
            'pages': (total + query_dto.per_page - 1) // query_dto.per_page,
            'current_page': query_dto.page
        }

    @staticmethod
    def get_items_with_categories_raw_sql(query_dto):
        sql = text("""
            SELECT t1.id, t1.name, t2.category_name
            FROM tb_item t1
            JOIN tb_category t2 ON t1.category_id = t2.id
            WHERE 1=1
        """)

        if 'id' in query_dto.other_data and query_dto.other_data['id']:
            sql = sql + text(" AND t1.id = :id")
        if 'name' in query_dto.other_data and query_dto.other_data['name']:
            sql = sql + text(" AND t1.name LIKE :name")
        if 'category_name' in query_dto.other_data and query_dto.other_data['category_name']:
            sql = sql + text(" AND t2.category_name LIKE :category_name")

        # 添加分页
        sql = sql + text(" LIMIT :limit OFFSET :offset")

        params = {
            'id': query_dto.other_data.get('id'),
            'name': f"%{query_dto.other_data.get('name')}%" if query_dto.other_data.get('name') else None,
            'category_name': f"%{query_dto.other_data.get('category_name')}%" if query_dto.other_data.get('category_name') else None,
            'limit': query_dto.per_page,
            'offset': (query_dto.page - 1) * query_dto.per_page
        }

        result = db.session.execute(sql, params).fetchall()
        tb_items = [{'id': row['id'], 'name': row['name'], 'category': row['category_name']} for row in result]

        # 这里简单处理分页信息
        total = db.session.execute(text("SELECT COUNT(*) FROM tb_item")).scalar()

        return {
            'tb_items': tb_items,
            'total': total,
            'pages': (total + query_dto.per_page - 1) // query_dto.per_page,
            'current_page': query_dto.page
        }

    @staticmethod
    def create_tb_item(name,category_id):
        try:
            with db.session.begin():
                id = str(uuid.uuid4()).replace('-', '')
                new_tb_item = TbItem(id=id, name=name, category_id=category_id)
                db.session.add(new_tb_item)
            return TbItemDTO(new_tb_item).to_dict()
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error creating TbItem: {str(e)}")
            raise e

    @staticmethod
    def update_tb_item(id, name):
        try:
            with db.session.begin():
                tb_item = TbItem.query.get(id)
                if tb_item:
                    tb_item.name = name
                    return TbItemDTO(tb_item).to_dict()
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error updating TbItem: {str(e)}")
            raise e

    @staticmethod
    def delete_tb_item(id):
        try:
            with db.session.begin():
                tb_item = TbItem.query.get(id)
                if tb_item:
                    db.session.delete(tb_item)
                    return True
                return False
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error deleting TbItem: {str(e)}")
            raise e
