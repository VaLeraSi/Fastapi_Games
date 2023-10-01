from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    name: str = Field(max_length=20)
    age: int = Field(min=0, max=100)
    email: str
    phone: str = Field(pattern=r'^\+7[0-9]{10}$', max_length=12, min_length=12)
    password: str


class UserResponse(BaseModel):
    name: str
    age: int
    email: str
    phone: str


class UsersGamesSchema(BaseModel):
    user_id: int
    game_id: int


class GameRequest(BaseModel):
    name: str = Field(max_length=20)


class Status(BaseModel):
    message: str


class Game(BaseModel):
    name: str

    class Config:
        from_attributes = True


class User(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserWithGames(BaseModel):
    name: str
    age: int
    email: str
    phone: str
    games: list[Game]


class GameWithUsers(BaseModel):
    name: str
    users: list[User]
