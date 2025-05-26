import httpx
from fastmcp import FastMCP
import copy
import sys

# Create an HTTP client for your API
client = httpx.AsyncClient(base_url="https://ca-lightsapi.salmoncliff-02f8b83d.westeurope.azurecontainerapps.io", timeout=60)

# Load your OpenAPI spec 
openapi_spec = httpx.get("https://ca-lightsapi.salmoncliff-02f8b83d.westeurope.azurecontainerapps.io/openapi.json", timeout=60).json()

# Fix the invalid OpenAPI spec
def fix_openapi_spec(spec):
    """Fix common OpenAPI spec issues that cause validation errors."""
    spec = copy.deepcopy(spec)
    
    # Fix the examples format in parameters
    for path_name, path_item in spec.get("paths", {}).items():
        for method_name, operation in path_item.items():
            if "parameters" in operation:
                for param in operation["parameters"]:
                    if "schema" in param and "examples" in param["schema"]:
                        examples = param["schema"]["examples"]
                        # Convert object examples to array format
                        if isinstance(examples, dict):
                            # Take the values from the dict and make them an array
                            param["schema"]["examples"] = list(examples.values())
    
    return spec

# Fix the OpenAPI spec before using it
fixed_openapi_spec = fix_openapi_spec(openapi_spec)

# Create the MCP server
mcp = FastMCP.from_openapi(
    openapi_spec=fixed_openapi_spec,
    client=client,
    name="Light API"
)

if __name__ == "__main__":
    print("\n--- Starting Remote FastMCP Server via HTTP ---", file=sys.stderr)
    # Run the server using streamable HTTP transport
    # This makes it accessible over HTTP instead of stdio
    mcp.run(
        transport="streamable-http",  # this is new and is preferred over sse
        host="0.0.0.0",
        port=8888,
        path="/lights"
    ) 