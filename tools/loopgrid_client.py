from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote, urlsplit

import requests


class LoopGridError(RuntimeError):
    pass


def parse_json_object(value: Any, label: str) -> dict[str, Any]:
    if value in (None, ""):
        return {}
    if isinstance(value, dict):
        return value
    try:
        parsed = json.loads(str(value))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} must be valid JSON") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"{label} must be a JSON object")
    return parsed


def _normalize_base_url(value: Any) -> str:
    base_url = str(value or "").strip().rstrip("/")
    parts = urlsplit(base_url)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise ValueError("LoopGrid Base URL must be a valid http:// or https:// URL")
    if parts.username or parts.password or parts.query or parts.fragment:
        raise ValueError("LoopGrid Base URL must not contain credentials, a query string, or a fragment")
    return base_url


def _safe_error(response: requests.Response) -> str:
    try:
        payload = response.json()
    except Exception:
        return (response.text or "request failed").strip()[:500]
    if isinstance(payload, dict):
        detail = payload.get("detail", payload)
        if isinstance(detail, str):
            return detail[:500]
        return json.dumps(detail, ensure_ascii=False)[:500]
    return str(payload)[:500]


@dataclass(frozen=True)
class LoopGridClient:
    base_url: str
    api_key: str
    workspace_id: str
    timeout: float = 20.0

    @classmethod
    def from_credentials(cls, credentials: dict[str, Any]) -> "LoopGridClient":
        api_key = str((credentials or {}).get("api_key") or "").strip()
        workspace_id = str((credentials or {}).get("workspace_id") or "default").strip()
        if not api_key:
            raise ValueError("LoopGrid API Key is required")
        if not workspace_id:
            raise ValueError("Workspace ID is required")
        return cls(
            base_url=_normalize_base_url((credentials or {}).get("base_url")),
            api_key=api_key,
            workspace_id=workspace_id,
        )

    def _request(self, method: str, path: str, *, body: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            response = requests.request(
                method,
                f"{self.base_url}{path}",
                headers={
                    "X-LoopGrid-Key": self.api_key,
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "User-Agent": "loopgrid-dify/0.1.0",
                },
                json=body,
                params=params,
                timeout=self.timeout,
                allow_redirects=False,
            )
        except requests.RequestException as exc:
            raise LoopGridError(f"Could not reach LoopGrid: {exc.__class__.__name__}") from exc
        if response.status_code >= 400:
            raise LoopGridError(f"LoopGrid returned HTTP {response.status_code}: {_safe_error(response)}")
        try:
            payload = response.json()
        except ValueError as exc:
            raise LoopGridError("LoopGrid returned a non-JSON response") from exc
        if not isinstance(payload, dict):
            raise LoopGridError("LoopGrid returned an unexpected response shape")
        return payload

    def get_json(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("GET", path, params=params)

    def post_json(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", path, body=body)

    @staticmethod
    def decision_path(decision_id: str, suffix: str = "") -> str:
        return f"/api/v1/decisions/{quote(str(decision_id), safe='')}{suffix}"
