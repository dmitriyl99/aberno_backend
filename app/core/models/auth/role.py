from tortoise.models import Model
from tortoise import fields


class Role(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    permissions = fields.ManyToManyField('models.Permission', related_name='roles',
                                         through='roles_permissions')

    class Meta:
        table = 'roles'
