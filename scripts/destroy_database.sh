#!/bin/sh

rm -f sqlite.db

export $(xargs <.env)
echo "DROP TABLE telegram_users;" | psql "$DATABASE_URI"
echo "DROP TABLE action_log;" | psql "$DATABASE_URI"
