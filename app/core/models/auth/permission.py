from tortoise.models import Model
from tortoise import fields


class Permission(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    class Meta:
        table = 'permissions'
