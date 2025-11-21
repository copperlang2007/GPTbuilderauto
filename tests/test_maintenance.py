"""
Tests for Maintenance Monitor
"""
import tempfile
import shutil
from pathlib import Path
from gptbuilderauto.monitor.maintenance import MaintenanceMonitor


class TestMaintenanceMonitor:
    """Test cases for MaintenanceMonitor"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.monitor = MaintenanceMonitor(check_interval=60)
        
    def teardown_method(self):
        """Cleanup test environment"""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
            
    def test_init(self):
        """Test initialization"""
        assert self.monitor.check_interval == 60
        assert isinstance(self.monitor.health_history, dict)
        
    def test_health_check_missing_deployment(self):
        """Test health check on missing deployment"""
        result = self.monitor.health_check("/nonexistent/path")
        
        assert result['status'] == 'error'
        assert 'not found' in result['message'].lower()
        
    def test_health_check_no_main_file(self):
        """Test health check with no main file"""
        deployment_path = Path(self.temp_dir) / "test_deploy"
        deployment_path.mkdir()
        
        result = self.monitor.health_check(str(deployment_path))
        
        assert result['status'] == 'error'
        assert 'main file' in result['message'].lower()
        
    def test_health_check_success(self):
        """Test successful health check"""
        deployment_path = Path(self.temp_dir) / "test_deploy"
        deployment_path.mkdir()
        
        # Create main file
        main_file = deployment_path / "main.py"
        main_file.write_text("print('Hello')")
        
        result = self.monitor.health_check(str(deployment_path))
        
        assert result['status'] in ['healthy', 'warning']
        assert 'main_file' in result
        assert result['file_size'] > 0
        
    def test_health_check_invalid_syntax(self):
        """Test health check with invalid Python syntax"""
        deployment_path = Path(self.temp_dir) / "test_deploy"
        deployment_path.mkdir()
        
        # Create invalid Python file
        main_file = deployment_path / "main.py"
        main_file.write_text("def invalid syntax here")
        
        result = self.monitor.health_check(str(deployment_path))
        
        assert result['syntax_valid'] is False
        
    def test_analyze_logs_missing_file(self):
        """Test log analysis with missing file"""
        result = self.monitor.analyze_logs("/nonexistent/log.txt")
        
        assert result['status'] == 'error'
        
    def test_analyze_logs_success(self):
        """Test successful log analysis"""
        log_file = Path(self.temp_dir) / "test.log"
        log_content = """
INFO: Application started
WARNING: Config file not found
ERROR: Database connection failed
INFO: Retrying connection
ERROR: Connection timeout
"""
        log_file.write_text(log_content)
        
        result = self.monitor.analyze_logs(str(log_file))
        
        assert result['status'] == 'success'
        assert result['errors'] == 2
        assert result['warnings'] == 1
        assert len(result['recent_errors']) == 2
        
    def test_get_health_history(self):
        """Test getting health history"""
        deployment_path = Path(self.temp_dir) / "test_deploy"
        deployment_path.mkdir()
        (deployment_path / "main.py").write_text("print('test')")
        
        # Perform multiple health checks
        self.monitor.health_check(str(deployment_path))
        self.monitor.health_check(str(deployment_path))
        
        history = self.monitor.get_health_history("test_deploy", hours=24)
        
        assert len(history) == 2
        
    def test_generate_report(self):
        """Test report generation"""
        deployment_path = Path(self.temp_dir) / "test_deploy"
        deployment_path.mkdir()
        (deployment_path / "main.py").write_text("print('test')")
        
        self.monitor.health_check(str(deployment_path))
        
        report = self.monitor.generate_report("test_deploy")
        
        assert "Maintenance Report" in report
        assert "test_deploy" in report
        assert "Total checks:" in report
