"""
Code Generator Module - Uses GPT to generate code autonomously
"""

import os
import logging
from typing import Dict, Optional
from openai import OpenAI


class CodeGenerator:
    """
    Autonomous code generation using GPT models
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize the code generator

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: GPT model to use (default: gpt-4)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self.logger = logging.getLogger(__name__)

    def generate_code(
        self, requirement: str, language: str = "python", context: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate code based on requirements

        Args:
            requirement: Description of what code to generate
            language: Programming language (default: python)
            context: Additional context or existing code

        Returns:
            Dictionary containing generated code and metadata
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured")

        system_prompt = f"""You are an expert {language} developer.
Generate clean, well-documented, production-ready code based on the user's requirements.
Include error handling, type hints, and follow best practices."""

        user_prompt = f"Requirement: {requirement}"
        if context:
            user_prompt += f"\n\nContext:\n{context}"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
            )

            generated_code = response.choices[0].message.content

            return {
                "code": generated_code,
                "language": language,
                "requirement": requirement,
                "model": self.model,
                "tokens_used": response.usage.total_tokens,
            }
        except Exception as e:
            self.logger.error(f"Code generation failed: {str(e)}")
            raise

    def refine_code(self, code: str, feedback: str, language: str = "python") -> str:
        """
        Refine existing code based on feedback

        Args:
            code: Existing code to refine
            feedback: Feedback or requirements for refinement
            language: Programming language

        Returns:
            Refined code
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured")

        prompt = f"""Here is some {language} code:

```{language}
{code}
```

Please refine this code based on the following feedback:
{feedback}

Provide only the refined code without explanations."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Code refinement failed: {str(e)}")
            raise

    def generate_tests(self, code: str, language: str = "python") -> str:
        """
        Generate tests for the given code

        Args:
            code: Code to generate tests for
            language: Programming language

        Returns:
            Generated test code
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured")

        prompt = f"""Generate comprehensive unit tests for this {language} code:

```{language}
{code}
```

Include edge cases and error conditions. Use pytest for Python."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Test generation failed: {str(e)}")
            raise
