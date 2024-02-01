from typing import List

from tortoise.models import Model
from tortoise import fields
from app.dal.models import TimestampMixin
from app.dal.models.auth.permission import Permission
from app.dal.models.auth.role import Role


class User(Model, TimestampMixin):
    id = fields.IntField(pk=True)
    name = fields.CharField(200)
    phone = fields.CharField(max_length=12)
    password = fields.TextField()

    roles: fields.ManyToManyRelation["Role"] = fields.ManyToManyField("models.Role", related_name='users', through='users_roles')
    permissions: fields.ManyToManyRelation["Permission"] = fields.ManyToManyField("models.Permission",
                                                                                  related_name='users',
                                                                                  through='users_permissions')

    async def has_role(self, name: str):
        role = self.roles.filter(name=name).first()
        return role is not None

    async def has_permission(self, permission: str):
        permissions = await self.get_all_permissions()
        return len(list(filter(lambda x: x.name == permission, permissions))) > 0

    async def get_all_permissions(self) -> List[Permission]:
        all_permissions = await self.permissions
        async for role in self.roles:
            all_permissions.extend(await role.permissions)

        return all_permissions

    class Meta:
        table = 'users'
