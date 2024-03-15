# Psychological Essence.
### Telegram bot.

## Starting the bot

```console
$ echo 'API_TOKEN=something' >> .env
$ echo 'DATABASE_URI=something' >> .env
$ ./run.sh
```

## Building (and running) docker container

```console
$ ./scripts/build_docker.sh
$ docker run --env-file .env psy-essence-bot
```

## Install pre-commit hooks

```console
$ pip install pre-commit
$ pre-commit install
```

---
### Team members:
*  [Konstantin Borisov](https://github.com/cortan122)
*  [Diana Vakhitova](https://github.com/SimplePlease)
*  [Alexander Malyshenko](https://github.com/washinson)
*  [Roman Khan](https://github.com/RomKhan)
