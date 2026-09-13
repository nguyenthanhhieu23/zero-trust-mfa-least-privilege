# SOURCE

This directory contains the demo application, network policy, firewall rules,
test scripts and evidence templates for the Zero Trust lab.

## Run the lab

From the repository root on a machine with Docker Desktop:

```bash
cp SETUP/.env.example SETUP/.env
bash SOURCE/scripts/setup.sh
bash SOURCE/scripts/test-connectivity.sh
```

On Windows PowerShell, copy the environment file with
`Copy-Item SETUP/.env.example SETUP/.env`, then run the Compose command from
`SETUP` with `docker compose up -d --build`.

The API uses Keycloak-signed JWTs and checks issuer, audience, signature and
realm roles. It is a demonstration component, not a production identity proxy.