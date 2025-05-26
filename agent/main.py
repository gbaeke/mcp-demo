from openai import OpenAI
from dotenv import load_dotenv
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.markdown import Markdown

load_dotenv()

console = Console()

def display_response(resp):
    """Display the OpenAI response in a nice format using Rich"""
    
    # Header
    console.print(Panel.fit(
        "[bold blue]OpenAI MCP Response[/bold blue]",
        style="blue"
    ))
    
    # Response metadata
    metadata_table = Table(show_header=False, box=None, padding=(0, 1))
    metadata_table.add_row("[bold]Response ID:[/bold]", resp.id)
    metadata_table.add_row("[bold]Model:[/bold]", resp.model)
    metadata_table.add_row("[bold]Status:[/bold]", f"[green]{resp.status}[/green]")
    
    console.print(Panel(metadata_table, title="Response Info", border_style="dim"))
    
    # MCP Tools Used
    mcp_tools_used = []
    mcp_calls = []
    final_messages = []
    
    for output in resp.output:
        if hasattr(output, 'type'):
            if output.type == 'mcp_list_tools':
                for tool in output.tools:
                    mcp_tools_used.append({
                        'name': tool.name,
                        'description': tool.description.strip() if tool.description else 'No description',
                        'server_label': output.server_label
                    })
            elif output.type == 'mcp_call':
                mcp_calls.append({
                    'name': output.name,
                    'server_label': output.server_label,
                    'arguments': output.arguments,
                    'error': output.error,
                    'output': output.output,
                    'success': output.error is None
                })
            elif output.type == 'message':
                final_messages.append(output)
    
    # Display MCP Tools Available
    if mcp_tools_used:
        tools_table = Table(title="MCP Tools Available", show_header=True, header_style="bold magenta")
        tools_table.add_column("Tool Name", style="cyan")
        tools_table.add_column("Server", style="yellow")
        tools_table.add_column("Description", style="white")
        
        for tool in mcp_tools_used:
            # Truncate long descriptions
            desc = tool['description'][:100] + "..." if len(tool['description']) > 100 else tool['description']
            tools_table.add_row(tool['name'], tool['server_label'], desc)
        
        console.print(tools_table)
        console.print()
    
    # Display MCP Tool Calls
    if mcp_calls:
        calls_table = Table(title="MCP Tool Calls", show_header=True, header_style="bold cyan")
        calls_table.add_column("Tool", style="cyan")
        calls_table.add_column("Server", style="yellow")
        calls_table.add_column("Arguments", style="white")
        calls_table.add_column("Status", style="white")
        
        for call in mcp_calls:
            status = "[green]✓ Success[/green]" if call['success'] else f"[red]✗ Error: {call['error']['message'] if call['error'] else 'Unknown'}[/red]"
            args = call['arguments'][:50] + "..." if len(call['arguments']) > 50 else call['arguments']
            calls_table.add_row(call['name'], call['server_label'], args, status)
        
        console.print(calls_table)
        console.print()
        
        # Display raw tool call results
        for i, call in enumerate(mcp_calls):
            if call['output'] is not None:
                console.print(Panel(
                    str(call['output']),
                    title=f"[bold cyan]Raw Output from {call['name']} (Call {i+1})[/bold cyan]",
                    border_style="cyan"
                ))
            elif call['error']:
                console.print(Panel(
                    f"Error Details: {call['error']}",
                    title=f"[bold red]Error Details from {call['name']} (Call {i+1})[/bold red]",
                    border_style="red"
                ))
            else:
                console.print(Panel(
                    "No output or error data available",
                    title=f"[bold yellow]No Data from {call['name']} (Call {i+1})[/bold yellow]",
                    border_style="yellow"
                ))
        console.print()
    
    # Display Final Response
    if final_messages:
        for message in final_messages:
            if hasattr(message, 'content') and message.content:
                for content in message.content:
                    if hasattr(content, 'text'):
                        console.print(Panel(
                            Markdown(content.text),
                            title="[bold green]Final Response[/bold green]",
                            border_style="green"
                        ))
    
    # Display usage information
    if hasattr(resp, 'usage') and resp.usage:
        usage_table = Table(show_header=False, box=None, padding=(0, 1))
        usage_table.add_row("[bold]Input Tokens:[/bold]", str(resp.usage.input_tokens))
        usage_table.add_row("[bold]Output Tokens:[/bold]", str(resp.usage.output_tokens))
        usage_table.add_row("[bold]Total Tokens:[/bold]", str(resp.usage.total_tokens))
        
        console.print(Panel(usage_table, title="Token Usage", border_style="dim"))


def main():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    console.print("[bold yellow]Making request to OpenAI with MCP tools...[/bold yellow]")
    
    resp = client.responses.create(
        model="gpt-4.1",
        instructions="You are a helpful assistant that only answers questions from the tools provided. If the tools are not relevant to the question, you should say so. If you are asked to provide URLs, reponds with an unformatted full url.",
        tools=[
            {
                "type": "mcp",
                "server_label": "search",
                # "server_label": "gitmcp",
                "server_url": "https://d578-2a02-1812-c35-b400-3d2f-e5a3-be22-511f.ngrok-free.app/mcp",
                # "server_url": "https://gitmcp.io/gbaeke/realtime-webrtc",
                "require_approval": "never",
            
            },
        ],
        input="Who is Geert Baeke and does he have a YouTube channel?",
    )
    
    display_response(resp)


if __name__ == "__main__":
    main()