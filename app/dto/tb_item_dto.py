from app.models.tb_item import TbItem

class TbItemDTO:
    def __init__(self, tb_item):
        # 遍历 TbItem 模型的所有列并赋值
        for column in TbItem.__table__.columns:
            setattr(self, column.name, getattr(tb_item, column.name))

    def to_dict(self):
        # 返回包含所有属性的字典
        return {column.name: getattr(self, column.name) for column in TbItem.__table__.columns}