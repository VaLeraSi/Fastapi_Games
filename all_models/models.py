from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20, unique=True)
    age = fields.IntField()
    email = fields.CharField(max_length=255)
    phone = fields.CharField(max_length=12, unique=True)
    password_hash = fields.CharField(max_length=255)
    games = fields.ManyToManyField("all_models.Game", related_name="users", through="users_games")


class Game(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20, unique=True)
    users: fields.ManyToManyRelation[User]


