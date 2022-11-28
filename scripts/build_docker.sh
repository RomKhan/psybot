#!/bin/sh

if [ -z "$SSH_AGENT_PID" ]; then
  eval `ssh-agent`
  ssh-add
  clean_ssh_agent=true
fi

DOCKER_BUILDKIT=1 docker build -t psy-essence-bot --ssh default .

if [ ! -z "$clean_ssh_agent" ]; then
  eval `ssh-agent -k`
fi
