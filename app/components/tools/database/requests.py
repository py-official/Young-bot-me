# pip lib
from sqlalchemy import create_engine, Column, MetaData, Table, Select, Insert
from sqlalchemy.engine.cursor import CursorResult

# my lib
from app.components.config import (
    DIR_DATABASE,
)
from app.components.tools.instances import Instances


# creating class to interact with the database
class RequestsToDatabase:
    def __new__(cls, database_name: str):
        # init engine sqlalchemy for db
        _engine = create_engine(f"sqlite:///{DIR_DATABASE + database_name}")

        # init Metadata class
        metadata = MetaData()

        # creating new instance class
        instance = super().__new__(cls)
        instance.database_name = database_name
        instance._engine = _engine
        instance.metadata = metadata

        """
        checking for the presence of a class instance in DatabaseRequestsClassInstances.instances.value,
        if there is, then we return the already created object from DatabaseRequestsClassInstances,
        if there is no instance in DatabaseRequestsClassInstances,
        we add it there and return the previously created instance of the class.
        """
        if instance in Instances.instances.value:
            return Instances.instances.value[
                Instances.instances.value.index(instance)]

        elif instance not in Instances.instances.value:
            Instances.instances.value.append(instance)

            return instance

    def __eq__(self, other):
        """
        :param other:
        :return:
        Returns True if the db names are the same
        and False if the names are different, or the instance does not belong to the RequestsToDatabase class.
        """
        if isinstance(other, RequestsToDatabase):
            return self.database_name == other.database_name

        return False

    def execute(self, obj: Select | Insert) -> CursorResult:  # func for general execution in db
        # connecting to db
        with self._engine.connect() as connection:
            # execute in db
            result = connection.execute(obj)

        return result

    def create_table(self, name_table: str, columns: list[Column]) -> None:  # func for creating a table in db
        # creating table
        Table(name_table, self.metadata, *columns)

        # creating table in db
        self.metadata.create_all(self._engine)

    def insert(self, table: Table, values: list[dict]) -> None:  # func for implementation of query 'insert' in db
        # generating insert request
        request_insert = table.insert().values(values)

        # executing insert request
        self.execute(request_insert)
