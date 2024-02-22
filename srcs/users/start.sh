#! /bin/sh

test_db_connection() {
  psql -U "$DB_USERNAME" -d "$DB_NAME" -h "$DB_HOSTNAME" -c 'SELECT 1;'
}

export PGPASSWORD="$DB_PASSWORD"

while true; do
  echo "Trying to connect to db"
  if test_db_connection >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

python3 manage.py makemigrations friends users
python3 manage.py migrate
python3 manage.py migrate friends users

mv /app/profile_pics /images/profile_pics

exec python3 manage.py runserver 0.0.0.0:80
