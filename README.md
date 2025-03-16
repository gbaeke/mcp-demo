# Search and Scrape MCP Server

A Claude Desktop MCP server that provides web search and content scraping capabilities. This server enables Claude to search the web using the Serper API and scrape content from web pages.

## Features

- **Web Search**: Search the web using Google Search results via Serper API
- **Web Scraping**: Extract content and metadata from any web page
- **Metadata Extraction**: Retrieve page titles, descriptions, keywords, and Open Graph metadata
- **Error Handling**: Robust error handling for network issues and invalid responses
- **SSL Security**: Secure HTTPS connections with proper certificate verification

## Prerequisites

- Python 3.7+
- A Serper API key (get one at [serper.dev](https://serper.dev))

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies using uv:
```bash
uv pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Serper API key:
```
SERPER_API_KEY=your_api_key_here
```

## Usage

### Use the server in Claude Desktop

Edit the following file: claude_desktop_config.json (use Developer Settings in Claude Desktop to find this file)

My file looks like this:

```json
{
    "mcpServers": {
        "search": {
            "command": "/usr/local/bin/uv",
            "args": [
                "--directory",
                "/Users/geertbaeke/projects/mcp-demo",
                "run",
                "main.py"
            ]
        }
    }
}
```

### Available Tools

#### 1. Search Tool
Searches the web using Serper API:

```python
search(query: str) -> str
```

Example response:
```json
[
  {
    "title": "Search Result Title",
    "link": "https://example.com",
    "snippet": "Result description..."
  }
]
```

#### 2. Scrape Tool
Scrapes content and metadata from a URL:

```python
scrape(url: str, include_metadata: bool = True) -> Dict
```

Example response:
```json
{
  "content": "Page content...",
  "url": "https://example.com",
  "status": 200,
  "metadata": {
    "title": "Page Title",
    "description": "Page description",
    "keywords": "key, words",
    "og_title": "OpenGraph Title",
    "og_description": "OpenGraph Description"
  }
}
```
