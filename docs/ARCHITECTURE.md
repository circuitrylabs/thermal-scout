# Thermal Scout Architecture

## Overview

Thermal Scout is designed as a modular, extensible system for thermal-aware model discovery. The architecture prioritizes efficiency, both in terms of computational resources and code organization.

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Interface (Typer)                 │
├─────────────────────────────────────────────────────────┤
│                  Core Business Logic                     │
│  ┌──────────┐ ┌──────────┐ ┌───────────┐ ┌──────────┐ │
│  │  Search  │ │ Analyzer │ │  Compare  │ │Recommend │ │
│  └──────────┘ └──────────┘ └───────────┘ └──────────┘ │
├─────────────────────────────────────────────────────────┤
│                 Thermal Cost Engine                      │
│         ┌─────────────────────────────────┐            │
│         │   Thermal Cost Estimation       │            │
│         └─────────────────────────────────┘            │
├─────────────────────────────────────────────────────────┤
│                  External Services                       │
│  ┌────────────────┐          ┌─────────────────────┐  │
│  │ Hugging Face   │          │   Local Cache       │  │
│  │     Hub API    │          │   Management        │  │
│  └────────────────┘          └─────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. CLI Interface (`cli.py`)

The command-line interface built with Typer provides:
- Intuitive command structure
- Rich terminal output with color and tables
- Progress indicators for long operations
- Consistent error handling

**Design Decisions:**
- Typer chosen for its automatic help generation and type hints
- Rich library for beautiful terminal output
- Commands mirror the core module structure for clarity

### 2. Search Module (`search.py`)

**Purpose**: Find models on Hugging Face Hub with thermal awareness.

**Key Functions:**
- `thermal_search()`: Main search interface
- `estimate_thermal_cost()`: Thermal cost calculation

**Algorithm:**
```python
thermal_score = base_score_from_size
thermal_score = adjust_for_parameter_count(thermal_score)
thermal_score = adjust_for_efficiency_tags(thermal_score)
return map_to_category(thermal_score)
```

**Design Patterns:**
- Strategy pattern for different thermal calculations
- Decorator pattern for search result enhancement

### 3. Analyzer Module (`analyzer.py`)

**Purpose**: Deep analysis of individual models.

**Key Functions:**
- `analyze_model()`: Comprehensive model analysis
- `parse_model_size()`: Extract size from various sources
- `estimate_requirements()`: Hardware requirement calculation
- `calculate_thermal_footprint()`: Detailed thermal analysis

**Data Flow:**
```
HF API → Model Info → Size Parser → Requirement Estimator → Analysis Result
                  ↓
            Thermal Calculator
```

### 4. Compare Module (`compare.py`)

**Purpose**: Side-by-side model comparison.

**Design:**
- Leverages analyzer module for individual analysis
- Normalizes data for consistent comparison
- Adds relative metrics (inference speed indicators)

### 5. Recommend Module (`recommend.py`)

**Purpose**: Intelligent model recommendations based on tasks.

**Key Components:**
- Task mapping system
- Scoring algorithm
- Constraint filtering

**Recommendation Flow:**
```
Task Description → Task Type Inference → Model Search
                                     ↓
                              Score & Filter
                                     ↓
                            Ranked Recommendations
```

### 6. Cache Module (`cache.py`)

**Purpose**: Manage local Hugging Face model cache.

**Features:**
- Cache size reporting
- Model listing
- Safe cache clearing

## Thermal Cost Algorithm

### Scoring System

The thermal cost estimation uses a multi-factor approach:

1. **Base Score from Model Name**
   - "tiny": 1 point
   - "small": 2 points
   - "base": 3 points
   - "large": 4 points
   - "xl": 5 points
   - "xxl": 6 points

2. **Parameter Count Adjustment**
   - < 100M: -1 point
   - 100M-1B: 0 points
   - 1B-10B: +1 point
   - > 10B: +2 points

