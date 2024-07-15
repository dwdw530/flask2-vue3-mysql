from app import db
from sqlalchemy.orm import relationship

class TbItem(db.Model):
    __tablename__ = 'tb_item'

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(255))
    category_id = db.Column(db.String(64),db.ForeignKey('tb_category.id'))
    category = relationship('TbCategory', back_populates='items')

    def __repr__(self):
        return f'<TbItem {self.name}>'
