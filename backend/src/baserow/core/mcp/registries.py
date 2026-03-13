from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union

from baserow.core.mcp.models import MCPEndpoint
from baserow.core.registry import Instance, Registry

if TYPE_CHECKING:
    from mcp import Tool
    from mcp.types import EmbeddedResource, ImageContent, TextContent


class MCPTool(Instance):
    name = None
    """Unique name of the tool used for routing."""

    def get_name(self):
        if self.name is None:
            raise NotImplementedError(
                "Either the `name` property or `get_name` method must be implemented."
            )
        return self.name

    async def list(self, endpoint: MCPEndpoint) -> List["Tool"]:
        """
        :param endpoint: The endpoint related to the request.
        :return: List of available tools for this user.
        """
        raise NotImplementedError("The `list` method must be implemented.")

    async def call(
        self,
        endpoint: MCPEndpoint,
        call_arguments: Dict[str, Any],
    ) -> Sequence[Union["TextContent", "ImageContent", "EmbeddedResource"]]:
        """
        :param endpoint: The endpoint related to the authenticated user.
        :param call_arguments: A dict containing the tool call arguments.
        :return: The response content.
        """
        raise NotImplementedError("The `call` method must be implemented.")


class MCPToolRegistry(Registry[MCPTool]):
    name = "mcp_tools"

    async def list_all_tools(self, endpoint: MCPEndpoint) -> List["Tool"]:
        """Return all tools available to the given endpoint user."""
        all_tools = []
        for mcp in self.registry.values():
            tools = await mcp.list(endpoint)
            all_tools.extend(tools)
        return all_tools

    def match_by_name(self, name: str) -> Optional[MCPTool]:
        """Return the tool registered under ``name``, or None."""
        return self.registry.get(name)


mcp_tool_registry = MCPToolRegistry()
