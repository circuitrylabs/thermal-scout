# META: Thermal Scout Development Flow

## [meta]
```json
{
  "project": "thermal-scout",
  "version": "0.1.0",
  "approach": "educational-development",
  "teaching_focus": ["frontend-basics", "api-integration", "thermal-awareness", "consent-patterns"],
  "workflow_type": "iterative-learning",
  "documentation_style": "inline-teaching"
}
```

## Development Workflow & Learning Path

**Note**: No extensive inline comments needed - focus on clean, working code.

### Phase 1: Foundation → HTML Structure
**Learning Goals:**
- HTML5 semantic structure
- Accessibility basics
- Mobile-first thinking

**Workflow:**
```
[Planning] → [HTML Scaffold] → [Semantic Review] → [Accessibility Check]
     ↓             ↓                    ↓                    ↓
  Concepts:    Structure:          Best Practices:       ARIA basics
  - DOCTYPE    - header/main       - alt texts          - roles
  - meta tags  - sections          - form labels        - landmarks
  - viewport   - footer            - semantic HTML      - focus order
```

**Agent Handoff:** planning.agent → html.agent → review.agent

### Phase 2: Styling → CSS Architecture
**Learning Goals:**
- CSS custom properties
- Monospace typography
- ASCII art borders
- Responsive design

**Workflow:**
```
[Design Tokens] → [Base Styles] → [Component Styles] → [Responsive]
       ↓               ↓                 ↓                  ↓
   Variables:      Typography:      ASCII Borders:     Breakpoints:
   - colors        - font-stack     - box-drawing      - mobile-first
   - spacing       - line-height     - characters       - fluid sizing
   - timing        - measure         - patterns         - grid/flex
```

**Teaching Moments:**
- Why custom properties over hard-coded values
- How monospace creates predictable layouts
- ASCII border techniques with CSS

### Phase 3: Interactivity → JavaScript Patterns
**Learning Goals:**
- Vanilla JS best practices
- Event delegation
- State management without frameworks
- API integration

**Workflow:**
```
[Core Functions] → [Event Handling] → [State Mgmt] → [API Integration]
        ↓                ↓                ↓               ↓
    Patterns:       Delegation:      localStorage:    HuggingFace:
    - modules       - bubbling       - consent UI     - fetch()
    - closures      - capturing      - encryption     - error handling
    - promises      - performance    - validation     - rate limiting
```

**Teaching Focus:**
1. **Module Pattern**: Organizing code without build tools
2. **Event Delegation**: Efficient event handling
3. **State Pattern**: Managing UI state in vanilla JS
4. **Fetch API**: Modern HTTP requests

### Phase 4: Thermal Awareness → Performance
**Learning Goals:**
- Performance metrics
- Thermal calculations
- Resource optimization

**Workflow:**
```
[Model Analysis] → [Thermal Calc] → [UI Indicators] → [Optimization]
        ↓               ↓                ↓                 ↓
   Parameters:      Formula:         Display:         Performance:
   - model size     - param count    - emoji scale    - lazy loading
   - quantization   - operations     - color coding   - pagination
   - context        - memory use     - animations     - caching
```

### Phase 5: Consent & Privacy → Ethical Patterns
**Learning Goals:**
- Consent UI patterns
- Local storage security
- Privacy-first design

**Workflow:**
```
[Consent UI] → [Storage Logic] → [Privacy Features] → [Documentation]
      ↓              ↓                  ↓                    ↓
   Patterns:     Security:         Features:            Docs:
   - explicit    - encryption      - data clearing      - privacy policy
   - granular    - validation      - export/import      - consent flow
   - reversible  - expiration      - audit trail        - user rights
```

## Frontend Teaching Points

### 1. HTML Structure Lesson
```html
<!-- We'll build this together, explaining each choice -->
<!DOCTYPE html> <!-- Why HTML5 -->
<html lang="en"> <!-- Accessibility from the start -->
<head>
    <meta charset="UTF-8"> <!-- Character encoding -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> <!-- Mobile-first -->
    <title>Thermal Scout | CircuitryLabs</title> <!-- SEO and clarity -->
</head>
```

### 2. CSS Architecture Lesson
```css
/* Design tokens approach */
:root {
    /* Why CSS custom properties */
    --color-primary: #00FFFF;
    --font-mono: 'Courier New', monospace;
    --spacing-unit: 0.25rem;
}

/* Utility-first without framework */
.text-mono { font-family: var(--font-mono); }
.thermal-cool { color: var(--color-primary); }
```

### 3. JavaScript Patterns Lesson
```javascript
// Module pattern for organization
const ThermalScout = (() => {
    // Private state
    let apiKey = null;
    
    // Public API
    return {
        init() {
            // Teach event delegation
            document.addEventListener('click', this.handleClick);
        },
        handleClick(e) {
            // Pattern matching without framework
            if (e.target.matches('[data-action]')) {
                const action = e.target.dataset.action;
                this[action]?.(e);
            }
        }
    };
})();
```

### 4. API Integration Lesson
```javascript
// Modern fetch with error handling
async function searchModels(query) {
    try {
        const response = await fetch(`${API_BASE}/models`, {
            headers: {
                'Authorization': `Bearer ${getApiKey()}`
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        // User-friendly error handling
        console.error('Search failed:', error);
        showUserMessage('Search temporarily unavailable');
    }
}
```

## Development Commands & Flow

### Iteration Pattern
```bash
# Each development cycle
1. Plan feature with teaching focus
2. Implement with inline education
3. Review and refactor together
4. Document learnings

# Example cycle:
/plan "Add API key consent UI"
/implement "Create consent modal with teaching comments"
/review "Check accessibility and patterns"
/document "Note new patterns learned"
```

### Teaching Checkpoints
- [ ] HTML semantics understood
- [ ] CSS custom properties mastered
- [ ] JavaScript modules comfortable
- [ ] API integration patterns clear
- [ ] Performance awareness developed
- [ ] Consent patterns implemented

## Agent Communication Flow

```
[meta.agent] → [planning.agent] → [teaching.agent] → [implement.agent]
      ↓               ↓                  ↓                  ↓
   Workflow      Requirements      Concepts          Code+Learning
      ↓               ↓                  ↓                  ↓
[review.agent] ← [test.agent] ← [refactor.agent] ← [document.agent]
```

## Next Steps

1. **Create CLAUDE.md** using doc.agent with this meta flow
2. **Start Phase 1** with HTML structure and teaching
3. **Iterate** through phases with learning focus
4. **Document** patterns for future projects

Ready to begin the educational development journey!