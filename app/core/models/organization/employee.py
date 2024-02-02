from tortoise.models import Model
from tortoise.fields import IntField, ForeignKeyField, ForeignKeyRelation, DateField, OneToOneField, OnDelete

from app.core.models import TimestampMixin
from app.core.models.auth.user import User
from app.core.models.organization.organization import Organization


class Employee(Model, TimestampMixin):
    id = IntField(pk=True)
    birth_date = DateField()

    user: ForeignKeyRelation["User"] = OneToOneField("models.User", related_name='employee', on_delete=OnDelete.CASCADE)
    organization: ForeignKeyRelation["Organization"] = ForeignKeyField("models.Organization", related_name='employees')
    department = ForeignKeyField("models.Department", related_name='employees')
