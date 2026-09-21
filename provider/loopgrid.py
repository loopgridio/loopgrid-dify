from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.loopgrid_client import LoopGridClient, LoopGridError


class LoopGridProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            client = LoopGridClient.from_credentials(credentials)
            client.get_json(
                "/api/v1/dashboard",
                params={"workspace_id": client.workspace_id},
            )
        except (ValueError, LoopGridError) as exc:
            raise ToolProviderCredentialValidationError(str(exc)) from exc
