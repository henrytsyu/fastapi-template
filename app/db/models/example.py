from . import GenericModel


class Example(GenericModel, table=True):
    name: str
