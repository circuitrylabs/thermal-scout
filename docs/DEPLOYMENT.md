# 🚀 Deploying Thermal Scout to Netlify

## Quick Deploy (Frontend Only)

Since Thermal Scout's web interface calls the HuggingFace API directly, you can deploy just the frontend to Netlify in seconds!

### Method 1: Drag & Drop

1. Visit [Netlify Drop](https://app.netlify.com/drop)
2. Drag these files into the browser:
   - `index.html`
   - `app.js`
   - `styles.css`
3. Done! Your site is live 🎉

### Method 2: Git Integration

1. Push your code to GitHub
2. In Netlify:
   - Click "New site from Git"
   - Connect your GitHub repo
   - Leave build settings empty (it's a static site)
   - Deploy!

### Method 3: Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod

# Follow prompts to authenticate and deploy
```

## Configuration

The `netlify.toml` file includes:
- Security headers
- Cache control for assets
- No build step needed

## Custom Domain

1. In Netlify dashboard → Domain settings
2. Add your custom domain
3. Netlify handles SSL automatically

## Environment Variables

Not needed! The app uses HuggingFace's public API directly.

## What About the CLI and API?

The CLI and API components need a Python backend. Options:

### Option 1: Frontend Only (Recommended)
Deploy just the web interface - it's fully functional!

### Option 2: Separate API Deployment
Deploy the Python API to:
- **Render**: Free tier, easy Python deployment
- **Railway**: Simple, scales well
- **Fly.io**: Great for global distribution
- **Vercel**: Supports Python via serverless functions

Then update `netlify.toml` to redirect API calls:

```toml
[[redirects]]
  from = "/api/*"
  to = "https://your-api.herokuapp.com/api/:splat"
  status = 200
  force = true
```

### Option 3: Netlify Functions (Serverless)
Convert the API endpoints to Netlify Functions (JavaScript):

1. Create `netlify/functions/search.js`
2. Port the Python search logic to JavaScript
3. API calls become `/.netlify/functions/search`

## Post-Deployment

After deploying, you'll get a URL like:
- `https://amazing-name-123.netlify.app`

Or with custom domain:
- `https://thermal-scout.circuitrylabs.com`

## Testing

Visit your deployed site and try searching for "bert" or "llama" - it should work immediately since it uses HuggingFace's public API!

## Monitoring

Netlify provides:
- Deploy previews for PRs
- Analytics (with paid plan)
- Form handling (if needed)
- Split testing

That's it! Your Thermal Scout is live! 🔥