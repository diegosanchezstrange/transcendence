#! /bin/bash


# Setup
base_dir="$PWD"
front_dir="$base_dir/srcs/front"
users_dir="$base_dir/srcs/users"
login_dir="$base_dir/srcs/login"
notifications_dir="$base_dir/srcs/notifications"

front_port="3000"
users_port="8081"
login_port="8080"
notifications_port="8082"

set -m

function log() {
  local message="$1"
  # shellcheck disable=SC2155
  local timestamp=$(date +"[%Y-%m-%d %H:%M:%S]")
  echo "$timestamp" "$message"
}

function sighandler() {
  log "SIGINT received... shutting down."
  kill $(jobs -p)
  cd "$base_dir/srcs" && docker-compose down
  exit 1
}

function init_env() {
  curr_dir="$1"

  if [ ! -d "$curr_dir/venv" ]; then
    log "Creating virtual environment"
    python3 -m venv venv
  fi
  source venv/bin/activate
  log "Installing requirements"
  pip install -r requirements.txt >/dev/null
  export $(cat ../../.env.example|tr "\n" " ")
}

function setup_database() {
  cd "$base_dir/srcs" || (echo "cd failed" && exit 1)
  docker-compose up --build database &
}

function run_service() {
  local dir="$1"
  local port="$2"

  trap 'sighandler' SIGINT
  cd "$dir" || (echo "Error: no such directory" && exit 1)
  init_env "$dir"
  python3 manage.py migrate
  python3 manage.py runserver 0.0.0.0:"$port"&
  deactivate
}

function wait_for_db() {
  local host="$1"
  local port="$2"

  while true; do
    if nc -zv "$host" "$port" 2>&1 | grep -q 'succeeded'; then
      log "Database connection successful"
      break
    else
      sleep 1
    fi
  done
}

function setup_redis() {
    cd "$base_dir/srcs" && docker-compose up --build redis &
}

function main() {
  # Signal handler to stop everything and clean up
  trap 'sighandler' SIGINT

  # Set up database
  log "Setting up database"
  setup_database

  log "Setting up redis"
  setup_redis

  wait_for_db "localhost" "5432"

  log "Setting up users service"
  run_service "$users_dir" "$users_port"

  log "Setting up login service"
  run_service "$login_dir" "$login_port"

  log "Setting up notifications service"
  run_service "$notifications_dir" "$notifications_port"

#  log "Setting up frontend service"
#  run_service "$front_dir" "$front_port"

  while true; do
    :
  done
}

main