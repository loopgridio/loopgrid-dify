# LoopGrid for Dify

Dify Tool Plugin for recording and verifying signed, tamper-evident evidence around consequential AI-agent decisions.

## What it does

The plugin exposes six tools:

- `loopgrid_record_decision`
- `loopgrid_record_action`
- `loopgrid_record_outcome`
- `loopgrid_submit_review`
- `loopgrid_get_decision`
- `loopgrid_verify_decision`

**LoopGrid records evidence. It does not execute payments, refunds, transfers, account changes, or other external business actions.** Use the appropriate Dify/external tool for the action, then record the resulting action/outcome in LoopGrid.

## Credentials

Configure:

1. LoopGrid Base URL — a reachable LoopGrid deployment. HTTPS is recommended.
2. Workspace ID.
3. LoopGrid API Key.

For all six tools in one credential, use only the `ingest`, `read`, and `review` scopes. Prefer least privilege if you only need a subset.

## Recommended workflow

```text
Agent / model
  -> LoopGrid Record Decision
  -> explicit approval/policy workflow when required
  -> external action tool
  -> LoopGrid Record Action
  -> observe result
  -> LoopGrid Record Outcome
  -> LoopGrid Verify Decision
```

For reliable evidence capture, place the LoopGrid tools explicitly in a Workflow/Chatflow rather than relying on an LLM to decide whether logging is optional.

## Privacy and data minimization

The plugin sends only the fields the Dify workflow supplies to the configured LoopGrid endpoint. It does not automatically read conversations, files, environment variables, or unrelated Dify data. `Record Decision` defaults to `redacted` privacy mode.

See `PRIVACY.md` for details.

## Development / remote debugging

Requires Python 3.12 for the current plugin SDK line.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Fill REMOTE_INSTALL_URL and REMOTE_INSTALL_KEY from Dify's plugin debug UI
python -m main
```

## Tests

```powershell
python -m unittest discover -s tests -v
python -m compileall main.py provider tools
```

## Packaging

Use the official Dify plugin CLI, not a hand-made ZIP:

```powershell
dify plugin package .
```

Before Marketplace submission, validate the generated `.difypkg` with Dify's marketplace validator and inspect it to ensure it contains no `.env`, secrets, caches, virtualenv, tests, or local logs.

## Marketplace risk disclosure

This plugin uses a **user-configured LoopGrid Base URL** so it can work with self-hosted LoopGrid deployments. Under current Dify Marketplace rules, that is a user-controlled network destination and must be disclosed conservatively in the Marketplace PR. Do not mark it low risk merely to speed review.

## Independent verification

`loopgrid_verify_decision` performs service-side verification against the connected LoopGrid deployment. For independent/offline verification of an exported evidence bundle, use `loopgrid-verify` separately.

## Support / source

Source: https://github.com/loopgridio/loopgrid-dify

Support: https://github.com/loopgridio/loopgrid-dify/issues

LoopGrid core: https://github.com/cybertechsoft/loopgrid

## License

Apache-2.0.
