from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field
from proxy.core.database.mongodb import PyObjectId


class SchemaBase(BaseModel):
    host: str
    scheme: str
    paths: Optional[list] = []

class SchemaCreate(SchemaBase):
    pass


class SchemaUpdate(SchemaBase):
    host: Optional[str]
    scheme: Optional[str]
    paths: Optional[list]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Schema(SchemaBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        aloow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
