from argparse import ArgumentParser


def add_arguments_to_parser(parser):
    # type: (ArgumentParser) -> None

    parser.add_argument(
        '-add_from_json',
        "--add_from_json",
        action="store",
        help=(
            "Add Data From JSON File (Specify path to "
            "tests JSON file, relative to current running script)"
        )
    )
    parser.add_argument(
        '-add_from_csv',
        "--add_from_csv",
        action="store",
        help=(
            "Add Data From CSV File (Specify path to "
            "tests JSON file, relative to current running script)"
        )
    )

    parser.add_argument(
        '-add_name',
        "--add_name_live",
        action="store",
        help="Add Name From Terminal"
    )
    parser.add_argument(
        '-add_address',
        "--add_address_live",
        action="store",
        help="Add Address From Terminal"
    )
    parser.add_argument(
        '-add_phone',
        "--add_phone_number_live",
        action="store",
        help="Add Phone Number From Terminal"
    )

    parser.add_argument(
        '-write_to_json',
        "--write_to_json",
        action="store",
        help=(
            "Write to JSON (Specify path to output "
            "JSON file, relative to current running script)"
        )
    )
    parser.add_argument(
        '-write_to_csv',
        "--write_to_csv",
        action="store",
        help=(
            "Write to CSV (Specify path to output "
            "JSON file, relative to current running script)"
        )
    )

    parser.add_argument(
        '-filter_by_name',
        "--filter_by_name",
        action="store",
        help=(
            "Filter existing data base by name "
            "(regular expression type of filtration)"
        )
    )
    parser.add_argument(
        '-filter_by_address',
        "--filter_by_address",
        action="store",
        help=(
            "Filter existing data base by address "
            "(regular expression type of filtration)"
        )
    )
    parser.add_argument(
        '-filter_by_phone_number',
        "--filter_by_phone_number",
        action="store",
        help=(
            "Filter existing data base by phone number "
            "(regular expression type of filtration)"
        )
    )

    parser.add_argument(
        '-c', "--clear", action="store_true", help="Clear All Data from Database"
    )
    parser.add_argument(
        '-d', "--display", action="store_true", help="Display Data from Database"
    )
