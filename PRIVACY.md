# Privacy Policy — LoopGrid Dify Plugin

Last updated: 2026-09-21

## Purpose

The LoopGrid Dify Plugin sends evidence fields explicitly supplied by a Dify workflow or agent tool call to the LoopGrid endpoint configured by the user. It is designed to record and retrieve evidence about AI-agent decisions, reviews, external actions, outcomes, and verification state.

## Data processed

Depending on how the workflow is configured, the plugin may process:

- decision identifiers and decision type;
- explicitly mapped agent/model/context/input metadata;
- proposed-action metadata;
- reviewer identity and review reason;
- external action/outcome references and selected details;
- the LoopGrid API key and workspace identifier used for authentication.

The plugin does not automatically read unrelated Dify conversations, files, environment variables, credentials, or datasets.

## Where data is sent

Data is sent over HTTP(S) to the **LoopGrid Base URL configured by the user**. This may be a self-hosted or separately hosted LoopGrid deployment. The plugin does not send workflow data to any other third-party endpoint on its own.

Because the destination is user-configurable, operators are responsible for choosing a trusted endpoint and using HTTPS for remote deployments.

## Credential handling

The LoopGrid API key is read from Dify provider credentials and placed only in the `X-LoopGrid-Key` request header. The plugin does not intentionally include the key in tool output or error messages.

## Storage and retention

The plugin itself does not maintain an independent database or durable cache. Evidence sent to LoopGrid is stored/retained according to the configuration and policies of the connected LoopGrid deployment. Dify may retain workflow/tool execution information according to the operator's Dify configuration.

## Sensitive data

Do not map sensitive or regulated data unless the connected LoopGrid deployment and your organizational policies explicitly allow it. Prefer LoopGrid `redacted` or `proof_only` capture modes where appropriate.

## External actions

This plugin does not execute payments, refunds, transfers, account changes, or other external business actions. It records evidence supplied by the workflow.

## Contact

Source and support: https://github.com/loopgridio/loopgrid-dify/issues

Security information: https://loopgrid.io/security/
