from sqlalchemy import Column, Integer, String

from ..common.database import BaseModel
from ..common.serializers import ModelSerializerMixin


class Foss(BaseModel, ModelSerializerMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, nullable=False, unique=True)
