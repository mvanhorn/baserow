import json

from asgiref.sync import sync_to_async

from baserow.contrib.database import services
from baserow.core.mcp.registries import MCPTool


class ListDatabasesMcpTool(MCPTool):
    type = "list_databases"
    name = "list_databases"

    async def list(self, endpoint):
        from mcp import Tool

        return [
            Tool(
                name=self.name,
                description="List all databases in the workspace.",
                inputSchema={"type": "object", "properties": {}},
            )
        ]

    async def call(self, endpoint, call_arguments):
        from mcp.types import TextContent

        try:
            databases = await sync_to_async(services.list_databases)(
                endpoint.user, endpoint.workspace
            )
            data = [
                {"id": db.id, "name": db.name, "order": db.order} for db in databases
            ]
            return [TextContent(type="text", text=json.dumps(data))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]


class CreateDatabaseMcpTool(MCPTool):
    type = "create_database"
    name = "create_database"

    async def list(self, endpoint):
        from mcp import Tool

        return [
            Tool(
                name=self.name,
                description="Create a new database in the workspace.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the database to create.",
                        },
                    },
                    "required": ["name"],
                },
            )
        ]

    async def call(self, endpoint, call_arguments):
        from mcp.types import TextContent

        try:
            db = await sync_to_async(services.create_database)(
                endpoint.user, endpoint.workspace, call_arguments["name"]
            )
            data = {"id": db.id, "name": db.name}
            return [TextContent(type="text", text=json.dumps(data))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]


class ListTablesMcpTool(MCPTool):
    type = "list_tables"
    name = "list_tables"

    async def list(self, endpoint):
        from mcp import Tool

        return [
            Tool(
                name=self.name,
                description=(
                    "List all tables in the workspace, optionally filtered by database."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "database_id": {
                            "type": "integer",
                            "description": (
                                "If provided, only return tables from this database."
                            ),
                        },
                    },
                },
            )
        ]

    async def call(self, endpoint, call_arguments):
        from mcp.types import TextContent

        try:
            database_id = call_arguments.get("database_id")
            tables = await sync_to_async(services.list_tables)(
                endpoint.user, endpoint.workspace, database_id=database_id
            )
            data = [
                {
                    "id": t.id,
                    "name": t.name,
                    "order": t.order,
                    "database_id": t.database_id,
                }
                for t in tables
            ]
            return [TextContent(type="text", text=json.dumps(data))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]


class CreateTableMcpTool(MCPTool):
    type = "create_table"
    name = "create_table"

    async def list(self, endpoint):
        from mcp import Tool

        return [
            Tool(
                name=self.name,
                description=(
                    "Create a new table in a database, optionally with initial fields. "
                    "Fields are created in dependency order "
                    "(regular → link_row → lookup → formula)."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "database_id": {
                            "type": "integer",
                            "description": "The ID of the database to create the table in.",
                        },
                        "name": {
                            "type": "string",
                            "description": "The name of the table.",
                        },
                        "fields": {
                            "type": "array",
                            "description": (
                                "Optional list of additional fields. Each item must have "
                                "'name' and 'type'. Type-specific extras: "
                                "number_decimal_places (number), date_include_time (date), "
                                "select_options=[{value, color}] "
                                "(single_select/multiple_select), "
                                "link_row_table_id (link_row). "
                                "Valid types: text, long_text, number, boolean, date, "
                                "single_select, multiple_select, link_row, file, email, "
                                "url, phone_number, rating, formula, lookup."
                            ),
                            "items": {"type": "object"},
                        },
                    },
                    "required": ["database_id", "name"],
                },
            )
        ]

    async def call(self, endpoint, call_arguments):
        from mcp.types import TextContent

        try:
            result = await sync_to_async(services.create_table)(
                endpoint.user,
                endpoint.workspace,
                call_arguments["database_id"],
                call_arguments["name"],
                call_arguments.get("fields"),
            )
            return [TextContent(type="text", text=json.dumps(result))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]


class UpdateTableMcpTool(MCPTool):
    type = "update_table"
    name = "update_table"

    async def list(self, endpoint):
        from mcp import Tool

        return [
            Tool(
                name=self.name,
                description="Rename an existing table.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_id": {
                            "type": "integer",
                            "description": "The ID of the table to rename.",
                        },
                        "name": {
                            "type": "string",
                            "description": "The new name for the table.",
                        },
                    },
                    "required": ["table_id", "name"],
                },
            )
        ]

    async def call(self, endpoint, call_arguments):
        from mcp.types import TextContent

        try:
            result = await sync_to_async(services.update_table)(
                endpoint.user,
                endpoint.workspace,
                call_arguments["table_id"],
                call_arguments["name"],
            )
            return [TextContent(type="text", text=json.dumps(result))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]


