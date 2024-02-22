#! /bin/sh

test_db_connection() {
  psql -U "$DB_USERNAME" -d "$DB_NAME" -h "$DB_HOSTNAME" -c 'SELECT 1;'
}

export PGPASSWORD="$DB_PASSWORD"

echo "Waiting for db to be ready..."

echo "DB_USERNAME: $DB_USERNAME"
echo "DB_NAME: $DB_NAME"
echo "DB_HOSTNAME: $DB_HOSTNAME"
echo "DB_PASSWORD: $DB_PASSWORD"

while true; do
  echo "Trying to connect to db"
  if test_db_connection >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

python3 manage.py makemigrations
python3 manage.py makemigrations game_matchmaking
python3 manage.py migrate game_matchmaking

exec python3 manage.py runserver 0.0.0.0:80
