#!/usr/bin/env python3
"""
Blinkit MCP Server - AI Agent Interface for Blinkit API
Enables AI agents to interact with Blinkit grocery shopping API
"""

import asyncio
import os
import json
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

app = Server("blinkit-mcp")

# Configuration
API_BASE_URL = os.getenv('BLINKIT_API_URL', 'https://oxide-corresponding-ebony-disciplines.trycloudflare.com')
SESSION_ID = os.getenv('SESSION_ID', 'unknown')
USER_ID = os.getenv('USER_ID', 'unknown')

#print(f"[MCP] Blinkit MCP Server started", flush=True)
#print(f"[MCP] API URL: {API_BASE_URL}", flush=True)
#print(f"[MCP] Session ID: {SESSION_ID}, User ID: {USER_ID}", flush=True)


# EMBEDDED COST TRACKING
async def track_usage(tool_name: str, cost: float = 0.0):
    """Track tool usage and optionally deduct cost"""
 #   print(f"[USAGE] Tool '{tool_name}' used - user={USER_ID}, session={SESSION_ID}, cost=${cost:.4f}", flush=True)

    usage_log = {
        "user_id": USER_ID,
        "session_id": SESSION_ID,
        "tool": tool_name,
        "cost": cost,
        "timestamp": asyncio.get_event_loop().time()
    }

    # Log to file
    os.makedirs("logs", exist_ok=True)
    with open("logs/usage.jsonl", "a") as f:
        f.write(json.dumps(usage_log) + "\n")

    return True


# HTTP Client
async def api_call(method: str, endpoint: str, data: dict = None) -> dict:
    """Make API call to Blinkit API"""
    url = f"{API_BASE_URL}{endpoint}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if method == "GET":
                response = await client.get(url)
            elif method == "POST":
                response = await client.post(url, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e), "status": "failed"}


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available Blinkit tools"""
    return [
        # Authentication Tools
        Tool(
            name="blinkit_check_login",
            description="Check if currently logged in to Blinkit",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="blinkit_login",
            description="Login to Blinkit using phone number (will send OTP)",
            inputSchema={
                "type": "object",
                "properties": {
                    "phone_number": {
                        "type": "string",
                        "description": "10-digit phone number",
                    },
                },
                "required": ["phone_number"],
            },
        ),
        Tool(
            name="blinkit_verify_otp",
            description="Verify OTP received on phone to complete login",
            inputSchema={
                "type": "object",
                "properties": {
                    "otp": {
                        "type": "string",
                        "description": "OTP code received on phone",
                    },
                },
                "required": ["otp"],
            },
        ),

        # Search Tool
        Tool(
            name="blinkit_search",
            description="Search for products on Blinkit (e.g., milk, bread, eggs)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Product name or category to search for",
                    },
                },
                "required": ["query"],
            },
        ),

        # Cart Tools
        Tool(
            name="blinkit_add_to_cart",
            description="Add a product to cart using its product ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "Product ID from search results",
                    },
                    "quantity": {
                        "type": "number",
                        "description": "Quantity to add (default: 1)",
                        "default": 1,
                    },
                },
                "required": ["item_id"],
            },
        ),
        Tool(
            name="blinkit_remove_from_cart",
            description="Remove a product from cart",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "Product ID to remove",
                    },
                    "quantity": {
                        "type": "number",
                        "description": "Quantity to remove (default: 1)",
                        "default": 1,
                    },
                },
                "required": ["item_id"],
            },
        ),
        Tool(
            name="blinkit_get_cart",
            description="View current cart contents and total",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),

        # Checkout Tools
        Tool(
            name="blinkit_checkout",
            description="Proceed to checkout (starts address selection)",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="blinkit_get_addresses",
            description="Get list of saved delivery addresses",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="blinkit_select_address",
            description="Select a delivery address by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {
                        "type": "number",
                        "description": "Address index from the addresses list",
                    },
                },
                "required": ["index"],
            },
        ),
        Tool(
            name="blinkit_proceed_to_pay",
            description="Proceed to payment page after selecting address",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),

        # Payment Tools
        Tool(
            name="blinkit_get_upi_ids",
            description="Get available UPI payment options",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="blinkit_select_upi",
            description="Select a UPI ID for payment",
            inputSchema={
                "type": "object",
                "properties": {
                    "upi_id": {
                        "type": "string",
                        "description": "UPI ID (e.g., user@paytm)",
                    },
                },
                "required": ["upi_id"],
            },
        ),
        Tool(
            name="blinkit_pay_now",
            description="Click Pay Now to complete the transaction",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    #print(f"[MCP] Tool '{name}' called by user={USER_ID}", flush=True)

    # Authentication Tools
    if name == "blinkit_check_login":
        await track_usage("check_login", 0.001)
        result = await api_call("GET", "/auth/check-login")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "blinkit_login":
        await track_usage("login", 0.01)
        phone_number = arguments.get("phone_number")
        result = await api_call("POST", "/auth/login", {"phone_number": phone_number})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "blinkit_verify_otp":
        await track_usage("verify_otp", 0.01)
        otp = arguments.get("otp")
        result = await api_call("POST", "/auth/verify-otp", {"otp": otp})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    # Search Tool
    elif name == "blinkit_search":
        await track_usage("search", 0.02)
        query = arguments.get("query")
        result = await api_call("POST", "/search", {"query": query})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    # Cart Tools
    elif name == "blinkit_add_to_cart":
        await track_usage("add_to_cart", 0.01)
        item_id = arguments.get("item_id")
        quantity = arguments.get("quantity", 1)
        result = await api_call("POST", "/cart/add", {"item_id": item_id, "quantity": quantity})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "blinkit_remove_from_cart":
        await track_usage("remove_from_cart", 0.01)
        item_id = arguments.get("item_id")
        quantity = arguments.get("quantity", 1)
        result = await api_call("POST", "/cart/remove", {"item_id": item_id, "quantity": quantity})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "blinkit_get_cart":
        await track_usage("get_cart", 0.01)
        result = await api_call("GET", "/cart")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    # Checkout Tools
    elif name == "blinkit_checkout":
        await track_usage("checkout", 0.01)
        result = await api_call("POST", "/checkout")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "blinkit_get_addresses":
        await track_usage("get_addresses", 0.01)
        result = await api_call("GET", "/addresses")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "blinkit_select_address":
        await track_usage("select_address", 0.01)
        index = arguments.get("index")
        result = await api_call("POST", "/addresses/select", {"index": int(index)})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "blinkit_proceed_to_pay":
        await track_usage("proceed_to_pay", 0.01)
        result = await api_call("POST", "/checkout/proceed-to-pay")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    # Payment Tools
    elif name == "blinkit_get_upi_ids":
        await track_usage("get_upi_ids", 0.01)
        result = await api_call("GET", "/payment/upi-ids")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "blinkit_select_upi":
        await track_usage("select_upi", 0.01)
        upi_id = arguments.get("upi_id")
        result = await api_call("POST", "/payment/select-upi", {"upi_id": upi_id})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "blinkit_pay_now":
        await track_usage("pay_now", 0.05)
        result = await api_call("POST", "/payment/pay-now")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main entry point"""
   # print("[MCP] Starting Blinkit MCP Server...", flush=True)
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
