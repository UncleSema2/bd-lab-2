#!/bin/bash
set -e

ROLE="${CASSANDRA_USERNAME}"
PASSWORD="${CASSANDRA_PASSWORD}"
KEYSPACE="${CASSANDRA_KEYSPACE}"

docker-entrypoint.sh cassandra &

for i in $(seq 1 60); do
  if cqlsh -u "${ROLE}" -p "${PASSWORD}" -e 'describe cluster' &>/dev/null; then
    echo "Cassandra is ready"
    break
  fi
  echo "Waiting for Cassandra to be ready... ($i/60)"
  sleep 5
done

cqlsh -u "${ROLE}" -p "${PASSWORD}" -e "CREATE KEYSPACE IF NOT EXISTS ${KEYSPACE} WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}" || true

tail -f /dev/null
