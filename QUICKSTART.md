# 🚀 RepoAsk - Quick Start Guide

## Prerequisites Check

Before starting, make sure you have:
- ✅ Python 3.11+ installed
- ✅ Git installed and in PATH
- ✅ Groq API key (get one at https://console.groq.com/)

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Open `.env` file and add your Groq API key:
```
GROQ_API_KEY=your_actual_api_key_here
```

### 3. Start Server
```bash
python main.py
```

### 4. Open Browser
Navigate to: **http://localhost:8000**

## Using RepoAsk

### Method 1: Repository URL (Recommended)

1. **Copy repository URL** from GitHub/GitLab
   - Example: `https://github.com/flaskr/flask`

2. **Paste URL** in the left panel input field

3. **Click "Clone Repository"**
   - Wait 5-30 seconds for cloning and indexing

4. **Start asking questions!**
   - "Audit this code for security issues"
   - "Explain the architecture"
   - "Generate documentation"
   - "How does authentication work?"

### Method 2: Local Files (Legacy)

1. Copy your code files to `codigo_a_analizar/` folder
2. Restart the server
3. Files will be automatically indexed

## Example Workflow

```
1. User pastes: https://github.com/requests/requests
2. System clones repository (shallow clone)
3. Smart filtering selects only code files
4. Vector index builds automatically
5. Status shows: "Ready (142 files indexed)"
6. User asks: "How are HTTP sessions managed?"
7. AI analyzes the code and provides detailed answer
8. User asks: "Are there any security vulnerabilities?"
9. AI performs security audit with specific findings
```

## Common Questions to Ask

### Security
- "Perform a complete security audit"
- "Find SQL injection vulnerabilities"
- "Check for XSS vulnerabilities"
- "Are there any hardcoded secrets?"

### Architecture
- "Explain the project structure"
- "How does the routing work?"
- "What design patterns are used?"
- "Explain the database schema"

### Documentation
- "Generate a README for this project"
- "Document the API endpoints"
- "Create developer onboarding guide"
- "Explain the deployment process"

### Code Quality
- "Suggest refactoring opportunities"
- "How can I improve performance?"
- "Identify code smells"
- "What tests should be added?"

## Managing Repositories

### Switch Between Repositories
- Click on repository name in left panel
- System loads and indexes automatically

### Delete Repository
- Hover over repository name
- Click the ✕ button
- Confirm deletion

### Multiple Repositories
- Clone as many as you want
- Switch between them instantly
- Each maintains its own context

## Troubleshooting

### "Cannot connect to server"
- Make sure `python main.py` is running
- Check if port 8000 is available

### "GROQ_API_KEY is not configured"
- Open `.env` file
- Add your API key
- Restart server

### "Failed to clone repository"
- Check URL format (must be HTTPS)
- Ensure Git is installed
- Verify repository is public

### "No files indexed"
- Repository may not have code files
- Check if files match supported extensions
- View `repoask.log` for details

## Keyboard Shortcuts

- **Ctrl+Enter** - Send message
- **Enter** - New line in input

## What's Filtered?

### ✅ Included (Code Files)
- Python, JavaScript, TypeScript, Java
- C, C++, Go, Rust, Ruby, PHP
- HTML, CSS, Vue, Svelte
- YAML, JSON, TOML, Markdown
- Dockerfile, Makefile, LICENSE

### ❌ Excluded
- node_modules/, vendor/, venv/
- dist/, build/, target/
- .git/, .idea/, .vscode/
- Images, videos, binaries
- Lock files, cache files

## Performance Tips

1. **Shallow clones** - Only default branch is cloned
2. **Smart filtering** - Only code files are indexed
3. **Persistent storage** - Index saved between restarts
4. **Lazy loading** - Server starts instantly

## Next Steps

1. Clone your first repository
2. Ask a question about the code
3. Try different analysis types
4. Clone another repository to compare

---

**Need help?** Check `README.md` for detailed documentation.
