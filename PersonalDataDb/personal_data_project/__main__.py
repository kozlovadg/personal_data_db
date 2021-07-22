#!usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sqlite3 as lite

from personal_data_project.personal_data_db_service import (
    personalDataDbService
)
from personal_data_project.personal_data_service import personalDataService
from personal_data_project.bindings_specs import di_container
from personal_data_project.utils import add_arguments_to_parser

connection = lite.connect('info.db')
personal_data_service = di_container.provide(
    personalDataService
)  # type: personalDataService
personal_data_db_service = di_container.provide(
    personalDataDbService
)  # type: personalDataDbService

parser = argparse.ArgumentParser(description="personalData")
add_arguments_to_parser(parser)
args = parser.parse_args()

# --------------------------- CLEAN ---------------------------
if args.clear:
    personal_data_db_service.clear_all_data(connection=connection)

# --------------------------- ADD FROM JSON ---------------------------
if args.add_from_json:
    personal_data_service.add_personal_data_from_json_file(
        connection=connection, json_path=args.add_from_json
    )

# --------------------------- ADD FROM CSV ---------------------------
if args.add_from_csv:
    personal_data_service.add_personal_data_from_csv_file(
        connection=connection, csv_path=args.add_from_csv
    )

# --------------------------- ADD FROM LIVE ---------------------------
if args.add_name_live or args.add_address_live or args.add_phone_number_live:
    personal_data_service.add_personal_data_from_live(
        connection=connection,
        name=args.add_name_live if args.add_name_live else '',
        address=args.add_address_live if args.add_address_live else '',
        phone_number=(
            args.add_phone_number_live
            if args.add_phone_number_live
            else ''
        ),
    )

# --------------------------- FILTER ---------------------------
personal_data_filtered = None
if args.filter_by_name or args.filter_by_address or args.filter_by_phone_number:
    personal_data_filtered = personal_data_service.filter(
        connection=connection,
        name=args.filter_by_name if args.filter_by_name else None,
        address=args.filter_by_address if args.filter_by_address else None,
        phone_number=(
            args.filter_by_phone_number if args.filter_by_phone_number else None
        )
    )

# --------------------------- DISPLAY TO STDOUT ---------------------------
if args.display:
    if personal_data_filtered:
        personal_data_service.print_data_base(
            personal_data_list=personal_data_filtered
        )
    else:
        if personal_data_db_service.check_if_table_exists(connection=connection):
            personal_data_db_service.print_data_base(connection=connection)
        else:
            print 'Data base is empty.'

# --------------------------- WRITE TO JSON ---------------------------
if args.write_to_json:
    personal_data_service.write_as_json_file(
        connection=connection,
        file_path=args.write_to_json,
        personal_data_list_filtered=personal_data_filtered
    )

# --------------------------- WRITE TO CSV ---------------------------
if args.write_to_csv:
    personal_data_service.write_as_csv_file(
        connection=connection, file_path=args.write_to_csv,
        personal_data_list_filtered=personal_data_filtered
    )