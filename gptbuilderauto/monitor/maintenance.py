"""
Maintenance Monitor Module - Monitors and maintains deployed code
"""

import logging
from typing import Dict, List
from datetime import datetime, timedelta
from pathlib import Path
import subprocess


class MaintenanceMonitor:
    """
    Monitors and maintains deployed code
    """

    def __init__(self, check_interval: int = 300):
        """
        Initialize the maintenance monitor

        Args:
            check_interval: Interval in seconds between health checks
        """
        self.check_interval = check_interval
        self.logger = logging.getLogger(__name__)
        self.health_history: Dict[str, List[Dict]] = {}

    def health_check(self, deployment_path: str) -> Dict[str, any]:
        """
        Perform health check on a deployment

        Args:
            deployment_path: Path to deployment

        Returns:
            Health check results
        """
        deployment_path = Path(deployment_path)

        if not deployment_path.exists():
            return {
                "status": "error",
                "message": "Deployment not found",
                "timestamp": datetime.now().isoformat(),
            }

        try:
            # Check if main file exists
            main_files = list(deployment_path.glob("main.*"))
            if not main_files:
                return {
                    "status": "error",
                    "message": "Main file not found",
                    "timestamp": datetime.now().isoformat(),
                }

            # Check file integrity
            main_file = main_files[0]
            file_size = main_file.stat().st_size

            # Basic syntax check for Python
            if main_file.suffix == ".py":
                syntax_ok = self._check_python_syntax(main_file)
            else:
                syntax_ok = True

            health_status = {
                "status": "healthy" if syntax_ok else "warning",
                "deployment_path": str(deployment_path),
                "main_file": str(main_file),
                "file_size": file_size,
                "syntax_valid": syntax_ok,
                "timestamp": datetime.now().isoformat(),
            }

            # Store in history
            deployment_name = deployment_path.name
            if deployment_name not in self.health_history:
                self.health_history[deployment_name] = []
            self.health_history[deployment_name].append(health_status)

            return health_status
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            return {"status": "error", "message": str(e), "timestamp": datetime.now().isoformat()}

    def _check_python_syntax(self, file_path: Path) -> bool:
        """
        Check Python syntax

        Args:
            file_path: Path to Python file

        Returns:
            True if syntax is valid
        """
        try:
            result = subprocess.run(
                ["python3", "-m", "py_compile", str(file_path)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Syntax check failed: {str(e)}")
            return False

    def analyze_logs(self, log_file: str) -> Dict[str, any]:
        """
        Analyze logs for errors and issues

        Args:
            log_file: Path to log file

        Returns:
            Log analysis results
        """
        log_path = Path(log_file)

        if not log_path.exists():
            return {"status": "error", "message": "Log file not found"}

        try:
            content = log_path.read_text()
            lines = content.split("\n")

            errors = [line for line in lines if "ERROR" in line.upper()]
            warnings = [line for line in lines if "WARNING" in line.upper()]

            return {
                "status": "success",
                "total_lines": len(lines),
                "errors": len(errors),
                "warnings": len(warnings),
                "recent_errors": errors[-10:] if errors else [],
                "recent_warnings": warnings[-10:] if warnings else [],
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Log analysis failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    def get_health_history(self, deployment_name: str, hours: int = 24) -> List[Dict]:
        """
        Get health check history for a deployment

        Args:
            deployment_name: Name of deployment
            hours: Number of hours of history to retrieve

        Returns:
            List of health check results
        """
        if deployment_name not in self.health_history:
            return []

        cutoff_time = datetime.now() - timedelta(hours=hours)

        history = []
        for record in self.health_history[deployment_name]:
            record_time = datetime.fromisoformat(record["timestamp"])
            if record_time >= cutoff_time:
                history.append(record)

        return history

    def auto_fix(self, deployment_path: str, issue: str) -> Dict[str, any]:
        """
        Attempt to automatically fix common issues

        Args:
            deployment_path: Path to deployment
            issue: Description of the issue

        Returns:
            Fix attempt results
        """
        # This is a placeholder for auto-fix functionality
        # In a real implementation, this would use GPT to analyze and fix issues

        self.logger.info(f"Auto-fix attempted for {deployment_path}: {issue}")

        return {
            "status": "not_implemented",
            "message": "Auto-fix functionality requires GPT integration",
            "deployment_path": deployment_path,
            "issue": issue,
            "timestamp": datetime.now().isoformat(),
        }

    def generate_report(self, deployment_name: str) -> str:
        """
        Generate maintenance report for a deployment

        Args:
            deployment_name: Name of deployment

        Returns:
            Formatted report
        """
        history = self.get_health_history(deployment_name, hours=24)

        if not history:
            return f"No health history available for {deployment_name}"

        report = f"""# Maintenance Report: {deployment_name}

## Summary
- Total checks: {len(history)}
- Period: Last 24 hours
- Generated: {datetime.now().isoformat()}

## Health Status
"""

        healthy_count = sum(1 for h in history if h.get("status") == "healthy")
        warning_count = sum(1 for h in history if h.get("status") == "warning")
        error_count = sum(1 for h in history if h.get("status") == "error")

        report += f"""
- Healthy: {healthy_count} ({healthy_count/len(history)*100:.1f}%)
- Warnings: {warning_count} ({warning_count/len(history)*100:.1f}%)
- Errors: {error_count} ({error_count/len(history)*100:.1f}%)

## Recent Issues
"""

        recent_issues = [h for h in history if h.get("status") != "healthy"][-5:]
        if recent_issues:
            for issue in recent_issues:
                timestamp = issue.get("timestamp")
                status = issue.get("status")
                message = issue.get("message", "No details")
                report += f"\n- [{timestamp}] {status}: {message}"
        else:
            report += "\nNo recent issues detected."

        return report