3. **Architecture Efficiency**
   - Distilled models: -1 point
   - Efficient architectures (ALBERT, etc.): -1 point

4. **Final Mapping**
   - Score ≤ 1: 🟢 Low
   - Score 2-3: 🟡 Medium
   - Score 4-5: 🔴 High
   - Score > 5: 🔥 Very High

### Power Consumption Estimates

Based on empirical observations:

| Category | Typical Power | Hardware | Use Case |
|----------|--------------|----------|----------|
| 🟢 Low | 5-10W | CPU, integrated GPU | Edge devices, continuous operation |
| 🟡 Medium | 10-50W | CPU or entry GPU | Workstations, batch processing |
| 🔴 High | 50-150W | Mid-range GPU | Dedicated ML workstations |
| 🔥 Very High | 150W+ | High-end GPU | Data centers, research |

## Data Flow

### Search Flow
```
User Query → API Search → Results Enhancement → Thermal Sorting → Display
                              ↓
                    Thermal Cost Calculation
```

### Analysis Flow
```
Model ID → HF API → Model Info → Size Detection → Requirements
                        ↓              ↓
                  Thermal Analysis   Architecture Detection
                        ↓              ↓
                    Combined Analysis Result
```

### Recommendation Flow
```
Task Description → Task Type Detection → Parallel Searches
                         ↓                      ↓
                  Constraint Filtering    Score Calculation
                         ↓                      ↓
                      Merged & Ranked Results
```

## Extension Points

### Adding New Thermal Factors

To add new factors to thermal cost calculation:

1. Modify `estimate_thermal_cost()` in `search.py`
2. Add new patterns or heuristics
3. Update scoring weights

### Adding New Commands

To add new CLI commands:

1. Add function to `cli.py` with `@app.command()` decorator
2. Implement business logic in appropriate module
3. Update documentation

### Custom Task Mappings

Extend task recognition in `recommend.py`:

```python
TASK_MAPPINGS["your_task"] = ["model-type-1", "model-type-2"]
```

## Performance Considerations

### API Rate Limiting
- Results are implicitly cached by HF Hub client
- Batch operations where possible
- Use specific queries to reduce result sets

### Memory Usage
- Stream large result sets
- Lazy loading for model information
- Efficient data structures for comparison

### Thermal Efficiency
- The tool itself is designed to be lightweight
- Minimal dependencies for core functionality
- Fast startup time with lazy imports

## Security Considerations

### API Key Management
- Uses HF Hub's built-in token management
- No credentials stored in code
- Respects environment variables

### Cache Safety
- Cache operations require confirmation
- No automatic deletions
- Size checks before operations

## Future Enhancements

### Planned Features
1. **Quantization Detection**: Identify and prefer quantized models
2. **Deployment Profiles**: Pre-configured constraints for common scenarios
3. **Batch Analysis**: Analyze multiple models in parallel
4. **Export Formats**: JSON/CSV export for analysis results
5. **Custom Scoring**: User-defined thermal cost functions

### Architecture Evolution
1. **Plugin System**: Allow custom analyzers and scorers
2. **Caching Layer**: Cache analysis results locally
3. **Async Operations**: Parallel API calls for faster results
4. **Web Interface**: Optional web UI for visual exploration

## Testing Strategy

### Unit Tests
- Thermal cost calculation accuracy
- Task mapping correctness
- Size parsing reliability

### Integration Tests
- API interaction stability
- End-to-end command flows
- Cache operations safety

### Performance Tests
- Response time for common operations
- Memory usage under load
- API call efficiency

## Contributing

### Code Style
- Type hints for all functions
- Comprehensive docstrings
- Clear variable names
- Modular design

### Adding Features
1. Discuss in issues first
2. Follow existing patterns
3. Add tests and documentation
4. Update CHANGELOG.md

### Review Process
1. Code review for logic
2. Documentation review
3. Performance impact assessment
4. Thermal efficiency verification