# Contributing to TyranoStudio MCP Server

Thank you for your interest in contributing! 🎉

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/ShunsukeHayashi/tyrano-studio-mcp.git
cd tyrano-studio-mcp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server locally:
```bash
python3 server.py
```

## Project Structure

```
tyrano-studio-mcp/
├── server.py           # Main MCP server implementation
├── README.md           # User documentation
├── TODO.md             # Development roadmap
├── CONTRIBUTING.md     # This file
├── requirements.txt    # Python dependencies
├── mcp_config.json     # Example MCP configuration
└── LICENSE             # MIT License
```

## Development Workflow

1. **Create a new branch**:
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**:
   - Follow PEP 8 style guide
   - Add docstrings to functions
   - Update documentation if needed

3. **Test your changes**:
   - Manually test with Claude Code
   - Verify all existing features still work

4. **Commit your changes**:
```bash
git add .
git commit -m "feat: add your feature description"
```

5. **Push and create a Pull Request**:
```bash
git push origin feature/your-feature-name
```

## Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add audio file management tool
fix: correct scenario validation for nested tags
docs: update installation instructions
refactor: simplify project creation logic
```

## Code Style

- Use Python 3.11+
- Follow PEP 8
- Use type hints where possible
- Keep functions focused and small
- Add docstrings to all public functions

Example:
```python
async def example_handler(arguments: dict) -> list[types.TextContent]:
    """
    Brief description of what this handler does.

    Args:
        arguments: Dictionary containing tool arguments

    Returns:
        List of TextContent responses
    """
    # Implementation
    pass
```

## Adding New Tools

1. Add tool definition in `list_tools()`:
```python
types.Tool(
    name="your_tool_name",
    description="Clear description of what it does",
    inputSchema={
        "type": "object",
        "properties": {
            "param_name": {
                "type": "string",
                "description": "Parameter description",
            },
        },
        "required": ["param_name"],
    },
)
```

2. Add handler in `call_tool()`:
```python
elif name == "your_tool_name":
    return await your_tool_handler(arguments)
```

3. Implement the handler function:
```python
async def your_tool_handler(arguments: dict) -> list[types.TextContent]:
    """Implementation"""
    pass
```

4. Update README.md with usage examples

## Testing Checklist

Before submitting a PR, verify:

- [ ] All existing tools still work
- [ ] New tool works as expected
- [ ] Error cases are handled gracefully
- [ ] Documentation is updated
- [ ] Code follows style guidelines
- [ ] No sensitive information is committed

## What to Contribute

### High Priority
- Advanced scenario validation features
- Audio/video resource management
- Better error messages
- Cross-platform path handling

### Welcome Contributions
- Bug fixes
- Documentation improvements
- Example projects
- Test cases
- Performance optimizations

### Needs Discussion First
- Breaking API changes
- Major architectural changes
- New dependencies
- Export/build features

## Questions?

- Open an issue for bug reports
- Open a discussion for feature ideas
- Check TODO.md for planned features

## License

By contributing, you agree that your contributions will be licensed under the MIT License.