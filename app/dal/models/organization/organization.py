from tortoise.models import Model
from tortoise.fields import IntField, TextField

from app.dal.models import TimestampMixin


class Organization(Model, TimestampMixin):
    id = IntField(pk=True)
    name = TextField()
    legal_name = TextField()
    legal_name_prefix = TextField()

    class Meta:
        table = 'organizations'
