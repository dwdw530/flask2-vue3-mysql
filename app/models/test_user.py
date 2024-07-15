from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class TestUser(db.Model):
    __tablename__ = 'test_user'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(100))
    pwd = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.pwd = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwd, password)

    def __repr__(self):
        return f'<TestUser {self.name}>'

