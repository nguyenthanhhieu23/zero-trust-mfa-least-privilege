#!/usr/bin/env bash
set -euo pipefail

curl --fail --silent http://localhost:5000/health
printf '\n'
curl --fail --silent http://localhost:5000/api/public
printf '\n'
echo "Unauthenticated protected endpoints should return HTTP 401."
curl --silent --output /dev/null --write-out 'user endpoint: HTTP %{http_code}\n' http://localhost:5000/api/user
curl --silent --output /dev/null --write-out 'admin endpoint: HTTP %{http_code}\n' http://localhost:5000/api/admin