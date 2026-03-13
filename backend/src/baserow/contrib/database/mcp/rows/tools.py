import json

from asgiref.sync import sync_to_async

from baserow.contrib.database import services
from baserow.contrib.database.table.models import Table
from baserow.core.mcp.registries import MCPTool


class ListRowsMcpTool(MCPTool):
    type = "list_table_rows"
    name = "list_table_rows"

    async def list(self, endpoint):
        from mcp import Tool

        return [
            Tool(
                name=self.name,
                description="List rows from a table with optional search and pagination.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_id": {
                            "type": "integer",
                            "description": "The ID of the table to list rows from.",
                        },
                        "search": {
                            "type": "string",
                            "description": "Optional search term to filter rows.",
                        },
                        "page": {
                            "type": "integer",
                            "default": 1,
                            "description": "Page number (1-based).",
                        },
                        "size": {
                            "type": "integer",
                            "default": 100,
                            "description": "Maximum number of rows to return.",
                        },
                    },
                    "required": ["table_id"],
                },
            )
        ]

    async def call(self, endpoint, call_arguments):
        from mcp.types import TextContent

        try:
            result = await sync_to_async(services.list_rows)(
                endpoint.user,
                endpoint.workspace,
                call_arguments["table_id"],
                search=call_arguments.get("search", ""),
                page=call_arguments.get("page", 1),
                size=call_arguments.get("size", 100),
            )
            return [TextContent(type="text", text=json.dumps(result))]
        except Table.DoesNotExist:
            return [
                TextContent(
                    type="text",
                    text="Table not found or not in endpoint workspace.",
                )
            ]


class CreateRowsMcpTool(MCPTool):
    type = "create_rows"
    name = "create_rows"

    async def list(self, endpoint):
        from mcp import Tool

        return [
            Tool(
                name=self.name,
                description=(
                    "Create one or more rows in a table. "
                    "Call get_table_schema first to learn the field names and types."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_id": {
                            "type": "integer",
                            "description": "The ID of the table to create rows in.",
                        },
                        "rows": {
                            "type": "array",
                            "description": (
                                "List of rows to create. Each row is an object "
                                "mapping field name to value."
                            ),
                            "items": {"type": "object"},
                        },
                    },
                    "required": ["table_id", "rows"],
                },
            )
        ]

    async def call(self, endpoint, call_arguments):
        from mcp.types import TextContent

        try:
            created = await sync_to_async(services.create_rows)(
                endpoint.user,
                endpoint.workspace,
                call_arguments["table_id"],
                call_arguments["rows"],
            )
            return [TextContent(type="text", text=json.dumps(created))]
        except Table.DoesNotExist:
            return [
                TextContent(
                    type="text",
                    text="Table not found or not in endpoint workspace.",
                )
            ]
        except ValueError as e:
            return [TextContent(type="text", text=f"Invalid field name: {e}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]


class UpdateRowsMcpTool(MCPTool):
    type = "update_rows"
    name = "update_rows"

    async def list(self, endpoint):
        from mcp import Tool

        return [
            Tool(
                name=self.name,
                description=(
                    "Update one or more existing rows in a table. "
                    "Each row must include 'id' plus the fields to update. "
                    "Call get_table_schema first to learn the field names."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_id": {
                            "type": "integer",
                            "description": "The ID of the table containing the rows.",
                        },
                        "rows": {
                            "type": "array",
                            "description": (
                                "List of rows to update. Each row must have 'id' "
                                "plus the field names and their new values."
                            ),
                            "items": {"type": "object"},
                        },
                    },
                    "required": ["table_id", "rows"],
                },
            )
        ]

    async def call(self, endpoint, call_arguments):
        from mcp.types import TextContent

        try:
            updated = await sync_to_async(services.update_rows)(
                endpoint.user,
                endpoint.workspace,
                call_arguments["table_id"],
                call_arguments["rows"],
            )
            return [TextContent(type="text", text=json.dumps(updated))]
        except Table.DoesNotExist:
            return [
                TextContent(
                    type="text",
                    text="Table not found or not in endpoint workspace.",
                )
            ]
        except ValueError as e:
            return [TextContent(type="text", text=f"Invalid field name: {e}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]


class DeleteRowsMcpTool(MCPTool):
    type = "delete_rows"
    name = "delete_rows"

    async def list(self, endpoint):
        from mcp import Tool

        return [
            Tool(
                name=self.name,
                description="Delete one or more rows from a table by ID.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_id": {
                            "type": "integer",
                            "description": "The ID of the table to delete rows from.",
                        },
                        "row_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of row IDs to delete.",
                        },
                    },
                    "required": ["table_id", "row_ids"],
                },
            )
        ]

    async def call(self, endpoint, call_arguments):
        from mcp.types import TextContent

        try:
            await sync_to_async(services.delete_rows)(
                endpoint.user,
                endpoint.workspace,
                call_arguments["table_id"],
                call_arguments["row_ids"],
            )
            return [TextContent(type="text", text="Rows successfully deleted.")]
        except Table.DoesNotExist:
            return [
                TextContent(
                    type="text",
                    text="Table not found or not in endpoint workspace.",
                )
            ]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]
