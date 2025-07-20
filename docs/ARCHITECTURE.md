# Thermal Scout Architecture

## Overview

Thermal Scout provides three interfaces for finding AI models with thermal awareness:

```
┌─────────────────────────────────────────────────┐
│              Thermal Scout                       │
├─────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │   Web   │  │   CLI   │  │   API   │        │
│  │   UI    │  │ (Typer) │  │(FastAPI)│        │
│  └────┬────┘  └────┬────┘  └────┬────┘        │
│       │            │             │              │
│       └────────────┴─────────────┘              │
│                    │                            │
│         ┌──────────▼──────────┐                │
│         │   Core Search Logic │                │
│         │   (search.py)       │                │
│         └──────────┬──────────┘                │
│                    │                            │
│         ┌──────────▼──────────┐                │
│         │  HuggingFace Hub    │                │
│         │      API            │                │
│         └─────────────────────┘                │
└─────────────────────────────────────────────────┘
```

## Components

### Web UI
- **Technology**: Vanilla HTML/CSS/JavaScript
- **Files**: `index.html`, `app.js`, `styles.css`
- **Features**: Real-time search, thermal indicators, light mode

### CLI
- **Technology**: Python with Typer
- **File**: `thermal_scout/cli.py`
- **Features**: Table/JSON output, thermal filtering

### API
- **Technology**: Python with FastAPI
- **File**: `thermal_scout/api/main.py`
- **Features**: REST endpoints, OpenAPI docs, async support

### Core Search
- **File**: `thermal_scout/search.py`
- **Features**: HuggingFace integration, thermal calculation

## Thermal Algorithm

Models are categorized by parameter count:

```python
def get_thermal_indicator(parameters: int) -> str:
    if parameters < 1e9:  # <1B
        return "Cool"
    elif parameters < 3e9:  # 1-3B
        return "Warm"
    elif parameters < 7e9:  # 3-7B
        return "Moderate"
    else:  # 7B+
        return "Hot"
```

## Data Flow

1. **User Input** → Search query enters via Web/CLI/API
2. **Core Logic** → `search_models()` queries HuggingFace
3. **Thermal Calc** → Parameter count determines thermal level
4. **Response** → Formatted results return to user

## Key Design Decisions

- **No API Keys**: Direct HuggingFace Hub access
- **Minimal Dependencies**: Keep it lightweight
- **Type Safety**: Full type hints in Python
- **Simple Algorithm**: Parameter count as thermal proxy
- **Three Interfaces**: Cover all use cases

## Testing

- Unit tests for core logic
- Integration tests for API
- Manual testing for Web UI
- >95% coverage target