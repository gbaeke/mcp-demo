"""Search and scrape Server for Claude Desktop."""

import os
import sys
import certifi
import json
import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Dict, Optional

# Load environment variables from .env file
load_dotenv()

# Add startup message
print("Starting Search and Scrape MCP Server...", file=sys.stderr)

# Create MCP server
mcp = FastMCP(
    "search-and-scrape", 
    description="Search and scrape MCP server"
)
print("MCP server instance created", file=sys.stderr)

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
            
        # Return organic results
        return json.dumps(organic_results, indent=2)
        
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


@mcp.tool()
def scrape(url: str, include_metadata: bool = True) -> Dict:
    """
    Scrape content from a given URL.

    Args:
        url: The URL to scrape
        include_metadata: Whether to include page metadata (title, description, etc.)
    
    Returns:
        Dictionary containing the scraped content and metadata
    """
    try:
        # Make request with SSL verification
        response = session.get(
            url, 
            verify=certifi.where(),
            timeout=10
        )
        response.raise_for_status()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for element in soup(['script', 'style', 'iframe']):
            element.decompose()
            
        # Extract main content
        content = soup.get_text(separator='\n', strip=True)
        
        # Prepare result
        result = {
            "content": content[:5000],  # Limit content length
            "url": url,
            "status": response.status_code
        }
        
        # Add metadata if requested
        if include_metadata:
            metadata = {}
            
            # Get title
            title = soup.find('title')
            if title:
                metadata['title'] = title.string
                
            # Get meta description
            description = soup.find('meta', attrs={'name': 'description'})
            if description:
                metadata['description'] = description.get('content')
                
            # Get meta keywords
            keywords = soup.find('meta', attrs={'name': 'keywords'})
            if keywords:
                metadata['keywords'] = keywords.get('content')
                
            # Get Open Graph metadata
            og_title = soup.find('meta', property='og:title')
            if og_title:
                metadata['og_title'] = og_title.get('content')
                
            og_description = soup.find('meta', property='og:description')
            if og_description:
                metadata['og_description'] = og_description.get('content')
                
            result['metadata'] = metadata
            
        return result
        
    except requests.RequestException as e:
        error_msg = f"Error fetching URL: {str(e)}"
        print(error_msg, file=sys.stderr)
        return {"error": error_msg, "url": url}
    except Exception as e:
        error_msg = f"Error scraping content: {str(e)}"
        print(error_msg, file=sys.stderr)
        return {"error": error_msg, "url": url}


if __name__ == "__main__":
    # Run the server with stdio transport (default)
    print("Starting MCP server run...", file=sys.stderr)
    mcp.run()
