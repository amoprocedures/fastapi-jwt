from tortoise.models import Model
from tortoise.fields import IntField, CharField, TextField


class User(Model):
    id = IntField(pk=True)
    email = CharField(max_length=100, null=False, unique=True)
    first_name = CharField(max_length=50, null=True)
    last_name = CharField(max_length=50, null=True)
    password_hash = CharField(max_length=100, null=False)
    refresh_token = TextField(null=True)

    class Meta:
        table = 'users'
