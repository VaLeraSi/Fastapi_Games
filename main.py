import bcrypt
from tortoise.contrib.fastapi import register_tortoise
from starlette.exceptions import HTTPException
from fastapi import FastAPI
from models.models_for_pydantic import (
    UserRequest,
    GameRequest,
    UserResponse,
    Status,
    UsersGamesSchema,
    UserWithGames,
    GameWithUsers,
)
from models.models import User, Game
from config.settings import database_url, settings_site

app = FastAPI()


@app.post(
    "/user",
    status_code=201,
    response_model=UserResponse,
)
async def register_user(user: UserRequest):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
    user_obj = await User.create(
        **user.model_dump(exclude_unset=True), password_hash=hashed_password
    )
    return user_obj


@app.post(
    "/game",
    status_code=201,
    response_model=GameRequest,
)
async def register_user(game: GameRequest):
    game_obj = await Game.create(**game.model_dump(exclude_unset=True))
    return game_obj


@app.get(
    "/all_users",
    status_code=200,
    response_model=list[UserResponse],
)
async def get_all_users():
    users = await User.all()
    return users


@app.delete("/user/{user_id}", response_model=Status)
async def delete_user(user_id: int):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")


@app.delete("/game/{game_id}", response_model=Status)
async def delete_game(game_id: int):
    deleted_count = await Game.filter(id=game_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")
    return Status(message=f"Deleted game {game_id}")


@app.patch(
    "/users_games",
    status_code=204,
)
async def bind_user_game(data: UsersGamesSchema):
    user = await User.get(id=data.user_id)
    game = await Game.get(id=data.game_id)

    await user.games.add(game)


@app.get(
    "/about_user",
    status_code=200,
    response_model=UserWithGames,
)
async def about_user(user_id: int):
    user = await User.get(id=user_id)
    await user.fetch_related("games")
    return user


@app.get(
    "/about_game",
    status_code=200,
    response_model=GameWithUsers,
)
async def about_user(game_id: int):
    game = await Game.get(id=game_id)
    await game.fetch_related("users")
    return game


# app.include_router(router)
print(database_url)
register_tortoise(
    app,
    db_url=database_url,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings_site.host, port=settings_site.port)
