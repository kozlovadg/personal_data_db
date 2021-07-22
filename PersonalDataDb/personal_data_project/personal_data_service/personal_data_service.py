import csv
import json
import re
import sqlite3

import attr
from typing import List, Optional

from personal_data_project.personal_data import personalDataFactory
from personal_data_project.personal_data.personal_data import (
    personalData, ADDRESS, NAME, PHONE_NUMBER
)
from personal_data_project.personal_data_db_service import personalDataDbService


@attr.s
class personalDataService(object):

    personal_data_factory = attr.ib(
        type=personalDataFactory
    )  # type: personalDataFactory

    personal_data_db_service = attr.ib(
        type=personalDataDbService
    )  # type: personalDataDbService

    def get_personal_data_from_db(self, connection):
        # type: (SQLite.connection) -> List[personalData]

        personal_data_list = []
        if self.personal_data_db_service.check_if_table_exists(
                connection=connection
        ):

            connection.row_factory = sqlite3.Row

            with connection:
                cur = connection.cursor()
                cur.execute("SELECT * FROM info")

                rows = cur.fetchall() or []

                for row in rows:
                    personal_data = self.personal_data_factory.create(
                        name=row[NAME] if NAME in row.keys() else '',
                        phone_number=row[PHONE_NUMBER] if PHONE_NUMBER in row.keys() else '',
                        address=row[ADDRESS] if ADDRESS in row.keys() else ''
                    )

                    personal_data_list.append(personal_data)

        return personal_data_list

    # -------------- LIVE --------------

    def add_personal_data_from_live(
            self, connection, name='', phone_number='', address=''
    ):
        # type: (SQLite.connection, Optional[str], Optional[str], Optional[str]) -> personalData

        personal_data = self.personal_data_factory.create(
            name=name,
            phone_number=phone_number,
            address=address
        )

        self.personal_data_db_service.add_to_data_base(
            connection=connection,
            personal_data_list=[personal_data]
        )

        return personal_data

    # -------------- JSON --------------

    def add_personal_data_from_json_file(self, connection, json_path):
        # type: (SQLite.connection, str) -> List[personalData]

        personal_data_list = []

        with open(json_path) as json_file:
            data = json.load(json_file)
            if not data:
                raise KeyError
            
            if 'people' not in data:
                raise KeyError
                
            for person in data['people']:

                for key in [ADDRESS, NAME, PHONE_NUMBER]:
                    if key not in data['people'][person]:
                        raise KeyError

                personal_data = self.personal_data_factory.create(
                    name=data['people'][person][NAME],
                    phone_number=data['people'][person][PHONE_NUMBER],
                    address=data['people'][person][ADDRESS]
                )
                personal_data_list.append (personal_data)

        self.personal_data_db_service.add_to_data_base(
            connection=connection,
            personal_data_list=personal_data_list
        )

        return personal_data_list

    def write_as_json_file(
            self, connection, file_path, personal_data_list_filtered
    ):
        # type: (SQLite.connection, str, Optional[List[personalData]]) -> None

        people = {}
        personal_data_list = (
            self.get_personal_data_from_db(connection=connection)
            if not personal_data_list_filtered
            else personal_data_list_filtered
        )  # type: List[personalData]

        increment = 0
        for personal_data in personal_data_list:

            person = 'person_{}'.format(increment)
            people[person] = {
                NAME: personal_data.name,
                PHONE_NUMBER: personal_data.phone_number,
                ADDRESS: personal_data.address,
            }
            increment += 1

        data = {'people': people} if people else {}

        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)

    # -------------- CSV --------------

    def add_personal_data_from_csv_file(self, connection, csv_path):
        # type: (SQLite.connection, str) -> List[personalData]

        personal_data_list = []

        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if line_count == 0:

                    for key in [ADDRESS, NAME, PHONE_NUMBER]:
                        if key not in row:
                            raise KeyError

                    name_index = row.index(NAME)
                    address_index = row.index(ADDRESS)
                    phone_number_index = row.index(PHONE_NUMBER)

                    line_count += 1

                else:

                    personal_data = self.personal_data_factory.create(
                        name=row[name_index],
                        address=row[address_index],
                        phone_number=row[phone_number_index]
                    )
                    personal_data_list.append (personal_data)
                    
                    line_count += 1
                    
        self.personal_data_db_service.add_to_data_base(
            connection=connection,
            personal_data_list=personal_data_list
        )
        
        return personal_data_list

    def write_as_csv_file(
            self, connection, file_path, personal_data_list_filtered
    ):
        # type: (SQLite.connection, str, Optional[List[personalData]]) -> None

        people = []
        personal_data_list = (
            self.get_personal_data_from_db(connection=connection)
            if not personal_data_list_filtered
            else personal_data_list_filtered
        )  # type: List[personalData]

        for personal_data in personal_data_list:

            person = [
                personal_data.name,
                personal_data.phone_number,
                personal_data.address
            ]
            people.append(person)

        with open(file_path, 'wb') as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow([NAME, ADDRESS, PHONE_NUMBER])
            for person in people:
                writer.writerow(person)

    # -------------- FILTER --------------

    def filter(self, connection, name=None, address=None, phone_number=None):
        # type: (SQLite.connection, Optional[str], Optional[str], Optional[str]) -> List[personalData]

        name_pattern = re.compile(name) if name else None
        address_pattern = re.compile(address) if address else None
        phone_number_pattern = re.compile(phone_number) if phone_number else None

        people = []
        personal_data_list = self.get_personal_data_from_db(
            connection=connection
        )  # type: List[personalData]

        if name_pattern:
            for personal_data in personal_data_list:
                if not name_pattern.match (personal_data.name):
                    continue
                people.append (personal_data)

            personal_data_list = people

        if address_pattern:
            for personal_data in personal_data_list:
                if not address_pattern.match (personal_data.address):
                    continue
                people.append (personal_data)

            personal_data_list = people

        if phone_number_pattern:
            for personal_data in personal_data_list:
                if not phone_number_pattern.match (personal_data.phone_number):
                    continue
                people.append (personal_data)

            personal_data_list = people

        return personal_data_list

    def print_data_base(self, personal_data_list):
        # type: (List[personalData]) -> None

        for personal_data in personal_data_list:
            print '({name}, {phone}, {address})'.format(
                name=personal_data.name,
                phone=personal_data.phone_number,
                address=personal_data.address
            )
