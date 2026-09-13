#!/usr/bin/env bash
set -euo pipefail

echo "Manual MFA test:"
echo "1. Open http://localhost:8080 and select realm zero-trust."
echo "2. Login as user, admin or guest with the lab password."
echo "3. Configure TOTP when Keycloak requests CONFIGURE_TOTP."
echo "4. Logout, login again, and verify a wrong OTP is rejected."