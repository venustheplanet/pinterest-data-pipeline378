import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text
from datetime import datetime


random.seed(100)


class AWSDBConnector:

    def __init__(self):

        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector()


def run_infinite_post_data_loop():
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)
            

            # send data to API
            post_to_api("https://j4vf084mkf.execute-api.us-east-1.amazonaws.com/dev/streams/streaming-121ca9f7ce2b-pin/record", pin_result, "streaming-121ca9f7ce2b-pin")
            post_to_api("https://j4vf084mkf.execute-api.us-east-1.amazonaws.com/dev/streams/streaming-121ca9f7ce2b-geo/record", geo_result, "streaming-121ca9f7ce2b-geo")
            post_to_api("https://j4vf084mkf.execute-api.us-east-1.amazonaws.com/dev/streams/streaming-121ca9f7ce2b-user/record", user_result, "streaming-121ca9f7ce2b-user")


# def default_serializer(obj):
#     if isinstance(obj, datetime):
#         return obj.isoformat()  # Convert datetime to a string representation
#     raise TypeError("Type not serializable")

def post_to_api(invoke_url, record, stream_name):
    payload = json.dumps({
        "StreamName": stream_name,
        "Data": record,
        "PartitionKey": stream_name
        }, default=str) #Use custom serializer for datetime objects
    
    headers = {'Content-Type': 'application/json'}
    # print(payload)
    response = requests.request("PUT", invoke_url, headers=headers, data=payload)
    print(response.status_code)
    # print(response.content)

if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')
    
    


