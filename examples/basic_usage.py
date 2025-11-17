"""
Example: Basic usage of GPTbuilderauto
"""
from gptbuilderauto import CodeGenerator, CodeExecutor, Deployer, MaintenanceMonitor


def main():
    # 1. Generate code
    print("Step 1: Generating code...")
    generator = CodeGenerator(api_key="your-api-key-here")
    
    result = generator.generate_code(
        requirement="Create a function that calculates the factorial of a number",
        language="python"
    )
    
    code = result['code']
    print(f"Generated code ({result['tokens_used']} tokens used)")
    print(code)
    
    # 2. Execute code
    print("\nStep 2: Executing code...")
    executor = CodeExecutor(use_docker=False)
    
    exec_result = executor.execute_python(code)
    
    if exec_result['success']:
        print("Execution successful!")
        print(f"Output: {exec_result['stdout']}")
    else:
        print(f"Execution failed: {exec_result['stderr']}")
    
    # 3. Deploy code
    print("\nStep 3: Deploying code...")
    deployer = Deployer(deploy_path="/tmp/gptbuilder_examples")
    
    deploy_result = deployer.deploy_code(
        code=code,
        name="factorial_app",
        language="python",
        metadata={
            "requirement": "factorial function",
            "auto_generated": True
        }
    )
    
    if deploy_result['success']:
        print(f"Deployed to: {deploy_result['deployment_path']}")
    
    # 4. Monitor deployment
    print("\nStep 4: Monitoring deployment...")
    monitor = MaintenanceMonitor()
    
    health = monitor.health_check(deploy_result['deployment_path'])
    print(f"Health status: {health['status']}")
    
    # 5. List all deployments
    print("\nStep 5: Listing deployments...")
    deployments = deployer.list_deployments()
    
    for dep in deployments:
        print(f"  - {dep['name']} (created: {dep['created']})")


if __name__ == "__main__":
    main()