class DeleteTableMcpTool(MCPTool):
    type = "delete_table"
    name = "delete_table"

    async def list(self, endpoint):
        from mcp import Tool

        return [
            Tool(
                name=self.name,
                description="Delete (trash) a table and all its rows.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_id": {
                            "type": "integer",
                            "description": "The ID of the table to delete.",
                        },
                    },
                    "required": ["table_id"],
                },
            )
        ]

    async def call(self, endpoint, call_arguments):
        from mcp.types import TextContent

        try:
            await sync_to_async(services.delete_table)(
                endpoint.user, endpoint.workspace, call_arguments["table_id"]
            )
            return [TextContent(type="text", text="Table successfully deleted.")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]


class GetTableSchemaMcpTool(MCPTool):
    type = "get_table_schema"
    name = "get_table_schema"

    async def list(self, endpoint):
        from mcp import Tool

        return [
            Tool(
                name=self.name,
                description=(
                    "Get the field schema for one or more tables. "
                    "Call this before create_rows or update_rows to learn the field "
                    "names and types accepted by those tools."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of table IDs to get the schema for.",
                        },
                    },
                    "required": ["table_ids"],
                },
            )
        ]

    async def call(self, endpoint, call_arguments):
        from mcp.types import TextContent

        try:
            schemas = await sync_to_async(services.get_table_schema)(
                endpoint.user, endpoint.workspace, call_arguments["table_ids"]
            )
            return [TextContent(type="text", text=json.dumps(schemas))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]


class CreateFieldsMcpTool(MCPTool):
    type = "create_fields"
    name = "create_fields"

    async def list(self, endpoint):
        from mcp import Tool

        return [
            Tool(
                name=self.name,
                description=(
                    "Add one or more fields to an existing table. "
                    "Fields are created in dependency order "
                    "(regular → link_row → lookup → formula)."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_id": {
                            "type": "integer",
                            "description": "The ID of the table to add fields to.",
                        },
                        "fields": {
                            "type": "array",
                            "description": (
                                "List of fields to create. Each item must have 'name' "
                                "and 'type'. See create_table for valid types and extras."
                            ),
                            "items": {"type": "object"},
                        },
                    },
                    "required": ["table_id", "fields"],
                },
            )
        ]

    async def call(self, endpoint, call_arguments):
        from mcp.types import TextContent

        try:
            created = await sync_to_async(services.create_fields)(
                endpoint.user,
                endpoint.workspace,
                call_arguments["table_id"],
                call_arguments["fields"],
            )
            return [TextContent(type="text", text=json.dumps(created))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]


class UpdateFieldsMcpTool(MCPTool):
    type = "update_fields"
    name = "update_fields"

    async def list(self, endpoint):
        from mcp import Tool

        return [
            Tool(
                name=self.name,
                description="Update one or more existing fields.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "fields": {
                            "type": "array",
                            "description": (
                                "List of field updates. Each item must have 'id' "
                                "plus the properties to change (name, type, "
                                "or type-specific options)."
                            ),
                            "items": {"type": "object"},
                        },
                    },
                    "required": ["fields"],
                },
            )
        ]

    async def call(self, endpoint, call_arguments):
        from mcp.types import TextContent

        try:
            updated = await sync_to_async(services.update_fields)(
                endpoint.user, endpoint.workspace, call_arguments["fields"]
            )
            return [TextContent(type="text", text=json.dumps(updated))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]


class DeleteFieldsMcpTool(MCPTool):
    type = "delete_fields"
    name = "delete_fields"

    async def list(self, endpoint):
        from mcp import Tool

        return [
            Tool(
                name=self.name,
                description="Delete (trash) one or more fields by ID.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "field_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of field IDs to delete.",
                        },
                    },
                    "required": ["field_ids"],
                },
            )
        ]

    async def call(self, endpoint, call_arguments):
        from mcp.types import TextContent

        try:
            await sync_to_async(services.delete_fields)(
                endpoint.user, endpoint.workspace, call_arguments["field_ids"]
            )
            return [TextContent(type="text", text="Fields successfully deleted.")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]
