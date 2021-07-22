import unittest

import sqlite3 as lite

from personal_data_project.personal_data.personal_data import personalData
from personal_data_project.personal_data import personalDataFactory
from personal_data_project.personal_data_db_service import personalDataDbService
from personal_data_project.personal_data_service import personalDataService


class FactoryUsageTestCase(unittest.TestCase):

    def test_object_type(self):
        personal_data_factory = personalDataFactory()
        obj = personal_data_factory.create(
            'Test Name', 'Test Phone Number', 'Test Address'
        )
        self.assertIsInstance(obj, personalData)

    def test_parameter_type(self):
        personal_data_factory = personalDataFactory()
        obj = personal_data_factory.create(
            'Test Name', 89112223344, 'Test Address'
        )
        self.assertIsInstance(obj.phone_number, str)


class DataBaseTestCase(unittest.TestCase):

    def test_create_data_base_from_file(self):

        personal_data_factory = personalDataFactory()
        personal_data_db_service = personalDataDbService()

        personal_data_service = personalDataService(
            personal_data_factory=personal_data_factory,
            personal_data_db_service=personal_data_db_service
        )

        connection = lite.connect('info.db')
        personal_data_service.add_personal_data_from_json_file(
            connection=connection,
            json_path='input.json'
        )


if __name__ == '__main__':
    unittest.main()
