#!/bin/bash

rm -f sqlite.db

if [ -z "$DATABASE_URI" ]; then
  export $(xargs <.env)
fi

if ! [[ "$DATABASE_URI" == *cortan122.tk* || "$DATABASE_URI" == *localhost* ]]; then
  echo "Are you trying to delete a production database??"
  exit 1
fi

echo "DROP TABLE telegram_users CASCADE;" | psql "$DATABASE_URI"
echo "DROP TABLE android_users;" | psql "$DATABASE_URI"
echo "DROP TABLE quiz_results;" | psql "$DATABASE_URI"
echo "DROP TABLE action_log;" | psql "$DATABASE_URI"
echo "DROP TABLE quiz_answers;" | psql "$DATABASE_URI"
echo "DROP TABLE recorded_likes;" | psql "$DATABASE_URI"

echo "DROP TABLE data_articles;" | psql "$DATABASE_URI"
echo "DROP TABLE data_quizzes CASCADE;" | psql "$DATABASE_URI"
echo "DROP TABLE data_recommendations;" | psql "$DATABASE_URI"
echo "DROP TABLE data_techniques;" | psql "$DATABASE_URI"
echo "DROP TABLE data_facts;" | psql "$DATABASE_URI"
echo "DROP TABLE data_lessons;" | psql "$DATABASE_URI"
echo "DROP TABLE data_courses;" | psql "$DATABASE_URI"

echo "DROP sequence telegram_users_id_seq;" | psql "$DATABASE_URI"
echo "DROP sequence global_id_seq;" | psql "$DATABASE_URI"
