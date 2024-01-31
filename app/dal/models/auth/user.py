from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(200)
    phone = fields.CharField(max_length=12)
    password = fields.TextField()

    roles = fields.ManyToManyField("models.Role", related_name='users', through='users_roles')
    permissions = fields.ManyToManyField("models.Permission", related_name='users',
                                         through='users_permissions')

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'users'
