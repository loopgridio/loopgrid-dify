from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.loopgrid_client import LoopGridClient, LoopGridError


class SubmitReviewTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            client = LoopGridClient.from_credentials(self.runtime.credentials)
            decision_id = str(tool_parameters.get("decision_id") or "").strip()
            reviewer = str(tool_parameters.get("reviewer") or "").strip()
            action = str(tool_parameters.get("action") or "").strip()
            if not decision_id or not reviewer or action not in {"approve", "reject"}:
                raise ValueError("Decision ID, reviewer, and a valid approve/reject action are required")
            result = client.post_json(client.decision_path(decision_id, "/review"), {
                "action": action,
                "reviewer": reviewer,
                "reason": str(tool_parameters.get("reason") or ""),
            })
            yield self.create_json_message(json=result)
        except (ValueError, LoopGridError) as exc:
            yield self.create_text_message(text=str(exc))
