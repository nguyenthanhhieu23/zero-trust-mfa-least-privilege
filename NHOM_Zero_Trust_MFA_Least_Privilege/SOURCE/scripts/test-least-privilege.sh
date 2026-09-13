#!/usr/bin/env bash
set -euo pipefail

TOKEN="${TOKEN:-}"
if [ -z "$TOKEN" ]; then
  echo "Set TOKEN to a Keycloak access token before running this test."
  exit 2
fi

for endpoint in public user admin; do
  curl --silent --show-error --output /dev/null \
    --write-out "$endpoint endpoint: HTTP %{http_code}\n" \
    -H "Authorization: Bearer $TOKEN" \
    "http://localhost:5000/api/$endpoint"
done
echo "Expected: guest=200/403, user=200/403, admin=200 on public/user/admin respectively."