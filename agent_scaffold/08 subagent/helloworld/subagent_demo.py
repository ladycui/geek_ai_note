import asyncio
import os
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

from dotenv import load_dotenv

load_dotenv(override=True)

async def main():
    async for message in query(
        prompt="Review the authentication module for security issues",
        options=ClaudeAgentOptions(
            # Auto-approve these tools, including Agent for subagent invocation
            allowed_tools=["Read", "Grep", "Glob"],
            agents={
                "code-reviewer": AgentDefinition(
                    # description tells Claude when to use this subagent
                    description="Expert code review specialist. Use for quality, security, and maintainability reviews.",
                    # prompt defines the subagent's behavior and expertise
                    prompt="""You are a code review specialist with expertise in security, performance, and best practices.

When reviewing code:
- Identify security vulnerabilities
- Check for performance issues
- Verify adherence to coding standards
- Suggest specific improvements

Be thorough but concise in your feedback.""",
                    # tools restricts what the subagent can do (read-only here)
                    tools=["Read", "Grep", "Glob"],
                    # model overrides the default model for this subagent
                    model="sonnet",
                ),
                "test-runner": AgentDefinition(
                    description="Runs and analyzes test suites. Use for test execution and coverage analysis.",
                    prompt="""You are a test execution specialist. Run tests and provide clear analysis of results.

Focus on:
- Running test commands
- Analyzing test output
- Identifying failing tests
- Suggesting fixes for failures""",
                    # Bash access lets this subagent run test commands
                    tools=["Bash", "Read", "Grep"],
                ),
            },
            env={
                    "ANTHROPIC_BASE_URL": "https://api.moonshot.cn/anthropic",
                    "ANTHROPIC_MODEL": "kimi-k2.5",
                    "ANTHROPIC_SMALL_FAST_MODEL": "kimi-k2.5",
                    "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
                },
            setting_sources=[],
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)


asyncio.run(main())