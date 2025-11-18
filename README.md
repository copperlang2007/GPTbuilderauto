# GPTbuilderauto

**Fully Autonomous ChatGPT Code Creation, Execution, Deployment, and Maintenance**

GPTbuilderauto is a comprehensive system that leverages ChatGPT to autonomously generate, execute, deploy, and maintain code with minimal human intervention.

## 🚀 Features

- **Autonomous Code Generation**: Use GPT-4 to generate production-ready code from natural language requirements
- **Safe Code Execution**: Execute generated code in sandboxed environments with Docker support
- **Automated Deployment**: Deploy code to local or remote environments with version control
- **Continuous Monitoring**: Monitor deployed code health and automatically detect issues
- **Multi-Language Support**: Support for Python, JavaScript, and more
- **CLI Interface**: Easy-to-use command-line interface for all operations

## 📋 Requirements

- Python 3.8 or higher
- OpenAI API key
- Docker (optional, for sandboxed execution)
- Git (optional, for git-based deployments)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/copperlang2007/GPTbuilderauto.git
cd GPTbuilderauto
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# or
pip install -e .
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## 🎯 Quick Start

### Generate Code
```bash
gptbuilder generate "create a function to calculate fibonacci numbers"
```

### Execute Code
```bash
gptbuilder execute my_code.py
```

### Deploy Code
```bash
gptbuilder deploy my_code.py my_app
```

### Fully Autonomous Mode
```bash
gptbuilder auto "create a REST API for user management" --name user-api
```

This will:
1. Generate the code using GPT-4
2. Execute it to verify it works
3. Deploy it to the configured environment
4. Run a health check

## 📚 Usage

### Code Generation

Generate code from requirements:
```bash
gptbuilder generate "create a web scraper for news articles" --language python --output scraper.py
```

### Code Execution

Execute code safely:
```bash
# With Docker (recommended)
gptbuilder execute my_script.py --docker

# Without Docker (local execution)
gptbuilder execute my_script.py --no-docker
```

### Deployment

Deploy code to target environment:
```bash
gptbuilder deploy my_app.py my-application --provider local
```

List all deployments:
```bash
gptbuilder list-deployments
```

### Monitoring

Monitor a deployed application:
```bash
gptbuilder monitor /path/to/deployment
```

## 🏗️ Architecture

```
gptbuilderauto/
├── core/
│   └── code_generator.py    # GPT-based code generation
├── executor/
│   └── code_executor.py     # Sandboxed code execution
├── deployer/
│   └── deployer.py          # Automated deployment
├── monitor/
│   └── maintenance.py       # Health monitoring
├── utils/
│   ├── config.py           # Configuration management
│   └── logging.py          # Logging utilities
└── cli.py                  # Command-line interface
```

## 🔐 Security

GPTbuilderauto implements several security measures:

- **Sandboxing**: Code execution in isolated environments
- **Docker Support**: Container-based isolation
- **Network Restrictions**: Optional network isolation for executed code
- **Resource Limits**: Memory and CPU limits for executed code
- **Timeout Protection**: Automatic termination of long-running processes

## ⚙️ Configuration

Configuration is managed through environment variables (`.env` file):

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4

# Execution Settings
EXECUTION_TIMEOUT=300
ENABLE_DOCKER=true
ENABLE_SANDBOXING=true

# Deployment Settings
DEPLOY_PROVIDER=local
DEPLOY_PATH=/tmp/gptbuilder_deployments

# Logging
LOG_LEVEL=INFO
LOG_FILE=gptbuilder.log
```

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

Run tests with coverage:
```bash
pytest --cov=gptbuilderauto tests/
```

## 📖 API Usage

Use GPTbuilderauto programmatically:

```python
from gptbuilderauto import CodeGenerator, CodeExecutor, Deployer

# Generate code
generator = CodeGenerator(api_key="your-api-key")
result = generator.generate_code("create a factorial function", language="python")
code = result['code']

# Execute code
executor = CodeExecutor(use_docker=True)
exec_result = executor.execute_python(code)
print(exec_result['stdout'])

# Deploy code
deployer = Deployer(deploy_path="/tmp/deployments")
deploy_result = deployer.deploy_code(code, "factorial_app", "python")
print(f"Deployed to: {deploy_result['deployment_path']}")
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Powered by OpenAI's GPT models
- Built with Python and modern DevOps practices

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**GPTbuilderauto** - Bringing autonomous code creation to life! 🚀
