from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gptbuilderauto",
    version="0.1.0",
    author="GPTbuilderauto",
    description="ChatGPT fully autonomous code creation, execution, deployment, and maintenance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/copperlang2007/GPTbuilderauto",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "docker>=6.0.0",
        "pyyaml>=6.0",
        "click>=8.0.0",
        "requests>=2.31.0",
        "GitPython>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "gptbuilder=gptbuilderauto.cli:main",
        ],
    },
)
