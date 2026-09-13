# Keycloak lab

Keycloak imports `realm-export.json` when the container starts for the first time.
Open `http://localhost:8080`, then use the admin credentials from `.env`.

The realm contains roles `admin`, `user`, and `guest`, plus a public client named
`zero-trust-demo`. Users must configure TOTP at their first login. For a real
deployment, replace all example passwords and keep secrets outside Git.