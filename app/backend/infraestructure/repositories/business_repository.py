from app.backend.domain.entities import Business
from app.utils import logger
from typing import List
from typing import Optional
import boto3
import uuid
import json

class BusinessRepository:

    def __init__(self, aws_access_key_id, aws_secret_access_key, region, db_url='http://dynamodb-local:8000'):
        dynamodb = boto3.resource('dynamodb', endpoint_url=db_url, region_name=region,
                          aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.table_name = 'businesses'
        self.table = dynamodb.Table(self.table_name)

    def save(self, business: Business):
        business_id = str(uuid.uuid4())
        business.business_id = business_id

        self.table.put_item(
            Item={
                'id': business_id,
                'bnbot_id': business.bnbot_id,
                'info': business.json()
            }
        )

        return business
