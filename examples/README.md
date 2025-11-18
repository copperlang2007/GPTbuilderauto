# Examples

This directory contains example scripts demonstrating GPTbuilderauto usage.

## Available Examples

### basic_usage.py
Demonstrates the basic usage of all GPTbuilderauto components:
- Code generation
- Code execution
- Deployment
- Monitoring

Run:
```bash
python examples/basic_usage.py
```

### autonomous_workflow.py
Shows a fully autonomous workflow including:
- Automatic code generation
- Validation through execution
- Code refinement on failure
- Automated deployment
- Health monitoring

Run:
```bash
export OPENAI_API_KEY=your_key_here
python examples/autonomous_workflow.py
```

## Notes

- Make sure to set your `OPENAI_API_KEY` environment variable
- Docker is recommended for safe code execution
- Review the generated code before deploying to production
