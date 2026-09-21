from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.loopgrid_client import LoopGridClient, LoopGridError


class GetDecisionTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            client = LoopGridClient.from_credentials(self.runtime.credentials)
            decision_id = str(tool_parameters.get("decision_id") or "").strip()
            if not decision_id:
                raise ValueError("Decision ID is required")
            yield self.create_json_message(json=client.get_json(client.decision_path(decision_id)))
        except (ValueError, LoopGridError) as exc:
            yield self.create_text_message(text=str(exc))
