"""Example OpenAI responses API client for testing the MCP server."""

import os
from openai import OpenAI
import argparse

def test_openai_responses():
    """Test the MCP server with OpenAI responses API."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Test MCP server with OpenAI responses API')
    parser.add_argument('--server-url', type=str, default=os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp"),
                        help='MCP server URL')
    parser.add_argument('--query', type=str, default="What is the FastMCP library?",
                        help='Query to search for')
    args = parser.parse_args()
    
    print(f"Using MCP server URL: {args.server_url}")
    print(f"Query: {args.query}")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create a prompt with instructions to use the search tool
    prompt = f"""
    Please use the search tool to find information about: {args.query}
    
    Then summarize the search results in a clear and concise way.
    """
    
    print("\nSending request to OpenAI with MCP tool configuration...")
    
    # Create response with MCP tool configuration
    resp = client.responses.create(
        model="gpt-4.1",
        tools=[
            {
                "type": "mcp",
                "server_label": "search",
                "server_url": args.server_url,
                "require_approval": "never",
            },
        ],
        input=prompt,
    )
    
    print("Streaming response from OpenAI:")
    print("-" * 40)
    
    # Stream the response
    for chunk in resp:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    
    print("\n" + "-" * 40)
    print("Response complete")


if __name__ == "__main__":
    test_openai_responses()