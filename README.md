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
$ docker build -t psy-essence-bot .
$ docker run --env-file .env psy-essence-bot
```

## Install pre-commit hooks

```console
$ pip install pre-commit
$ pre-commit install
```

## Todo list

- [ ] Standardize the use of en, em and ascii dashes in [facts.json](/data/facts.json)

---
### Team members:
*  [Konstantin Borisov](https://github.com/cortan122)
*  [Diana Vakhitova](https://github.com/SimplePlease)
*  [Alexander Malyshenko](https://github.com/washinson)
