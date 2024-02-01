from tortoise.models import Model
from tortoise import fields

from app.dal.models import TimestampMixin
from app.dal.models.organization.organization import Organization
from app.dal.models.organization.employee import Employee


class Department(Model, TimestampMixin):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    organization: fields.ForeignKeyRelation["Organization"] = fields.ForeignKeyField("models.Organization",
                                                                                     related_name='departments')
    manager: fields.ForeignKeyRelation["Employee"] = fields.ForeignKeyField("models.Employee",
                                                                            related_name='managed_departments')
