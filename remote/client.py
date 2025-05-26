"""Client to test the remote MCP server over HTTP."""

import asyncio
from fastmcp import Client


async def test_remote_server():
    """Test the remote MCP server running over HTTP."""
    print("--- Testing Remote MCP Server ---")
    
    # Connect to the remote server via HTTP
    # The server should be running on http://localhost:8000/mcp
    # client = Client("http://localhost:8000/mcp")
    client = Client("https://d578-2a02-1812-c35-b400-3d2f-e5a3-be22-511f.ngrok-free.app/mcp")
    
    try:
        async with client:
            print("✅ Connected to remote MCP server")
            
            # List available tools
            tools = await client.list_tools()
            print(f"📋 Available tools: {[tool.name for tool in tools]}")
            
            # Test the search tool
            print("\n🔍 Testing search tool...")
            search_result = await client.call_tool("search", {"query": "FastMCP Python library"})
            print(f"🔍 Search result: {search_result[0].text[:200]}...")
            
    except Exception as e:
        print(f"❌ Error connecting to remote server: {e}")
        print("Make sure the server is running with: python server.py")


if __name__ == "__main__":
    asyncio.run(test_remote_server()) 