from app import db
from sqlalchemy.orm import relationship

class TbCategory(db.Model):
    __tablename__ = 'tb_category'

    id = db.Column(db.String(64), primary_key=True)
    category_name = db.Column(db.String(255))
    items = relationship('TbItem', back_populates='category')

    def __repr__(self):
        return f'<TbCategory {self.name}>'

