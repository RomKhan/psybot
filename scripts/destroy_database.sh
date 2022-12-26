#!/bin/sh

rm -f sqlite.db

export $(xargs <.env)

if echo "$DATABASE_URI" | grep -qv 'cortan122.tk'; then
  echo "Are you trying to delete a production database??"
  exit 1
fi

echo "DROP TABLE telegram_users;" | psql "$DATABASE_URI"
echo "DROP TABLE android_users;" | psql "$DATABASE_URI"
echo "DROP TABLE quiz_results;" | psql "$DATABASE_URI"
echo "DROP TABLE action_log;" | psql "$DATABASE_URI"
echo "DROP TABLE quiz_answers;" | psql "$DATABASE_URI"

echo "DROP TABLE data_articles;" | psql "$DATABASE_URI"
echo "DROP TABLE data_quizzes;" | psql "$DATABASE_URI"
echo "DROP TABLE data_recommendations;" | psql "$DATABASE_URI"
echo "DROP TABLE data_techniques;" | psql "$DATABASE_URI"
echo "DROP TABLE data_facts;" | psql "$DATABASE_URI"
