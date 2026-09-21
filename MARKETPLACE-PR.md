# Plugin Submission

## Plugin information

- Author: loopgridio
- Plugin name: LoopGrid
- Version: 0.1.0
- Source repository: https://github.com/loopgridio/loopgrid-dify
- Contact: https://github.com/loopgridio/loopgrid-dify/issues

## Submission type

- [x] New plugin
- [ ] Version update

## What changed

Initial LoopGrid Tool Plugin release. It provides six evidence operations: record decision, record external action, record outcome, submit human review, get decision evidence, and verify a decision through the connected LoopGrid service.

The plugin records evidence only and does not execute the underlying business action.

## Risk level

- [ ] Low risk
- [ ] Medium risk
- [x] High risk

## Required checks

- [x] I have read and followed the Marketplace submission requirements.
- [x] I have read and comply with the Plugin Developer Agreement.
- [ ] I tested this plugin on Dify Community Edition and Dify Cloud, or documented any limitation below.
- [x] The package contains only files needed at runtime.
- [x] The package does not contain secrets, local credentials, `.env` files, `.git` directories, virtual environments, caches, logs, or IDE files.
- [x] The package does not contain executables or bundled binaries.
- [x] The plugin README includes setup steps, usage instructions, required APIs or credentials, connection requirements, and the source repository link.
- [x] The plugin includes `PRIVACY.md` and `manifest.yaml` references it.
- [x] All user-facing text is primarily in English.

## Security and privacy notes

The plugin sends only workflow-selected evidence fields to a LoopGrid endpoint configured in provider credentials. The API key is sent only via the `X-LoopGrid-Key` header and is not intentionally emitted in results/errors.

The Base URL is configurable to support self-hosted LoopGrid. Because this is a user-controlled network destination, the submission is conservatively marked **High risk** under the current Marketplace classification. Requests have a fixed timeout and redirects are disabled.

The plugin does not execute code, SQL, shell commands, filesystem operations, browser automation, payments, refunds, or asset transfers.

## Local validation

Before submission replace this section with actual results from:

- Dify remote-debug run
- Dify Community Edition tool execution for all six tools
- Dify Cloud test or documented network limitation
- official `dify plugin package .`
- Dify Marketplace `.difypkg` validator output

## Reviewer notes

A reviewer needs a reachable LoopGrid HTTP(S) endpoint, a workspace ID, and a restricted service key. For all six operations the test key needs `ingest`, `read`, and `review` scopes. Synthetic test data is sufficient.
