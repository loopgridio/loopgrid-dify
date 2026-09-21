from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.loopgrid_client import LoopGridClient, LoopGridError


class VerifyDecisionTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            client = LoopGridClient.from_credentials(self.runtime.credentials)
            decision_id = str(tool_parameters.get("decision_id") or "").strip()
            if not decision_id:
                raise ValueError("Decision ID is required")
            verification = client.get_json(client.decision_path(decision_id, "/verify"))
            yield self.create_json_message(json={
                "decision_id": decision_id,
                "verification": verification,
                "offline_verifier_used": False,
                "note": "Service-side verification. Use loopgrid-verify for independent offline evidence-bundle verification.",
            })
        except (ValueError, LoopGridError) as exc:
            yield self.create_text_message(text=str(exc))
