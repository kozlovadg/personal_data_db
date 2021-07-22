import attr

NAME = 'name'
PHONE_NUMBER = 'phone_number'
ADDRESS = 'address'


@attr.s
class personalData(object):
    name = attr.ib(type=str)  # type: str
    phone_number = attr.ib(type=str)  # type: str
    address = attr.ib(type=str)  # type: str
