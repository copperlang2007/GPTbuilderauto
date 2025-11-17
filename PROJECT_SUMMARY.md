# GPTbuilderauto - Project Summary

## Overview
GPTbuilderauto is a comprehensive system that leverages ChatGPT (GPT-4) to autonomously generate, execute, deploy, and maintain code with minimal human intervention.

## Repository Structure
```
GPTbuilderauto/
├── gptbuilderauto/           # Main package
│   ├── core/                 # Code generation
│   │   └── code_generator.py # GPT-4 based code generation
│   ├── executor/             # Code execution
│   │   └── code_executor.py  # Sandboxed execution with Docker support
│   ├── deployer/             # Deployment automation
│   │   └── deployer.py       # Local and git-based deployment
│   ├── monitor/              # Monitoring and maintenance
│   │   └── maintenance.py    # Health checks and monitoring
│   ├── utils/                # Utilities
│   │   ├── config.py         # Configuration management
│   │   └── logging.py        # Logging utilities
│   └── cli.py                # Command-line interface
├── tests/                    # Test suite
│   ├── test_code_generator.py
│   ├── test_code_executor.py
│   ├── test_deployer.py
│   └── test_maintenance.py
├── examples/                 # Usage examples
│   ├── basic_usage.py
│   └── autonomous_workflow.py
├── docs/                     # Documentation
│   ├── README.md
│   ├── CONTRIBUTING.md
│   └── CHANGELOG.md
├── requirements.txt          # Dependencies
├── setup.py                  # Package setup
├── pytest.ini               # Test configuration
├── .env.example             # Environment configuration template
└── .gitignore               # Git ignore rules
```

## Core Components

### 1. Code Generator (`gptbuilderauto/core/code_generator.py`)
- **Purpose**: Generate code using OpenAI GPT-4
- **Key Features**:
  - Generate code from natural language requirements
  - Refine existing code based on feedback
  - Automatically generate unit tests
  - Support for multiple programming languages
- **Dependencies**: openai>=1.0.0

### 2. Code Executor (`gptbuilderauto/executor/code_executor.py`)
- **Purpose**: Safely execute generated code
- **Key Features**:
  - Sandboxed execution environment
  - Docker container isolation (optional)
  - Timeout protection
  - Resource limits (memory, CPU)
  - Network isolation for enhanced security
- **Dependencies**: docker>=6.0.0

### 3. Deployer (`gptbuilderauto/deployer/deployer.py`)
- **Purpose**: Automated code deployment
- **Key Features**:
  - Local filesystem deployment
  - Git repository deployment
  - Version tracking
  - Metadata management
  - Deployment listing and deletion
- **Dependencies**: GitPython>=3.1.0

### 4. Maintenance Monitor (`gptbuilderauto/monitor/maintenance.py`)
- **Purpose**: Monitor and maintain deployed code
- **Key Features**:
  - Health checks (file integrity, syntax validation)
  - Log analysis (error and warning detection)
  - Health history tracking
  - Automated reporting
  - Auto-fix placeholder (extensible)

### 5. CLI Interface (`gptbuilderauto/cli.py`)
- **Purpose**: Command-line interface for all operations
- **Commands**:
  - `generate` - Generate code from requirements
  - `execute` - Execute code safely
  - `deploy` - Deploy code to target environment
  - `monitor` - Health check deployed code
  - `auto` - Fully autonomous workflow (generate → execute → deploy → monitor)
  - `list-deployments` - List all deployments
- **Dependencies**: click>=8.0.0

## Installation

```bash
# Clone the repository
git clone https://github.com/copperlang2007/GPTbuilderauto.git
cd GPTbuilderauto

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Usage Examples

### Basic Code Generation
```bash
gptbuilder generate "create a function to calculate prime numbers" --output primes.py
```

### Safe Code Execution
```bash
gptbuilder execute primes.py --docker
```

### Code Deployment
```bash
gptbuilder deploy primes.py prime_checker
```

### Health Monitoring
```bash
gptbuilder monitor /tmp/gptbuilder_deployments/prime_checker_*/
```

### Fully Autonomous Mode
```bash
gptbuilder auto "create a REST API for user management" --name user-api
```
This command will:
1. Generate the code using GPT-4
2. Execute it to verify it works
3. Deploy it to the configured environment
4. Run a health check

## Programmatic Usage

```python
from gptbuilderauto import CodeGenerator, CodeExecutor, Deployer

# Generate code
generator = CodeGenerator(api_key="your-api-key")
result = generator.generate_code("create a factorial function", language="python")

# Execute code
executor = CodeExecutor(use_docker=True)
exec_result = executor.execute_python(result['code'])

# Deploy code
deployer = Deployer(deploy_path="/tmp/deployments")
deploy_result = deployer.deploy_code(result['code'], "factorial_app", "python")
```

## Testing

### Test Suite
- **Total Tests**: 28
- **Coverage**: 42% (core logic tested)
- **Test Categories**:
  - Code generation (6 tests)
  - Code execution (6 tests)
  - Deployment (7 tests)
  - Monitoring (9 tests)

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gptbuilderauto --cov-report=html

# Run specific test file
pytest tests/test_code_generator.py
```

## Security Features

1. **Sandboxed Execution**
   - Code runs in isolated environments
   - Docker container support for maximum isolation
   - Network restrictions (optional)

2. **Resource Limits**
   - Execution timeout protection
   - Memory limits (512MB for Docker)
   - CPU restrictions

3. **Input Validation**
   - API key validation
   - File path sanitization
   - Environment variable filtering

4. **Code Quality**
   - All code passes flake8 linting
   - Black formatting applied
   - No security vulnerabilities (CodeQL verified)

## Configuration

Configuration is managed through environment variables (`.env` file):

```bash
# OpenAI API
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4

# Execution
EXECUTION_TIMEOUT=300
ENABLE_DOCKER=true
ENABLE_SANDBOXING=true

# Deployment
DEPLOY_PROVIDER=local
DEPLOY_PATH=/tmp/gptbuilder_deployments

# Logging
LOG_LEVEL=INFO
LOG_FILE=gptbuilder.log
```

## Dependencies

### Core Dependencies
- `openai>=1.0.0` - GPT-4 API access
- `click>=8.0.0` - CLI framework
- `python-dotenv>=1.0.0` - Environment configuration
- `docker>=6.0.0` - Container management
- `GitPython>=3.1.0` - Git operations
- `pyyaml>=6.0` - YAML parsing

### Development Dependencies
- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting
- `black>=23.0.0` - Code formatting
- `flake8>=6.0.0` - Linting

## Future Enhancements

1. **Language Support**
   - Add support for more programming languages (Go, Rust, Java, etc.)
   - Language-specific execution environments

2. **Deployment Providers**
   - AWS Lambda deployment
   - Google Cloud Functions
   - Azure Functions
   - Kubernetes deployment

3. **Monitoring**
   - Real-time monitoring dashboards
   - Alerting and notifications
   - Performance metrics
   - Auto-fix implementation using GPT-4

4. **Code Quality**
   - Automatic code review using GPT-4
   - Security vulnerability scanning
   - Performance optimization suggestions

5. **Collaboration**
   - Multi-user support
   - Project templates
   - Shared deployments
   - Version control integration

## License
MIT License - See LICENSE file for details

## Contributing
See CONTRIBUTING.md for guidelines on how to contribute to this project.

## Support
For issues, questions, or contributions, please open an issue on GitHub.

---

**GPTbuilderauto** - Bringing autonomous code creation to life! 🚀
