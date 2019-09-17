from sqlalchemy import create_engine, or_, delete, and_, select, func, literal
from sqlalchemy.orm import sessionmaker, join

from settings import USERNAME, PASSWORD, DBNAME, HOST
# note: there is additional information to connect to database
# define fields with the same names to connect to database
from SQLAlchemy_models import Shop, Item, Department, Base


class AlchemyManager:

    def __init__(self):

        connection_data = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:5432/{DBNAME}'
        self.engine = create_engine(connection_data)

        self.session = sessionmaker(bind=self.engine)()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Item.__table__.drop(self.engine)
        Department.__table__.drop(self.engine)
        Shop.__table__.drop(self.engine)

    def insert_data(self):

        self.session.add_all(
            [
                Shop(name='Auchan', address=None, staff_amount=250),
                Shop(name='IKEA', address='Street Žirnių g. 56, Vilnius, Lithuania.',
                     staff_amount=500)
            ]
        )
        self.session.commit()

        self.session.add_all(
            [
                Department(sphere='Furniture', staff_amount=250, shop_id=1),
                Department(sphere='Furniture', staff_amount=300, shop_id=2),
                Department(sphere='Dishes', staff_amount=200, shop_id=2)
            ]
        )
        self.session.commit()

        self.session.add_all(
            [
                Item(name='Table', description='Cheap wooden table', price='300', department_id=1),
                Item(name='Table', description=None, price='750', department_id=2),
                Item(name='Bed', description='Amazing wooden bed', price='1200', department_id=2),
                Item(name='Cuo', description=None, price='10', department_id=3),
                Item(name='Plate', description='Glass plate', price='20', department_id=3)
            ]
        )
        self.session.commit()

    def update_data(self):
        query = self.session.query(Item)\
            .filter(or_(Item.name.ilike("%e"), Item.name.ilike("b%")))

        for item in query:
            item.price += 100

        self.session.commit()

    def delete_data(self, mode: int):

        if mode == 1:
            self.session.execute(
                delete(Item).where(or_(Item.price > 500, Item.description == None))
            )
        elif mode == 2:
            self.session.execute(
                delete(Item).where(and_(
                    Item.department_id == Department.id, Shop.id == Department.shop_id,
                    Shop.address == None))
            )
        elif mode == 3:
            self.session.execute(
                delete(Item).where(and_(
                    Item.department_id == Department.id,
                    Department.staff_amount < 275, Department.staff_amount > 225))
            )
        elif mode == 4:
            self.session.execute(delete(Item))
            self.session.execute(delete(Department))
            self.session.execute(delete(Shop))

        self.session.commit()

    def select_data(self, mode: int):

        if mode == 1:
            return [item.__repr__() for item in
                    self.session.execute(select(['*'])
                                         .where(Item.description != None)).fetchall()]
        elif mode == 2:
            return [department.sphere for department in self.session.query(Department)]
        elif mode == 3:
            return [item.__repr__() for item in
                    self.session.execute(select([Shop.name])
                                         .where(Shop.name.ilike("i%"))).fetchall()]
        elif mode == 4:
            return list(self.session.query(Item)
                        .filter(and_(Item.department_id == Department.id,
                                     Department.sphere == 'Furniture')))
        elif mode == 5:
            return list(self.session.query(Shop).filter(
                and_(Department.shop_id == Shop.id,
                     and_(Item.department_id == Department.id, Item.description != None))
            ))
        elif mode == 6:
            return self.session.query(Item, Department, Shop).join(Department).join(Shop).all()
        elif mode == 7:
            return self.session.query(Item).order_by(Item.name).offset(2).limit(2).all()
        elif mode == 8:
            return self.session.query(Item, Department).filter(and_(
                Department.id == Item.department_id, Item.department_id == Department.id).all())
        elif mode == 9:
            return self.session.query(Item, Department).join(Department).all()
        elif mode == 10:
            return self.session.query(Department, Item).join(Item).all()
        elif mode == 11:
            return self.session.query(Item, Department).join(Department, full=True).all()
        elif mode == 12:
            return self.session.query(Item, Department).join(Department, literal(True)).all()
        elif mode == 13:
            return self.session.execute(
                select([func.count(Item.id), func.sum(Item.price), func.max(Item.price),
                        func.min(Item.price), func.avg(Item.price)])
                .select_from(join(Shop, join(Department, Item)))
                .group_by(Shop.id).having(func.count(Item.id) > 1)
            ).fetchall()
        elif mode == 14:
            return [data for data in
                    self.session.execute(
                        select([Shop.name, func.array_agg(Item.name)])
                        .select_from(join(Item, join(Department, Shop))).group_by(Shop.name))]
