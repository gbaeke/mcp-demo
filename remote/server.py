"""Remote MCP Server with HTTP transport for search functionality."""

import os
import sys
import certifi
import json
import requests
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("../.env")

# Add startup message
print("Starting Remote Search MCP Server...", file=sys.stderr)

# Create MCP server
mcp = FastMCP(
    name="remote-search-server", 
    description="Remote MCP server with search functionality over HTTP"
)
print("Remote MCP server instance created", file=sys.stderr)

# Create a session with common headers
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
})


@mcp.tool()
def search(query: str) -> str:
    """
    Search the web for information using Serper API.

    Args:
        query: The query to search for
    
    Returns:
        Information about the query or error message
    """
    # Check if API key is set
    api_key = os.getenv('SERPER_API_KEY')
    if not api_key:
        error_msg = "Error: SERPER_API_KEY environment variable is not set"
        print(error_msg, file=sys.stderr)
        return error_msg
        
    try:
        # Create search payload with query
        payload = {
            "q": query,
            "num": 2
        }
        
        # Set headers with API key
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        
        # Make request
        response = session.post(
            "https://google.serper.dev/search",
            json=payload,
            headers=headers,
            verify=certifi.where(),
            timeout=10
        )
        response.raise_for_status()
        
        # Parse JSON and extract organic results
        results = response.json()
        organic_results = results.get("organic", [])
        
        if not organic_results:
            return "No results found for the query"
            
        # Format as plain text for optimal OpenAI responses API compatibility
        # Using extremely simple format to avoid any streaming/parsing issues
        result_text = f"Found {len(organic_results)} results for '{query}':\n\n"
        
        for idx, result in enumerate(organic_results):
            # Add each piece of information as a separate line for better streaming
            result_text += f"Result {idx+1}: {result.get('title', 'No title')}\n"
            result_text += f"{result.get('link', 'No link')}\n"
            result_text += f"{result.get('snippet', 'No snippet')}\n\n"
        
        # Return simple text format that's easier for streaming
        print(f"Returning {len(result_text)} characters of search results", file=sys.stderr)
        return result_text.strip()
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Error making API request: {str(e)}"
        print(error_msg, file=sys.stderr)
        return error_msg
    except json.JSONDecodeError as e:
        error_msg = f"Error parsing API response: {str(e)}"
        print(error_msg, file=sys.stderr)
        return error_msg
    except Exception as e:
        error_msg = f"Error occurred during search: {str(e)}"
        print(error_msg, file=sys.stderr)
        return error_msg


if __name__ == "__main__":
    print("\n--- Starting Remote FastMCP Server via HTTP ---", file=sys.stderr)
    # Run the server using streamable HTTP transport
    # This makes it accessible over HTTP instead of stdio
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
        path="/mcp",
        chunk_size=100,  # Small chunks for better streaming
        stream_mode="line"  # Stream line by line
    ) 
    