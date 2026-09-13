#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../SETUP"
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created SETUP/.env. Change demo passwords before use."
fi
docker compose --env-file .env up -d --build
echo "Keycloak: http://localhost:8080"
echo "Demo API: http://localhost:5000/health"