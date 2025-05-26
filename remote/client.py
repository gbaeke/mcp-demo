"""Client to test the remote MCP server over HTTP."""

import asyncio
import os
from fastmcp import Client


async def test_remote_server():
    """Test the remote MCP server running over HTTP."""
    print("--- Testing Remote MCP Server ---")
    
    # Get the server URL from environment variable or use default
    server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp")
    print(f"Connecting to server: {server_url}")
    
    # Connect to the remote server via HTTP
    client = Client(server_url)
    
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
            
            # Test with a longer query to check streaming
            print("\n🔍 Testing search with longer query...")
            search_result = await client.call_tool("search", {"query": "How does OpenAI streaming API work with chunked transfer encoding"})
            
            # Print the result in chunks to simulate streaming
            result_text = search_result[0].text
            chunks = [result_text[i:i+50] for i in range(0, len(result_text), 50)]
            for chunk in chunks:
                print(chunk, end="", flush=True)
                await asyncio.sleep(0.1)  # Simulate streaming delay
            print("\n✅ Streaming test complete")
            
    except Exception as e:
        print(f"❌ Error connecting to remote server: {e}")
        print("Make sure the server is running with: python server.py")
        print("\nTo use with a dev tunnel:")
        print("1. Start the server: python server.py")
        print("2. Create a tunnel: devtunnel host -p 8000 --protocol https")
        print("3. Run the client with: MCP_SERVER_URL=https://your-tunnel-url.devtunnels.ms/mcp python client.py")


if __name__ == "__main__":
    asyncio.run(test_remote_server()) 