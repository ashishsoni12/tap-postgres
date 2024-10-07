from typing import Any, Dict, Optional, Iterable
from singer_sdk.streams import Stream
from singer_sdk import typing as th  # JSON schema typing helpers
from sqlalchemy import create_engine,text
from sqlalchemy.exc import SQLAlchemyError
from tap_postgres.client import create_postgres_engine
from .globals import addition
import json
from datetime import datetime
from tap_postgres.conversion import convert_epoch_to_format
import logging
LOGGER = logging.getLogger(__name__)
import pendulum
import time
import os
class PostgresStream(Stream):
    """Base stream class for tap-postgres using SQLAlchemy."""

    # Define the name of the stream
    name = "postgres_stream"
    replication_key = "state_endTime"
    schema = th.PropertiesList(
        th.Property("data", th.ObjectType()),
        th.Property("state_endTime", th.IntegerType),
        th.Property("state_startTime", th.IntegerType),
        th.Property("state_currentTime", th.StringType),
    ).to_dict()

    
    
    def __init__(self, tap, table_name: Optional[str] = None):
        super().__init__(tap)
#        self.table_name = table_name or self.config.get("table_name")
        self.engine = create_postgres_engine(self.config)
        
    def get_starting_timestamp(self, context: Optional[dict]) -> Optional[datetime]:
        LOGGER.info("==========context %s==========",context)
        value = self.get_starting_replication_key_value(context)
        LOGGER.info("==========value %s==========",value)
        if value is None:
            return None
        try:
            value = int(value)
        except ValueError as verr:
            value = pendulum.from_format(value, 'YYYY-MM-DD HH:mm:ss.SSS')
            value = int(value.timestamp()*1000)
            pass
        except ValueError as verr:
            value = pendulum.from_format(value, 'YYYY-MM-DD HH:mm:ss')
            value = int(value.timestamp()*1000)
            pass
        except Exception as ex:
            LOGGER.info("==========Exception occurred while converting to int==========")
            pass

        if not self.is_timestamp_replication_key:
            raise ValueError(
                f"The replication key {self.replication_key} is not of timestamp type"
            )

        return value

    def get_records(self, context: Optional[Dict] = None) -> Iterable[Dict[str, Any]]:
        timefield=self.config.get("timefield")                                #input timefield name

        timefield_format=self.config.get("timefield_format")                   #input timefield format
        time_zone=self.config.get("time_zone")                                 #input timezone

        start_date = self.get_starting_timestamp(context)
        LOGGER.info("==========start_date %s==========",start_date)

        if start_date is None:
            if(self.config.get("initial_start_time")):
                startTime = self.config.get("initial_start_time")
            else:
                startTime = pendulum.now('UTC').subtract(hours=24)
                startTime = (startTime.int_timestamp*1000)
        else:
            startTime=start_date

        startTime = int(startTime)+10

        endTime = pendulum.now('UTC')
        endTime = (endTime.int_timestamp*1000)
        endTime = int(endTime) - 300000
        timediff=int(endTime)-int(startTime)
        if (timediff > 86400000):
              endTime=int(startTime)+86400000
        else:                                                                   #check it pass current time
           with open("lastPos.txt", "w") as file:
                  file.write("true")
        self.state_currentTime=pendulum.now('UTC').int_timestamp*1000
        self.state_endTime = endTime
        self.state_startTime = startTime


        if os.path.isfile("flagPos.txt"):
                 with open("flagPos.txt", 'r') as file:
                   content = file.read()
        if self.config.get("endtimeU"):
            endTime=self.config.get("endtimeU")
            startTime=self.config.get("initial_start_time")
        #set params after current time passed from intial start time
        if os.path.isfile("lastPos.txt") and os.path.isfile("flagPos.txt") and content == "false" and timediff >86400000 and not self.config.get("endtimeU") :
          startTime=int(startTime)
          os.remove("lastPos.txt")
          endTime = pendulum.now('UTC')
          endTime = (endTime.int_timestamp*1000)
          endTime = int(endTime) - 300000
          LOGGER.info("******updated startTime: %s",startTime)
          LOGGER.info("******updated endTime: %s",endTime)
          if (endTime-self.state_currentTime) > 0 :
             endTime=self.state_currentTime - 300000
          self.state_endTime=endTime
          self.state_startTime=startTime
        #add 1-1 data to endtime to increament it, before current time passed from intial start time
        if os.path.isfile("lastPos.txt")==False and os.path.isfile("flagPos.txt") and content == "false" and timediff >86400000  and not self.config.get("endtimeU"):
          startTime=int(startTime)
          endTime=addition(endTime)
          LOGGER.info("******updated startTime when a day data mising : %s",startTime)
          LOGGER.info("******updated endTime when a day data missing : %s",endTime)
          if (endTime-self.state_currentTime) > 0 :
             endTime=self.state_currentTime - 300000
          self.state_endTime=endTime
          self.state_startTime=startTime
        
        LOGGER.info("==========starttimeEpoch %s==========",startTime)
        LOGGER.info("==========endtimeEpoch %s==========",endTime)

        #covert startTime epoch to timefield format
        starttimeFormat=convert_epoch_to_format(startTime, timefield_format,time_zone)
        #covert endTime epoch to timefield format
        endtimeFormat=convert_epoch_to_format(endTime, timefield_format,time_zone)
        LOGGER.info("==========starttimeFormat %s==========",starttimeFormat)
        LOGGER.info("==========endtimeFormat %s==========",endtimeFormat)
        query_prefix=self.config.get("query")
        # Construct the SQL query
        query = f"{query_prefix} WHERE {timefield} >= '{starttimeFormat}' AND {timefield} < '{endtimeFormat}'"
        self.logger.info(f"Executing query: {query}")
        
          
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()
            if rows!=0:                                         # if some data found delete all flag files
              if os.path.isfile("flagPos.txt"):
                 os.remove("flagPos.txt")
              if os.path.isfile("Pos_value.txt"):
                 os.remove("Pos_value.txt")
            else:
              if os.path.isfile("flagPos.txt"):
                 with open("flagPos.txt", 'r') as file:
                   content = file.read()
                 content = content.replace("true", "false")
              else:
                 with open("flagPos.txt", "w") as file:
                   file.write("false")
            column_names = list(result.keys()) # Retrieve column names
            x={}
            for row in rows:
#                record = {column_names[i]: row[i] for i in range(len(column_names))}
                record = {column_names[i]: (row[i].isoformat() if isinstance(row[i], datetime) else row[i]) for i in range(len(column_names))}
                json_string = json.dumps(record)
                x["data"]=json_string
                x["state_startTime"]= self.state_startTime
                x["state_endTime"]= self.state_endTime
                x["state_currentTime"]=self.state_currentTime
                yield x

    def post_process(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Adjust records after they are retrieved, if necessary."""
        return record


    def get_new_pkey(self, record: Dict) -> Any:
        return record.get("id")

