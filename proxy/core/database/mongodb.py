import logging

import motor.motor_asyncio
from bson import ObjectId
from proxy.core.settings import Settings


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


async def get_mongodb():
    config = Settings().load_variables()
    client = motor.motor_asyncio.AsyncIOMotorClient(
        config.get("nosql_database_url"))

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as error:
        logging.error(error)

    return client