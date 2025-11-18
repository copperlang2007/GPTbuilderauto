"""
Tests for Code Generator
"""
import pytest
from unittest.mock import Mock, patch
from gptbuilderauto.core.code_generator import CodeGenerator


class TestCodeGenerator:
    """Test cases for CodeGenerator"""
    
    def test_init_with_api_key(self):
        """Test initialization with API key"""
        generator = CodeGenerator(api_key="test-key", model="gpt-4")
        assert generator.api_key == "test-key"
        assert generator.model == "gpt-4"
        
    def test_init_without_api_key(self):
        """Test initialization without API key"""
        with patch.dict('os.environ', {}, clear=True):
            generator = CodeGenerator()
            assert generator.api_key is None
            assert generator.client is None
            
    @patch('gptbuilderauto.core.code_generator.OpenAI')
    def test_generate_code_success(self, mock_openai):
        """Test successful code generation"""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="def hello(): pass"))]
        mock_response.usage = Mock(total_tokens=100)
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        generator = CodeGenerator(api_key="test-key")
        result = generator.generate_code("create a hello function", language="python")
        
        assert result['code'] == "def hello(): pass"
        assert result['language'] == "python"
        assert result['tokens_used'] == 100
        assert 'requirement' in result
        
    def test_generate_code_no_client(self):
        """Test code generation without API client"""
        generator = CodeGenerator(api_key=None)
        
        with pytest.raises(ValueError, match="OpenAI API key not configured"):
            generator.generate_code("test")
            
    @patch('gptbuilderauto.core.code_generator.OpenAI')
    def test_refine_code(self, mock_openai):
        """Test code refinement"""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="def improved(): pass"))]
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        generator = CodeGenerator(api_key="test-key")
        result = generator.refine_code("def old(): pass", "improve this")
        
        assert result == "def improved(): pass"
        
    @patch('gptbuilderauto.core.code_generator.OpenAI')
    def test_generate_tests(self, mock_openai):
        """Test test generation"""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="def test_func(): assert True"))]
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        generator = CodeGenerator(api_key="test-key")
        result = generator.generate_tests("def func(): pass")
        
        assert "test_func" in result
