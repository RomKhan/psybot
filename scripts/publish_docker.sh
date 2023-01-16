#!/bin/sh

set -m
cd -- "$(dirname -- "$0")/.."

if ! pgrep dockerd; then
  sudo dockerd -G $USER &
  dockerd_pid="$!"
  sleep 1
fi

./scripts/build_docker.sh
docker save psy-essence-bot | ssh -C psy-essence "docker load"
ssh psy-essence "systemctl restart psybot.service"

if [ ! -z "$dockerd_pid" ]; then
  kill -INT "$dockerd_pid"
  wait "$dockerd_pid"
fi
