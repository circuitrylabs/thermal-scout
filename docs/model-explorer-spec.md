# CircuitryLabs Model Explorer - Build Spec

## Core Concept
A minimal web app to find AI models through the lens of thermal cost and consent. Our first public tool that establishes CircuitryLabs visual language.

## Signature Style Guide

### Visual Identity
- **Font**: Monospace everywhere (IBM Plex Mono or system mono)
- **Colors**: 
  - Black (#000) and white (#fff) base
  - Electric cyan (#00ffff) for energy/thermal
  - Warm red (#ff6b6b) for warnings
  - Success green (#51cf66) for open licenses
- **Layout**: Minimal boxes, ASCII-inspired borders
- **Animations**: Subtle pulse on thermal indicators, gentle fades

### Core UI Pattern
```
┌─────────────────────────────────────┐
│ ⚡ CircuitryLabs Model Explorer     │
│ "Choose wisely, compute kindly"     │
└─────────────────────────────────────┘
```

## Technical Requirements

### Must Have
1. **HuggingFace Search**
   - User provides their own API key
   - Search text generation models
   - Store key in localStorage with consent

2. **Display Format**
   ```
   Model Name          Size    Thermal   License
   meta-llama/Llama-2  7B     🔥🔥      ✓ Open
   google/flan-t5-xl   3B     🔥        ✓ Open  
   gpt2               124M    ·         ✓ Open
   ```

3. **Filters** (checkboxes)
   - Under 7B params (low thermal)
   - Open license only
   - Text models only

4. **Thermal Indicators**
   - · = <1B (cool)
   - 🔥 = 1-3B (warm)
   - 🔥🔥 = 3-7B (moderate)
   - 🔥🔥🔥 = 7B+ (hot)

### Interaction Flow
1. First visit: "May I store your API key locally? [Yes] [No]"
2. Before search: "This search costs ~0.001 thermal units"
3. Results show immediately, no pagination for MVP
4. Click model name → HuggingFace page

### Unique CircuitryLabs Elements
- **Consent moments**: Ask before storing data
- **Thermal cost preview**: Show cost before actions
- **ASCII aesthetics**: Box drawing characters, simple icons
- **Status messages**: "Searching with respect..." "Found 12 models"
- **Footer tagline**: "The heat became light ✨"

## Implementation Notes

### Stack
- Vanilla HTML/CSS/JS (no framework for v1)
- HuggingFace API: `https://huggingface.co/api/models`
- Static hosting ready (GitHub Pages)

### API Integration
```javascript
// Basic search request
fetch('https://huggingface.co/api/models?search=llama&filter=text-generation', {
  headers: {
    'Authorization': `Bearer ${apiKey}`
  }
})
```

### Thermal Calculation
```javascript
function getThermalIndicator(parameters) {
  if (!parameters) return '?';
  const billions = parameters / 1_000_000_000;
  if (billions < 1) return '·';
  if (billions < 3) return '🔥';
  if (billions < 7) return '🔥🔥';
  return '🔥🔥🔥';
}
```

### Style Essentials
```css
body {
  font-family: 'IBM Plex Mono', 'Courier New', monospace;
  background: white;
  color: black;
  line-height: 1.6;
  padding: 2rem;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.header-box {
  border: 2px solid black;
  padding: 1rem;
  margin-bottom: 2rem;
  text-align: center;
}

.thermal {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
```

## Launch Checklist
- [ ] Basic search working
- [ ] API key storage with consent
- [ ] Thermal indicators displaying correctly
- [ ] Open license filter working
- [ ] Clean monospace aesthetic
- [ ] "Choose wisely, compute kindly" tagline
- [ ] Footer with "The heat became light ✨"
- [ ] Deploy to circuitrylabs.org/tools/models

## Future Additions (Not v1)
- Thermal cost calculator
- CIRIS compatibility scores
- Export model configs
- Community ratings
- More model types

---

Remember: This is our style announcement to the world. Every detail should whisper "consent and thermal awareness."