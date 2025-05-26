# Remote MCP Server

This directory contains a remote MCP server implementation using FastMCP with HTTP transport. Unlike the main server that uses stdio transport, this server runs over HTTP and can be accessed remotely.

## Features

- **HTTP Transport**: Uses FastMCP's streamable HTTP transport for remote access
- **Search Tool**: Implements web search functionality using the Serper API
- **Stateless**: Designed to be stateless and suitable for deployment

## Setup

1. **Install Dependencies**:
   ```bash
   cd remote
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Create a `.env` file in this directory with your Serper API key:
   ```
   SERPER_API_KEY=your_serper_api_key_here
   ```

## Running the Server

Start the remote MCP server:

```bash
python server.py
```

The server will start on `http://localhost:8000/mcp` by default.

You should see output like:
```
Starting Remote Search MCP Server...
Remote MCP server instance created
--- Starting Remote FastMCP Server via HTTP ---
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## Testing the Server

Run the test client to verify the server is working:

```bash
python client.py
```

This will:
1. Connect to the remote server
2. List available tools
3. Test the search functionality

## Using with MCP Clients

To use this remote server with MCP clients like Claude Desktop, you'll need to configure them to connect to the HTTP endpoint instead of running a local process.

### Example Configuration

For clients that support remote MCP servers, use:
- **URL**: `http://localhost:8000/mcp`
- **Transport**: Streamable HTTP

## Transport Types: Streamable-HTTP vs SSE

This server uses the **streamable-http** transport, which is the modern, recommended approach for remote MCP servers. Here's how it compares to the older SSE transport:

### Streamable-HTTP (Current - Recommended)
- **Single Endpoint**: Uses one endpoint (`/mcp`) that handles both GET and POST methods
- **Flexible Session Management**: Session ID passed in headers, supports both stateful and stateless modes
- **Infrastructure Friendly**: Works seamlessly with load balancers, proxies, and existing HTTP infrastructure
- **Resumable Connections**: Better support for connection recovery and message redelivery
- **Simplified Implementation**: Easier to implement and maintain
- **Future-Proof**: Active development focus, will receive ongoing improvements

### SSE (Server-Sent Events - Deprecated)
- **Multiple Endpoints**: Required separate endpoints for connection (`/sse`) and messaging (`/messages`)
- **Rigid Structure**: More complex connection flow with specific endpoint requirements
- **Query Parameters**: Session ID passed as query parameters
- **Limited Flexibility**: Less adaptable to different deployment scenarios
- **Being Phased Out**: No longer recommended for new implementations

### Why Streamable-HTTP is Better

1. **Stateless Support**: Can operate without maintaining server-side session state, perfect for serverless deployments
2. **Better Scalability**: Single endpoint design simplifies load balancing and horizontal scaling
3. **Infrastructure Compatibility**: "Just HTTP" - works with any HTTP infrastructure without special considerations
4. **Simplified Client Implementation**: Clients only need to know one endpoint URL
5. **Enhanced Reliability**: Built-in support for connection resumption and message recovery

### Recommendation

**Always use streamable-http for new remote MCP servers.** The SSE transport is deprecated and will be removed in future versions. Streamable-HTTP provides all the benefits of SSE while addressing its limitations and adding new capabilities.

## Key Differences from Local Server

1. **Transport**: Uses `streamable-http` instead of `stdio`
2. **Network Access**: Accessible over HTTP, not just local processes
3. **Deployment Ready**: Can be deployed to cloud platforms
4. **Stateless**: No session state maintained between requests

## Deployment

This server can be deployed to various platforms:

- **Local Development**: Run directly with `python server.py`
- **Cloud Platforms**: Deploy to services like Heroku, Railway, or cloud providers
- **Docker**: Can be containerized for consistent deployment
- **Serverless**: Compatible with serverless platforms that support HTTP endpoints

## Configuration Options

You can customize the server by modifying the `mcp.run()` call in `server.py`:

```python
mcp.run(
    transport="streamable-http",
    host="0.0.0.0",  # Listen on all interfaces for deployment
    port=8000,       # Change port as needed
    path="/mcp"      # Custom endpoint path
)
```

## Security Considerations

When deploying remotely:
- Use HTTPS in production
- Implement authentication if needed
- Consider rate limiting
- Validate all inputs
- Use environment variables for sensitive data 


## Testing with MCP Inspector

Run `npx @modelcontextprotocol/inspector' and open the web ui. In the UI:

- set transport to `streamable-http`
- set url to `http://localhost:8000/mcp`

Go to tools and list them. The search tool should be listed and you can call it.