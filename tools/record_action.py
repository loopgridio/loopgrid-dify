from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.loopgrid_client import LoopGridClient, LoopGridError, parse_json_object


class RecordActionTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            client = LoopGridClient.from_credentials(self.runtime.credentials)
            decision_id = str(tool_parameters.get("decision_id") or "").strip()
            if not decision_id:
                raise ValueError("Decision ID is required")
            payload = parse_json_object(tool_parameters.get("details_json"), "Action Details")
            payload["tool"] = str(tool_parameters.get("tool") or "").strip()
            ref = str(tool_parameters.get("external_reference") or "").strip()
            if ref:
                payload["external_reference"] = ref
            body: dict[str, Any] = {
                "event_type": "tool_executed",
                "actor_type": "tool",
                "actor_id": str(tool_parameters.get("actor_id") or "external-system"),
                "payload": payload,
            }
            key = str(tool_parameters.get("idempotency_key") or "").strip()
            if key:
                body["idempotency_key"] = key
            event = client.post_json(client.decision_path(decision_id, "/events"), body)
            yield self.create_json_message(json={"decision_id": decision_id, "recorded": True, "action_executed_by_loopgrid": False, "event": event})
        except (ValueError, LoopGridError) as exc:
            yield self.create_text_message(text=str(exc))
