# 1Password access for local agents

## Purpose

Local agents can read operational secrets from 1Password without depending on
the desktop app session. The access is for local development and validation.
It is not a production runtime identity.

## Access boundary

- 1Password account: `Adrez Living`
- Service account: `Codex Data Platform Local`
- Permission: read-only
- Allowed vaults: `Data Platform`, `API Users`
- All other vaults: no access

Do not expand this scope as part of another task. Change the service account in
1Password Administration only after Martin approves the new vault and purpose.

## Local configuration

The token is stored outside every repository:

```text
~/.config/adrez/1password-codex-service-account.token
```

The file must have mode `600`. The shell exposes only its path:

```sh
export ADREZ_1PASSWORD_SERVICE_ACCOUNT_TOKEN_FILE="$HOME/.config/adrez/1password-codex-service-account.token"
```

Do not persist `OP_SERVICE_ACCOUNT_TOKEN` in a shell profile. Load it only for
the process that calls `op`:

```sh
OP_SERVICE_ACCOUNT_TOKEN="$(cat "$ADREZ_1PASSWORD_SERVICE_ACCOUNT_TOKEN_FILE")" \
  op vault list
```

Never echo the token. Never enable shell tracing around commands that load it.

## Agent use

Before a task reads a secret:

1. Confirm that the requested item is in `Data Platform` or `API Users`.
2. Confirm that the token file exists and has mode `600`.
3. Pass the token only to the required `op` process.
4. Use an `op://` reference or a repository wrapper when one exists.
5. Keep secret values out of command output, logs, patches, and chat.

Repositories can read
`ADREZ_1PASSWORD_SERVICE_ACCOUNT_TOKEN_FILE`. Current Compose helpers use this
variable to resolve 1Password references without copying the token into a repo.

For `test on local Airflow` and equivalent requests, this service account is
the default authentication path. Follow
`../../airflow-orchestrator/docs/test-airflow-locally.md`. Do not ask for an
interactive 1Password session when the standard token file exists and passes
the checks below.

## Safe verification

This check reports file state and accessible vault names. It does not print the
token:

```sh
test -s "$ADREZ_1PASSWORD_SERVICE_ACCOUNT_TOKEN_FILE"
test "$(stat -f '%Lp' "$ADREZ_1PASSWORD_SERVICE_ACCOUNT_TOKEN_FILE")" = 600
OP_SERVICE_ACCOUNT_TOKEN="$(cat "$ADREZ_1PASSWORD_SERVICE_ACCOUNT_TOKEN_FILE")" \
  op vault list --format=json \
  | jq -r '.[].name' \
  | sort
```

The final output must contain exactly:

```text
API Users
Data Platform
```

## Change or rotation

Manage the identity in the Adrez Living 1Password web app:

`Developer tools` -> `Infrastructure Secrets` -> `Service Accounts` ->
`Codex Data Platform Local`

To rotate the token:

1. Create a replacement token for the same service account and vault scope.
2. Write it to a temporary file with `umask 077`.
3. Replace the token file atomically.
4. Verify file mode and the two accessible vault names.
5. Revoke the old token in 1Password.

If the file path changes, update the export in `~/.zshrc` and this document.
If the allowed vaults change, update the access boundary and verification list
in this document.
