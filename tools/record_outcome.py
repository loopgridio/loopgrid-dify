from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.loopgrid_client import LoopGridClient, LoopGridError, parse_json_object


class RecordOutcomeTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            client = LoopGridClient.from_credentials(self.runtime.credentials)
            decision_id = str(tool_parameters.get("decision_id") or "").strip()
            if not decision_id:
                raise ValueError("Decision ID is required")
            payload = parse_json_object(tool_parameters.get("details_json"), "Outcome Details")
            payload["status"] = str(tool_parameters.get("status") or "unknown")
            payload["verified_against"] = str(tool_parameters.get("verified_against") or "external-system")
            ref = str(tool_parameters.get("external_reference") or "").strip()
            if ref:
                payload["external_reference"] = ref
            body: dict[str, Any] = {
                "event_type": "outcome_observed",
                "actor_type": "integration",
                "actor_id": str(tool_parameters.get("actor_id") or "dify"),
                "payload": payload,
            }
            key = str(tool_parameters.get("idempotency_key") or "").strip()
            if key:
                body["idempotency_key"] = key
            event = client.post_json(client.decision_path(decision_id, "/events"), body)
            yield self.create_json_message(json={"decision_id": decision_id, "recorded": True, "event": event})
        except (ValueError, LoopGridError) as exc:
            yield self.create_text_message(text=str(exc))
