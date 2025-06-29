#!/bin/bash

sudo docker-compose up

# Optional: Log the execution
echo "Docker Compose cron job executed at $(date)" >>/var/log/docker_compose_cron.log