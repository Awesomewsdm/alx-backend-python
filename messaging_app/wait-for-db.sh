#!/bin/bash

# wait-for-db.sh - Script to wait for MySQL database to be ready

set -e

host="$1"
port="$2"
user="$3"
password="$4"
shift 4
cmd="$@"

until mysql -h"$host" -P"$port" -u"$user" -p"$password" -e 'SELECT 1' >/dev/null 2>&1; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"
exec $cmd