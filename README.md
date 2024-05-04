# Seven Wonders Duel API

An API for keeping track of scores in Seven Wonders Duel, using FastAPI and PostgreSQL.

## Setup

- Create a PostgreSQL database called `seven_wonders_duel`.
- Install Python >= 3.10.
- Install `uv`, a package installer for Python.

- From the root of this repository, install the Python dependencies with `uv`.


```sh
$ uv venv
$ source .venv/bin/activate
$ uv pip install -r requirements.txt
```

- Run the FastAPI server.

```sh
$ python -m uvicorn app.main:app
```

Navigate to http://localhost:8000/docs to view the API documentation.


## Example requests

### Add a game

`POST localhost:8000/games`

```json
{
    "date": "2022-12-19"
}
```

### Add a score

`POST localhost:8000/scores`

```json
{
    "game_id": 123,
    "player_id": 2,
    "civilian": 25,
    "science": 4,
    "commerce": 3,
    "guilds": 0,
    "wonders": 15,
    "tokens": 0,
    "coins": 2,
    "military": 5
}
```

### Get total scores of a game

`GET localhost:8000/scores/total?game_id=123`
