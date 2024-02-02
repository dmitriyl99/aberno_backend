from tortoise.models import Model
from tortoise import fields

from app.core.models import TimestampMixin
from app.core.models.organization.organization import Organization
from app.core.models.organization.employee import Employee


class Department(Model, TimestampMixin):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    organization: fields.ForeignKeyRelation["Organization"] = fields.ForeignKeyField("models.Organization",
                                                                                     related_name='departments')
