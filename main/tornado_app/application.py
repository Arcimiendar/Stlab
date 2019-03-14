from psycopg2 import connect, ProgrammingError

import tornado.web as web
import tornado.websocket as websocket
import tornado.ioloop as ioloop
from tornado.log import enable_pretty_logging

from typing import *
import re


DBNAME = ""  # put there name of database
USERNAME = ""  # put there username
PASSWORD = ""  # password
HOST = ""  # host


def init_database():

    connection = connect(dbname=DBNAME, user=USERNAME,
                         password=PASSWORD, host=HOST)

    with connection.cursor() as cursor:

        try:
            cursor.execute("""
                CREATE TABLE messages
                (id SERIAL,
                name VARCHAR(128) NOT NULL, 
                message VARCHAR(1024) NOT NULL,
                room INTEGER NOT NULL,
                PRIMARY KEY (id))
            """)
        except ProgrammingError:
            pass

    connection.commit()
    connection.close()


class Room(web.RequestHandler):
    def get(self, room_number: str, name: str):
        if name.lower() == 'admin' and room_number == "11":
            self.render("templates/admin.html")
        else:
            self.render("templates/messenger.html")

    def post(self, room_number: str, name: str):

        type_submit = self.get_argument('type_submit')

        room = self.get_argument('number')

        if type_submit == "clear":

            connection = connect(dbname=DBNAME, user=USERNAME,
                                 password=PASSWORD, host=HOST)

            with connection.cursor() as cursor:

                cursor.execute(f"""
                    DELETE FROM messages
                    WHERE room={room}   
                """)

                connection.commit()

            connection.close()

            for user in RoomSocket.rooms[int(room) - 1]:
                user.on_message('get messages')

        elif type_submit == 'restart':

            for user in RoomSocket.rooms[int(room) - 1]:
                user.write_message("disconnect")

        self.render('templates/admin.html')


class RoomSocket(websocket.WebSocketHandler):
    rooms: List[Set['RoomSocket']] = [set() for i in range(10)]

    def open(self, room_number, name):

        self._connecion = connect(dbname=DBNAME, user=USERNAME,
                                  password=PASSWORD, host=HOST)
        self._name = name
        self._room_number = int(room_number)

        RoomSocket.rooms[self._room_number - 1].add(self)
        self.update_online()
        self.on_message('get messages')

    def on_close(self):
        self._connecion.close()
        RoomSocket.rooms[self._room_number - 1].remove(self)
        self.update_online()

    def on_message(self, message: Union[str, bytes]):

        if message.startswith("message=") or message == 'get messages':

            with self._connecion.cursor() as cursor:

                if message != 'get messages':
                    message = message[8:]

                    cursor.execute(f"""
                        INSERT INTO messages (name, message, room)
                        VALUES (\'{self._name}\', \'{message}\', {self._room_number})
                    """)

                cursor.execute(f"""
                    SELECT name, message FROM messages
                    WHERE room={self._room_number}
                    ORDER BY id
                """)

                messages = cursor.fetchall()

            self._connecion.commit()

            response = 'messages: <br>'

            for message in messages:
                response += f'{message[0]} said: {message[1]} <br>'

            for user in RoomSocket.rooms[self._room_number - 1]:
                user.write_message(response)

    def __get_online(self) -> str:

        message = 'online: <br>'

        names_in_row = 0
        for user in RoomSocket.rooms[self._room_number - 1]:
            names_in_row += 1
            message += f'{user._name}, '

            if names_in_row == 6:
                names_in_row = 0
                message += '<br>'

        return message

    def update_online(self) -> None:
        online = self.__get_online()
        for user in RoomSocket.rooms[self._room_number - 1]:
            user.write_message(online)


class MainPage(web.RequestHandler):
    def get(self):
        self.render("templates/index.html")

    def post(self):

        try:
            name_to_check = self.get_body_argument("name_to_check")
            room_number = int(self.get_body_argument('number'))

            if name_to_check == 'admin' and room_number == 11:
                self.write("true")
                return

            if re.match(r"\w+", name_to_check).group(0) != name_to_check:
                self.write("name is note valid. Please, use another.")
                return

            for user in RoomSocket.rooms[room_number - 1]:
                if name_to_check == user._name:
                    self.write("name is already used. Please, chose another one")
                    return
            self.write("true")
            return
        except web.MissingArgumentError:
            name = self.get_argument("name")
            number = self.get_argument("number")
            self.redirect(f'/{number}/{name}/')
            pass


def make_app():
    return web.Application([
        (r'/', MainPage),
        (r'/(\d+)/(\w+)/', Room),
        (r'/(\d+)/([\w ]+)/ws', RoomSocket)
    ])


if __name__ == "__main__":
    init_database()
    app = make_app()
    app.listen(5000)
    enable_pretty_logging()
    ioloop.IOLoop.current().start()
