"""
Example: Fully autonomous code creation workflow
"""
import os
from gptbuilderauto import CodeGenerator, CodeExecutor, Deployer, MaintenanceMonitor


def autonomous_workflow(requirement: str, app_name: str):
    """
    Fully autonomous workflow: generate -> execute -> deploy -> monitor
    
    Args:
        requirement: What code to generate
        app_name: Name for the deployed application
    """
    print("=== GPTbuilderauto Autonomous Workflow ===\n")
    
    # Initialize components
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set")
        return
    
    generator = CodeGenerator(api_key=api_key)
    executor = CodeExecutor(use_docker=True, enable_sandboxing=True)
    deployer = Deployer(deploy_path="/tmp/autonomous_deployments")
    monitor = MaintenanceMonitor()
    
    try:
        # Step 1: Generate
        print(f"[1/4] Generating code for: {requirement}")
        gen_result = generator.generate_code(requirement, language="python")
        code = gen_result['code']
        print(f"✓ Code generated ({gen_result['tokens_used']} tokens)\n")
        
        # Step 2: Execute & Validate
        print("[2/4] Executing code to validate...")
        exec_result = executor.execute_python(code)
        
        if not exec_result['success']:
            print("✗ Initial execution failed, refining...")
            
            # Refine based on error
            feedback = f"The code failed with error: {exec_result['stderr']}"
            code = generator.refine_code(code, feedback)
            
            # Retry execution
            exec_result = executor.execute_python(code)
            
        if exec_result['success']:
            print("✓ Code executed successfully")
            if exec_result['stdout']:
                print(f"  Output: {exec_result['stdout'][:100]}")
        else:
            print(f"✗ Execution failed: {exec_result['stderr'][:100]}")
            print("  Continuing with deployment anyway...\n")
        
        # Step 3: Deploy
        print(f"[3/4] Deploying as '{app_name}'...")
        deploy_result = deployer.deploy_code(
            code=code,
            name=app_name,
            language="python",
            metadata={
                "requirement": requirement,
                "tokens_used": gen_result['tokens_used'],
                "execution_tested": exec_result['success'],
                "autonomous": True
            }
        )
        
        if deploy_result['success']:
            print(f"✓ Deployed to: {deploy_result['deployment_path']}\n")
            deployment_path = deploy_result['deployment_path']
        else:
            print(f"✗ Deployment failed: {deploy_result.get('error')}")
            return
        
        # Step 4: Monitor
        print("[4/4] Running health check...")
        health = monitor.health_check(deployment_path)
        print(f"✓ Status: {health['status']}")
        
        # Generate report
        print("\n=== Deployment Report ===")
        print(f"Application: {app_name}")
        print(f"Location: {deployment_path}")
        print(f"Health: {health['status']}")
        print(f"Code size: {health.get('file_size', 'N/A')} bytes")
        
        print("\n=== Autonomous Workflow Complete ===")
        
    except Exception as e:
        print(f"\n✗ Workflow failed: {str(e)}")


if __name__ == "__main__":
    # Example 1: Simple function
    autonomous_workflow(
        requirement="Create a function to check if a number is prime",
        app_name="prime_checker"
    )
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: More complex application
    autonomous_workflow(
        requirement="Create a simple calculator with add, subtract, multiply, divide functions",
        app_name="calculator"
    )
