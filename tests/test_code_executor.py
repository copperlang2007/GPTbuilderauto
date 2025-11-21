"""
Tests for Code Executor
"""
from gptbuilderauto.executor.code_executor import CodeExecutor


class TestCodeExecutor:
    """Test cases for CodeExecutor"""
    
    def test_init(self):
        """Test initialization"""
        executor = CodeExecutor(timeout=60, use_docker=False)
        assert executor.timeout == 60
        assert executor.use_docker is False
        
    def test_execute_python_simple(self):
        """Test simple Python execution"""
        executor = CodeExecutor(use_docker=False)
        code = "print('Hello, World!')"
        
        result = executor.execute_python(code)
        
        assert result['success'] is True
        assert "Hello, World!" in result['stdout']
        assert result['return_code'] == 0
        
    def test_execute_python_with_error(self):
        """Test Python execution with error"""
        executor = CodeExecutor(use_docker=False)
        code = "raise ValueError('Test error')"
        
        result = executor.execute_python(code)
        
        assert result['success'] is False
        assert result['return_code'] != 0
        assert 'ValueError' in result['stderr'] or 'Test error' in result['stderr']
        
    def test_execute_python_timeout(self):
        """Test execution timeout"""
        executor = CodeExecutor(use_docker=False, timeout=1)
        code = "import time; time.sleep(10)"
        
        result = executor.execute_python(code)
        
        assert result['success'] is False
        assert 'timeout' in result['stderr'].lower()
        
    def test_get_extension(self):
        """Test file extension mapping"""
        executor = CodeExecutor(use_docker=False)
        
        assert executor._get_extension("python") == "py"
        assert executor._get_extension("javascript") == "js"
        assert executor._get_extension("java") == "java"
        assert executor._get_extension("unknown") == "txt"
        
    def test_get_command(self):
        """Test command generation"""
        executor = CodeExecutor(use_docker=False)
        
        cmd = executor._get_command("python", "test.py", ["arg1", "arg2"])
        assert cmd == ["python3", "test.py", "arg1", "arg2"]
        
        cmd = executor._get_command("javascript", "test.js")
        assert cmd == ["node", "test.js"]
