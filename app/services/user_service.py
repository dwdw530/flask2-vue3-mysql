import uuid

from app import db, app
from app.models.test_user import TestUser
from app.dto.user_dto import UserDTO


class UserService:
    @staticmethod
    def get_users(page, per_page):
        pagination = TestUser.query.paginate(page=page, per_page=per_page, error_out=False)
        test_users = pagination.items
        user_dtos = [UserDTO(user).to_dict() for user in test_users]
        return {
            'users': user_dtos,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        }

    @staticmethod
    def create_user(id, name, email):
        new_user = TestUser(id=id, name=name, email=email)
        try:
            with db.session.begin():
                db.session.add(new_user)
            return UserDTO(new_user).to_dict()
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error creating TestUser: {str(e)}")
            raise e

    @staticmethod
    def update_user(id, name, email):
        try:
            with db.session.begin():
                user = TestUser.query.get(id)
                if user:
                    user.name = name
                    user.email = email
                    return UserDTO(user).to_dict()
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error updating TestUser: {str(e)}")
            raise e

    @staticmethod
    def delete_user(id):
        try:
            with db.session.begin():
                user = TestUser.query.get(id)
                if user:
                    db.session.delete(user)
                    return True
                return False
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error deleting TestUser: {str(e)}")
            raise e


    @staticmethod
    def register_user(name, email, password):
        id = str(uuid.uuid4()).replace('-', '')
        new_user = TestUser(id=id, name=name, email=email)
        new_user.set_password(password)
        try:
            db.session.add(new_user)
            db.session.commit()
            user_dto = UserDTO(new_user)
            app.logger.info(f"UserDTO: {user_dto.to_dict()}")
            return user_dto.to_dict()
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error creating TestUser: {str(e)}")
            raise e

    @staticmethod
    def login_user(email, password):
        user = TestUser.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        else:
            return None
