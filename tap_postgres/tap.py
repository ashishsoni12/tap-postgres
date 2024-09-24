from typing import List
from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
from tap_postgres.streams import PostgresStream
STREAM_TYPES = [
    PostgresStream

]

class Tappostgres(Tap):
    """PostgreSQL tap class."""
    name = "tap-postgres"

    config_jsonschema = th.PropertiesList(
        th.Property("host", th.StringType, required=True, description="PostgreSQL host"),
        th.Property("port", th.IntegerType, required=True, description="PostgreSQL port"),
        th.Property("database", th.StringType, required=True, description="PostgreSQL database name"),
        th.Property("user", th.StringType, required=True, description="PostgreSQL user"),
        th.Property("password", th.StringType, required=True, description="PostgreSQL password"),
        th.Property("initial_start_time", th.IntegerType, description="initial start time"),
        th.Property("endtimeU", th.IntegerType,  description="PostgreSQL table_name"),
        th.Property("timefield", th.StringType, required=True, description="PostgreSQL timefield name"),
        th.Property("timefield_format", th.StringType, required=True, description="PostgreSQL timefield_formate"),
        th.Property("time_zone", th.StringType, required=True, description="PostgreSQL databse timezone"),

    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        # Pass `self` to ensure it's the right type
        return [PostgresStream(tap=self)]

