# CircuitryLabs Dual-Interface Pattern

## Architecture Overview

Every CircuitryLabs application follows a dual-interface pattern, providing both web terminal and native CLI access to the same functionality.

```
┌─────────────────────────────────────────────────┐
│            CircuitryLabs App Pattern            │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────┐         ┌─────────────┐      │
│  │  Web Term   │         │  Native CLI │      │
│  │ (xterm.js)  │         │  (Python)   │      │
│  └──────┬──────┘         └──────┬──────┘      │
│         │                        │              │
│         └────────┬───────────────┘              │
│                  ▼                              │
│         ┌─────────────────┐                    │
│         │  Shared Core    │                    │
│         │  Python API     │                    │
│         └─────────────────┘                    │
│                  │                              │
│         ┌────────┴────────┐                    │
│         ▼                 ▼                    │
│    ┌─────────┐      ┌──────────┐             │
│    │ FastAPI │      │ Business │             │
│    │ Server  │      │  Logic   │             │
│    └─────────┘      └──────────┘             │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Project Structure

```
thermal-scout/
├── pyproject.toml           # Poetry/uv config
├── thermal_scout/           # Python package
│   ├── __init__.py
│   ├── cli.py              # Click CLI implementation
│   ├── api.py              # FastAPI server
│   ├── core.py             # Shared business logic
│   ├── models.py           # Pydantic models
│   └── commands/           # Command implementations
│       ├── search.py
│       ├── compare.py
│       └── export.py
├── web/                    # Web interface
│   ├── index.html
│   ├── terminal.js         # xterm.js integration
│   ├── app.js             # Web app logic
│   └── styles.css
├── scripts/
│   ├── dev.py             # Development server
│   └── build.py           # Build script
└── docs/
```

## Implementation Pattern

### 1. Shared Command Interface

```python
# thermal_scout/commands/base.py
from typing import Protocol, Dict, Any
from pydantic import BaseModel

class CommandResult(BaseModel):
    success: bool
    data: Any
    error: Optional[str] = None
    
class Command(Protocol):
    """All commands implement this interface"""
    name: str
    description: str
    
    def execute(self, **kwargs) -> CommandResult:
        ...
```

### 2. Command Implementation

```python
# thermal_scout/commands/search.py
from .base import Command, CommandResult

class SearchCommand(Command):
    name = "search"
    description = "Search for AI models"
    
    def execute(self, query: str, max_params: str = None, license: str = None) -> CommandResult:
        # Shared logic for both CLI and web
        models = search_huggingface(query, max_params, license)
        return CommandResult(success=True, data=models)
```

### 3. CLI Interface

```python
# thermal_scout/cli.py
import click
from .commands import SearchCommand, CompareCommand, ExportCommand

@click.group()
def cli():
    """Thermal Scout - AI Model Explorer"""
    pass

@cli.command()
@click.argument('query')
@click.option('--max-params', help='Maximum model parameters (e.g., 7B)')
@click.option('--license', default='open', help='License filter')
def search(query, max_params, license):
    """Search for AI models"""
    cmd = SearchCommand()
    result = cmd.execute(query=query, max_params=max_params, license=license)
    
    if result.success:
        # Format for terminal output
        for model in result.data:
            click.echo(f"{model.thermal_indicator} {model.name} ({model.size})")
    else:
        click.echo(f"Error: {result.error}", err=True)
```

### 4. Web Terminal Interface

```javascript
// web/terminal.js
class CircuitryTerminal {
    constructor() {
        this.term = new Terminal({
            theme: {
                background: '#0a0a0f',
                foreground: '#e8e8f0',
                cursor: '#00ffcc'
            },
            fontFamily: 'Courier New, monospace'
        });
        
        this.parser = new CommandParser();
        this.api = new ApiClient();
    }
    
    async handleCommand(input) {
        const { command, args } = this.parser.parse(input);
        
        // Send to backend API
        const result = await this.api.execute(command, args);
        
        // Display results in terminal
        this.displayResult(result);
    }
}
```

### 5. API Server

```python
# thermal_scout/api.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .commands import get_command

app = FastAPI()

@app.post("/api/execute")
async def execute_command(command: str, args: dict):
    """Execute any command via API"""
    cmd = get_command(command)
    if not cmd:
        return {"success": False, "error": f"Unknown command: {command}"}
    
    result = cmd.execute(**args)
    return result.dict()

# Serve web interface
app.mount("/", StaticFiles(directory="web", html=True))
```

## Development Workflow

### Local Development

```bash
# Install dependencies
uv sync

# Run development server (both CLI and web)
uv run python scripts/dev.py

# Use CLI directly
uv run thermal-scout search "llama"

# Access web terminal
open http://localhost:8000
```

### Building & Distribution

```bash
# Build Python package
uv build

# Build web assets
uv run python scripts/build.py

# Install globally
pip install thermal-scout

# Now available as:
thermal-scout search "llama"  # CLI
thermal-scout serve           # Start web server
```

## Standard Features

Every CircuitryLabs app includes:

1. **Consistent Command Syntax** - Same commands work in both interfaces
2. **Help System** - `help` command shows all available commands
3. **Tab Completion** - Both CLI and web terminal
4. **History** - Command history in both interfaces
5. **Export Formats** - JSON, CSV, YAML output options
6. **Pipe Support** - CLI commands work in Unix pipes
7. **Agent-Friendly** - Structured output for LLM consumption

## Terminal Aesthetics

```javascript
// Shared CircuitryLabs terminal config
const CIRCUITRY_THEME = {
    // ASCII banner on startup
    banner: `
╔═══════════════════════════════╗
║     CIRCUITRYLABS SYSTEMS     ║
║    heat → light → insight     ║
╚═══════════════════════════════╝
    `,
    
    // Color scheme
    colors: {
        background: '#0a0a0f',
        foreground: '#e8e8f0',
        accent: '#00ffcc',
        thermal: ['#00d4ff', '#ff6b35', '#ff3864', '#ffeb3b']
    },
    
    // Animations
    effects: {
        bootSequence: true,
        scanlines: true,
        glowCursor: true
    }
};
```

## Example Apps Following This Pattern

1. **thermal-scout** - Model explorer with thermal awareness
2. **resonance-cli** - Consciousness protocol terminal
3. **ciris-term** - CIRIS agent interface
4. **circuit-trace** - System monitoring terminal

## Benefits

1. **User Choice** - Power users get native CLI, everyone gets web
2. **Automation Ready** - Both interfaces scriptable
3. **Consistent UX** - Same commands everywhere
4. **Agent Integration** - LLMs can use either interface
5. **Deployment Flexible** - Ship as pip package, Docker, or static site
6. **Testing Simple** - Test core logic once, works everywhere

## Next Steps for Thermal Scout

1. Refactor current code into this structure
2. Add xterm.js for web terminal
3. Create Python CLI with Click
4. Implement shared command pattern
5. Add FastAPI server
6. Package for distribution

This becomes our standard for all CircuitryLabs projects!