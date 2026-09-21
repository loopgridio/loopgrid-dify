from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.loopgrid_client import LoopGridClient, LoopGridError, parse_json_object


class RecordDecisionTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            client = LoopGridClient.from_credentials(self.runtime.credentials)
            metadata = parse_json_object(tool_parameters.get("metadata_json"), "Metadata")
            metadata["source"] = "dify"
            body: dict[str, Any] = {
                "decision_type": str(tool_parameters.get("decision_type") or "agent_decision"),
                "service_name": str(tool_parameters.get("service_name") or "dify"),
                "workspace_id": client.workspace_id,
                "privacy_mode": str(tool_parameters.get("privacy_mode") or "redacted"),
                "agent": parse_json_object(tool_parameters.get("agent_json"), "Agent"),
                "authority": parse_json_object(tool_parameters.get("authority_json"), "Authority"),
                "model": parse_json_object(tool_parameters.get("model_json"), "Model"),
                "context": parse_json_object(tool_parameters.get("context_json"), "Context"),
                "input": parse_json_object(tool_parameters.get("input_json"), "Input Evidence"),
                "proposed_action": parse_json_object(tool_parameters.get("proposed_action_json"), "Proposed Action"),
                "metadata": metadata,
            }
            key = str(tool_parameters.get("idempotency_key") or "").strip()
            if key:
                body["idempotency_key"] = key
            result = client.post_json("/api/v1/decisions", body)
            result["action_executed_by_loopgrid"] = False
            yield self.create_json_message(json=result)
        except (ValueError, LoopGridError) as exc:
            yield self.create_text_message(text=str(exc))
