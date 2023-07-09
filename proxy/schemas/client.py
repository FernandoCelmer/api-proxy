from typing import List
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field
from proxy.core.database.mongodb import PyObjectId


class SchemaClientPaths(BaseModel):
    path: str
    max_request: int
    time_stamp: int


class SchemaClientBase(BaseModel):
    user: str
    host: str
    paths: Optional[List[SchemaClientPaths]] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class SchemaClient(SchemaClientBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        aloow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
