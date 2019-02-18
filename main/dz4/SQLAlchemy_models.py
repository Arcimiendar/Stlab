from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Shop(Base):

    __tablename__ = 'shops'

    def __repr__(self):
        return f'Shop({self.name}, {self.address}, {self.staff_amount})'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String, nullable=True)
    staff_amount = Column(Integer)


class Department(Base):

    __tablename__ = 'departments'

    def __repr__(self):
        return f'Department({self.sphere}, {self.staff_amount})'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sphere = Column(String)
    staff_amount = Column(Integer)
    shop_id = Column(Integer, ForeignKey('shops.id'))


class Item(Base):

    __tablename__ = 'items'

    def __repr__(self):
        return f'Item({self.name}, {self.description}, {self.price})'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(Text, nullable=True)
    price = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.id'))
