# CLAUDE.md - Thermal Scout

This file provides guidance to Claude Code when developing the Thermal Scout project - a minimal web app for finding AI models with thermal cost awareness.

## Project Overview

**Thermal Scout** is a CircuitryLabs Model Explorer that helps users find AI models on HuggingFace while being conscious of computational thermal costs. Built with vanilla HTML/CSS/JS, it emphasizes consent, minimalism, and thermal awareness.

### Core Principles
- **Thermal Awareness**: Show computational cost through visual indicators
- **Consent-First**: Explicit user consent for all data operations
- **Minimalist Design**: ASCII-inspired, monospace aesthetic
- **No Dependencies**: Vanilla stack for v1

## Quick Start Commands

```bash
# Development setup (no build needed for v1!)
cd thermal-scout

# Start local server
python -m http.server 8000
# or
npx serve .

# Open in browser
open http://localhost:8000
```

## Architecture Overview

### Stack (v1)
- **HTML5**: Semantic, accessible markup
- **CSS3**: Custom properties, Grid/Flexbox, ASCII borders
- **Vanilla JS**: ES6+, Fetch API, localStorage
- **No Build Tools**: Direct browser execution
- **API**: HuggingFace Models API

### File Structure
```
thermal-scout/
├── index.html          # Single page app
├── styles.css          # All styling
├── app.js             # Core application logic
├── CLAUDE.md          # This file
├── docs/
│   ├── model-explorer-spec.md    # Original spec
│   └── META-DEVELOPMENT-FLOW.md  # Development guide
└── README.md          # User documentation
```

## Development Guidelines

### 1. HTML Structure
```html
<!-- Follow semantic HTML5 patterns -->
<main class="container">
    <header class="ascii-border">
        <h1 class="text-mono">Thermal Scout</h1>
    </header>
    <section class="search-panel">
        <!-- Components here -->
    </section>
</main>
```

### 2. CSS Patterns
```css
/* Use CSS custom properties for theming */
:root {
    --color-bg: #000000;
    --color-text: #FFFFFF;
    --color-accent: #00FFFF;
    --font-mono: 'Courier New', Courier, monospace;
    --border-char: '═';
}

/* ASCII border utility */
.ascii-border {
    border: 1px solid var(--color-text);
    position: relative;
}
```

### 3. JavaScript Architecture
```javascript
// Use module pattern for organization
const ThermalScout = (() => {
    // Private state
    const state = {
        apiKey: null,
        models: [],
        filters: {}
    };
    
    // Public API
    return {
        init,
        search,
        updateFilters
    };
})();

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', ThermalScout.init);
```

### 4. Thermal Indicators
```javascript
// Model size to thermal mapping
function getThermalIndicator(parameters) {
    if (parameters < 1e9) return '·';        // <1B: cool
    if (parameters < 3e9) return '🔥';      // 1-3B: warm
    if (parameters < 7e9) return '🔥🔥';    // 3-7B: moderate
    return '🔥🔥🔥';                        // 7B+: hot
}
```

### 5. API Integration
```javascript
// HuggingFace API wrapper
async function fetchModels(query, filters) {
    const endpoint = 'https://huggingface.co/api/models';
    const params = new URLSearchParams({
        search: query,
        filter: filters.license || 'apache-2.0',
        limit: 20
    });
    
    return fetch(`${endpoint}?${params}`, {
        headers: {
            'Authorization': `Bearer ${getApiKey()}`
        }
    });
}
```

### 6. Consent Patterns
```javascript
// Always ask before storing
function requestConsent(action) {
    const modal = document.createElement('div');
    modal.className = 'consent-modal ascii-border';
    modal.innerHTML = `
        <h2>Consent Required</h2>
        <p>${action}</p>
        <button data-consent="accept">Accept</button>
        <button data-consent="decline">Decline</button>
    `;
    document.body.appendChild(modal);
}
```

## Visual Design Specifications

### Color Palette
- Background: `#000000` (black)
- Text: `#FFFFFF` (white)  
- Accent: `#00FFFF` (cyan)
- Error: `#FF0000` (red)

### Typography
- Primary: `'Courier New', Courier, monospace`
- Base size: `16px`
- Line height: `1.5`

### ASCII Border Characters
```
╔══════════════╗
║ Box Drawing  ║
╚══════════════╝

┌──────────────┐
│ Light Style  │
└──────────────┘
```

## Testing & Validation

### Manual Testing Checklist
- [ ] API key consent flow works
- [ ] Search returns results
- [ ] Thermal indicators display correctly
- [ ] Filters apply properly
- [ ] Responsive on mobile
- [ ] Keyboard navigation works
- [ ] Screen reader friendly

### Performance Targets
- First paint: <1s
- Interactive: <2s
- API response: <3s
- No external fonts or heavy assets

## Common Tasks

### Add a New Feature
1. Check the spec in `docs/model-explorer-spec.md`
2. Follow existing patterns in codebase
3. Maintain vanilla JS approach
4. Test manually in browser
5. Ensure mobile responsive

### Debug API Issues
```javascript
// Enable debug logging
localStorage.setItem('debug', 'true');

// Check API key
console.log('API Key present:', !!localStorage.getItem('hf_api_key'));

// Test API directly
fetch('https://huggingface.co/api/models?limit=1')
    .then(r => r.json())
    .then(console.log);
```

### Deploy to GitHub Pages
```bash
# Ensure index.html is in root
git add .
git commit -m "Deploy Thermal Scout"
git push origin main

# Enable GitHub Pages in settings
# Visit: https://[username].github.io/thermal-scout
```

## Privacy & Security

1. **No tracking**: Zero analytics or third-party scripts
2. **Local storage only**: API keys never leave device
3. **Explicit consent**: Every data operation requires permission
4. **Clear data option**: User can wipe all stored data
5. **No cookies**: No tracking mechanisms

## Future Enhancements (v2+)

- Model comparison view
- Export search results
- Advanced filters (quantization, tasks)
- Thermal cost calculator
- Carbon footprint estimates
- PWA capabilities

## Resources

- [HuggingFace API Docs](https://huggingface.co/docs/api-inference/index)
- [MDN Web Docs](https://developer.mozilla.org/)
- [CircuitryLabs Design System](https://circuitrylabs.com/design)

Remember: Keep it minimal, respect user consent, and always show thermal costs!