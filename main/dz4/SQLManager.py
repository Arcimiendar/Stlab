from settings import USERNAME, PASSWORD, DBNAME, HOST
# note: there is additional information to connect to database
# define fields with the same names to connect to database
from psycopg2 import connect


class SQLManager:
    def __init__(self):
        self.connection = connect(dbname=DBNAME, user=USERNAME,
                                  password=PASSWORD, host=HOST)

    def __delete__(self, instance):
        self.connection.close()

    def create_tables(self):

        with self.connection.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE Shops
                (id SERIAL,
                name VARCHAR(256) NOT NULL,
                address VARCHAR(256) NULL,
                staff_amount INTEGER,
                PRIMARY KEY (id));
            """)

            cursor.execute("""
                CREATE TABLE Departments
                (id SERIAL,
                sphere VARCHAR(256),
                staff_amount INTEGER,
                shop_id INTEGER,
                PRIMARY KEY (id),
                FOREIGN KEY(shop_id) REFERENCES shops(id));
            """)

            cursor.execute("""
                CREATE TABLE Items
                (id SERIAL,
                name VARCHAR(256),
                description TEXT NULL,
                price INTEGER,
                department_id INTEGER,
                PRIMARY KEY (id),
                FOREIGN KEY (department_id) REFERENCES Departments(id));
            """)

        self.connection.commit()

    def drop_tables(self):

        with self.connection.cursor() as cursor:

            cursor.execute("""
            DROP TABLE items;
            DROP TABLE departments;
            DROP TABLE shops
            """)

        self.connection.commit()

    def insert_data(self):

        with self.connection.cursor() as cursor:

            cursor.execute("""
                INSERT INTO shops (name, address, staff_amount)
                VALUES 
                ('Auchan', NULL, 250), 
                ('IKEA', 'Street Žirnių g. 56, Vilnius, Lithuania.', 500)
            """)

            cursor.execute("""
                INSERT INTO departments (sphere, staff_amount, shop_id)
                VALUES 
                ('Furniture', 250, 1), 
                ('Furniture', 300, 2),
                ('Dishes',    200, 2)
            """)

            cursor.execute("""
                INSERT INTO items (name, description, price, department_id)
                VALUES 
                ('Table', 'Cheap wooden table', 300, 1), 
                ('Table', NULL, 750, 2), 
                ('Bed', 'Amazing wooden bed', 1200, 2),
                ('Cup', NULL, 10, 3),
                ('Plate', 'Glass plate', 20, 3)
            """)

        self.connection.commit()

    def update_data(self):

        with self.connection.cursor() as cursor:

            cursor.execute("""
                UPDATE items
                SET price = price + 100
                WHERE name ILIKE 'b%' OR name ILIKE '%e'
            """)

        self.connection.commit()

    def delete_data(self, mode: int):

        with self.connection.cursor() as cursor:

            if mode == 1:
                cursor.execute("""
                    DELETE FROM items
                    WHERE price > 500 OR description ISNULL
                """)
            elif mode == 2:
                cursor.execute("""
                    DELETE FROM items i
                    USING departments d, shops s 
                    WHERE i.department_id = d.id 
                    AND d.shop_id = s.id AND  s.address ISNULL 
                """)
            elif mode == 3:
                cursor.execute("""
                    DELETE FROM items i
                    USING departments d
                    WHERE i.department_id = d.id
                    AND 225 < d.staff_amount AND d.staff_amount < 275
                """)
            elif mode == 4:
                cursor.execute("""
                    DELETE FROM items 
                    WHERE TRUE;
                    
                    DELETE FROM departments
                    WHERE TRUE;
                    
                    DELETE FROM shops
                    WHERE TRUE;
                """)

        self.connection.commit()

    def select_data(self, mode: int):
        with self.connection.cursor() as cursor:
            if mode == 1:
                cursor.execute("""
                   SELECT * FROM items
                   WHERE description NOTNULL 
                """)
            elif mode == 2:
                cursor.execute("""
                    SELECT DISTINCT d.sphere 
                    FROM departments d
                    RIGHT JOIN items i on d.id = i.department_id
                    WHERE d.staff_amount > 200
                """)
            elif mode == 3:
                cursor.execute("""
                    SELECT address FROM shops
                    WHERE name ILIKE 'i%'
                """)
            elif mode == 4:
                cursor.execute("""
                    SELECT i.name
                    FROM items i, departments d
                    WHERE d.id = i.department_id  and  d.sphere ILIKE 'furniture'           
                """)
            elif mode == 5:
                cursor.execute("""
                    SELECT s.name 
                    FROM shops s, departments d, items i 
                    WHERE i.description NOTNULL 
                    AND i.department_id = d.id 
                    AND d.shop_id = s.id
                """)
            elif mode == 6:
                cursor.execute("""
                    SELECT i.name, i.description, i.price, 
                           d.sphere AS department_sphere,
                           d.staff_amount AS department_staff_amount,
                           s.name AS shop_name, 
                           s.staff_amount AS shop_staff_amount
                            
                    FROM items i
                    LEFT JOIN departments d ON i.department_id = d.id
                    LEFT JOIN shops s ON d.shop_id = s.id              
                """)
            elif mode == 7:
                cursor.execute("""
                    SELECT name FROM items 
                    ORDER BY name
                    OFFSET 2
                    LIMIT 2    
                """)
            elif mode == 8:
                cursor.execute("""
                    SELECT i.name, d.sphere
                    FROM items i
                    INNER JOIN departments d on i.department_id = d.id
                """)
            elif mode == 9:
                cursor.execute("""
                    SELECT i.name, d.sphere 
                    FROM items i 
                    LEFT JOIN departments d on i.department_id = d.id
                """)
            elif mode == 10:
                cursor.execute("""
                    SELECT i.name, d.sphere
                    FROM items i 
                    RIGHT JOIN departments d on i.department_id = d.id
                """)
            elif mode == 11:
                cursor.execute("""
                    SELECT i.name, d.sphere
                    FROM items i
                    FULL JOIN departments d on i.department_id = d.id
                """)
            elif mode == 12:
                cursor.execute("""
                    SELECT i.name, d.sphere
                    FROM items i
                    CROSS JOIN departments d 
                """)
            elif mode == 13:
                cursor.execute("""
                    SELECT count(i), sum(i.price), max(i.price),
                    min(i.price), avg(i.price)
                    FROM shops s  
                    LEFT JOIN departments d on s.id = d.shop_id
                    LEFT JOIN items i on d.id = i.department_id
                    GROUP BY shop_id
                    HAVING count(i) > 1
                """)
            elif mode == 14:
                cursor.execute("""
                    SELECT s.name, array_agg(i.name)
                    FROM shops s
                    LEFT JOIN departments d on s.id = d.shop_id
                    LEFT JOIN items i on d.id = i.department_id
                    GROUP BY s.name
                """)

            selected_data = cursor.fetchall()

        return selected_data
