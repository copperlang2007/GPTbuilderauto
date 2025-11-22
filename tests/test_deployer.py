"""
Tests for Deployer
"""
import tempfile
import shutil
from pathlib import Path
from gptbuilderauto.deployer.deployer import Deployer


class TestDeployer:
    """Test cases for Deployer"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.deployer = Deployer(deploy_path=self.temp_dir, provider="local")
        
    def teardown_method(self):
        """Cleanup test environment"""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
            
    def test_init(self):
        """Test initialization"""
        assert self.deployer.deploy_path == Path(self.temp_dir)
        assert self.deployer.provider == "local"
        assert self.deployer.deploy_path.exists()
        
    def test_deploy_code_success(self):
        """Test successful code deployment"""
        code = "print('Hello, World!')"
        result = self.deployer.deploy_code(code, "test_app", "python")
        
        assert result['success'] is True
        assert 'test_app' in result['deployment_name']
        assert Path(result['deployment_path']).exists()
        assert Path(result['code_file']).exists()
        
    def test_deploy_code_creates_files(self):
        """Test deployment creates necessary files"""
        code = "console.log('Hello');"
        result = self.deployer.deploy_code(
            code,
            "js_app",
            "javascript",
            metadata={"author": "test"}
        )
        
        deployment_path = Path(result['deployment_path'])
        
        assert (deployment_path / "main.js").exists()
        assert (deployment_path / "README.md").exists()
        assert (deployment_path / "metadata.json").exists()
        
    def test_list_deployments(self):
        """Test listing deployments"""
        # Deploy some apps
        self.deployer.deploy_code("code1", "app1", "python")
        self.deployer.deploy_code("code2", "app2", "python")
        
        deployments = self.deployer.list_deployments()
        
        assert len(deployments) == 2
        assert any('app1' in d['name'] for d in deployments)
        assert any('app2' in d['name'] for d in deployments)
        
    def test_delete_deployment(self):
        """Test deployment deletion"""
        result = self.deployer.deploy_code("code", "delete_me", "python")
        deployment_name = result['deployment_name']
        
        # Delete deployment
        success = self.deployer.delete_deployment(deployment_name)
        assert success is True
        
        # Verify it's gone
        deployments = self.deployer.list_deployments()
        assert not any(deployment_name == d['name'] for d in deployments)
        
    def test_delete_nonexistent_deployment(self):
        """Test deleting non-existent deployment"""
        success = self.deployer.delete_deployment("nonexistent")
        assert success is False
        
    def test_get_extension(self):
        """Test file extension mapping"""
        assert self.deployer._get_extension("python") == "py"
        assert self.deployer._get_extension("javascript") == "js"
        assert self.deployer._get_extension("go") == "go"
