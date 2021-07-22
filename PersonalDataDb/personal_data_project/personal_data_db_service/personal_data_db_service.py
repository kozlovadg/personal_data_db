import attr
from typing import List

from personal_data_project.personal_data.personal_data import (
    personalData, ADDRESS, NAME, PHONE_NUMBER
)


@attr.s
class personalDataDbService(object):

    def clear_all_data(self, connection):
        # type: (SQLite.connection) -> None

        if self.check_if_table_exists(connection=connection):
            sql = 'DELETE FROM info'
            cur = connection.cursor()
            cur.execute(sql)
            connection.commit()

    def check_if_table_exists(self, connection):
        # type: (SQLite.connection) -> bool

        list_of_tables = connection.execute(
            """SELECT name FROM sqlite_master WHERE type='table' AND name='info'; """
        ).fetchall()

        if not list_of_tables:
            return False

        return True

    def add_to_data_base(self, connection, personal_data_list):
        # type: (SQLite.connection, List[personalData]) -> None

        with connection:
            cur = connection.cursor()
            if not self.check_if_table_exists(connection):
                cur.execute(
                    "CREATE TABLE info ({name} TEXT, {phone_number} TEXT, {address} TEXT)".format(
                        name=NAME,
                        address=ADDRESS,
                        phone_number=PHONE_NUMBER
                    )
                )
            for personal_data in personal_data_list:

                cur.execute(
                    "SELECT rowid FROM info WHERE {name} = ? AND {phone_number} = ? AND {address} = ?".format(
                        name=NAME,
                        address=ADDRESS,
                        phone_number=PHONE_NUMBER
                    ), (
                        personal_data.name,
                        personal_data.phone_number,
                        personal_data.address
                    )
                )
                data = cur.fetchall()
                if len(data) == 0:
                    print(
                        'Debug: Component {} was added.'.format(personal_data)
                    )
                    cur.execute("INSERT INTO info VALUES('{}', '{}', '{}')".format(
                            personal_data.name,
                            personal_data.phone_number,
                            personal_data.address
                        )
                    )
                else:
                    print(
                        'Debug: Component {} already exists.'.format(
                            personal_data
                        )
                    )

    def print_data_base(self, connection):
        # type: (SQLite.connection) -> None

        with connection:
            cur = connection.cursor()
            cur.execute("SELECT * FROM info")

            rows = cur.fetchall() or []
            for row in rows:
                print row
