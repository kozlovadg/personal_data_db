import pinject

from .personal_data import personalDataFactory
from .personal_data_db_service import personalDataDbService


class personalDataBindingSpec(pinject.BindingSpec):
    def configure(self, bind):

        bind("personal_data_factory", to_class=personalDataFactory)
        bind("personal_data_db_service", to_class=personalDataDbService)


di_container = pinject.new_object_graph(
    binding_specs=[
        personalDataBindingSpec(),
    ],
    modules=None,
)
