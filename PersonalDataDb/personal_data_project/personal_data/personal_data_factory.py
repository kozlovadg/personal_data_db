import attr

from .personal_data import personalData


@attr.s
class personalDataFactory(object):

    def create(self, name, phone_number, address):
        # type: (str, str, str) -> personalData

        personal_data = personalData(
            name=name, phone_number=phone_number, address=address
        )
        return personal_data
