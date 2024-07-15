from app.models.test_user import TestUser

class UserDTO:
    def __init__(self, test_user):
        for column in TestUser.__table__.columns:
            setattr(self, column.name, getattr(test_user, column.name))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in TestUser.__table__.columns}