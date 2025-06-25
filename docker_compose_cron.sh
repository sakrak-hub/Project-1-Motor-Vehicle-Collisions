#!/bin/bash

sudo /usr/bin/python3 app_launcher.py 

# Optional: Log the execution
echo "Docker Compose cron job executed at $(date)" >> /var/log/docker_compose_cron.log