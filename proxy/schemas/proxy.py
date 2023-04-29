from typing import List
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field
from proxy.core.database.mongodb import PyObjectId


class SchemaProxyPaths(BaseModel):
    path: str
    target: str
    max_request: int
    time_stamp: int


class SchemaProxyBase(BaseModel):
    host: str
    scheme: str
    paths: Optional[List[SchemaProxyPaths]] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class SchemaProxy(SchemaProxyBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        aloow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
