# python lib
from logging import ERROR

# pip lib
from sqlalchemy import create_engine, Column, MetaData, Table, Select, Insert
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.ext.automap import automap_base, AutomapBase

# project lib
from app.components.config import (
    DIR_CONF_YAML_SECRET,
    DIR_SECRET_KEYS,
    FILE_TYPE_YAML_CONFS,
    FILE_TYPE_SECRET_KEY,
)
from app.components.tools.instances import Instances
from ..encryption import get_encrypted_data
from ..log.logger import CustomLogger


# creating logger
logger = CustomLogger(__name__, ERROR)


# creating class to interact with the database
class RequestsToDatabase:
    def __new__(cls, type_database: str, host_name: str):
        path_to_connect_db_data_file = DIR_CONF_YAML_SECRET + "secret_database_hosts" + FILE_TYPE_YAML_CONFS
        path_to_secret_key_file = DIR_SECRET_KEYS + "secret_key_database_hosts" + FILE_TYPE_SECRET_KEY

        connect_db_data: str = cls.__get_connect_db_data(path_to_connect_db_data_file, path_to_secret_key_file,
                                                         host_name)

        # init engine sqlalchemy for db
        _engine = create_engine(f"{type_database}://{connect_db_data}")

        # init Metadata class
        metadata: MetaData = MetaData()
        metadata.reflect(bind=_engine)

        # initialization of the base class of the database and table reflection
        base: AutomapBase = automap_base(metadata=metadata)
        base.prepare()

        # creating new instance class
        instance = super().__new__(cls)
        instance.database_name = host_name
        instance._engine = _engine
        instance.metadata = metadata
        instance.base = base

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

    @staticmethod
    def __get_connect_db_data(path_to_file_db_data: str, path_to_file_secret_key: str, host_name: str) -> str:
        """
        Function for obtaining data that will be used to connect to the database
        :param path_to_file_db_data:
        :param path_to_file_secret_key:
        :param host_name:
        :return:
        """

        # receiving decrypted data to connect to the database
        decrypted_connect_db_data: dict = get_encrypted_data(path_to_file_db_data, path_to_file_secret_key)

        # checking whether the specified host name for connecting to the database is in the decrypted data
        if host_name in decrypted_connect_db_data:
            return decrypted_connect_db_data[host_name]

        else:
            text_error = "The host name for connecting to the database was not found."
            logger.error(text_error)
            raise ValueError(text_error)

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

    def users_get_id(self, table: str) -> tuple:
        jsm = JsonManager()
        jsm.dload_cfg("bots_properties.json")
        fields = jsm.buffer["YoungMouse"]["modals"]["reg_modal"]["questions"]
        db_field = "did, " + ", ".join(field["custom_id"] for field in fields)
        self.cursor.execute(f'SELECT {db_field} FROM {table}')
        ids = self.cursor.fetchall()
        return ids
