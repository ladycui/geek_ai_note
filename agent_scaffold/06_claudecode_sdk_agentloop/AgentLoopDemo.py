"""
Agent Loop 演示：用 Claude Agent SDK 修复 calc.py 里的 bug

观察输出你会看到完整的 loop：
  1. AssistantMessage(文本) —— 模型在"思考"，说明它打算做什么
  2. AssistantMessage(tool_use) —— 模型决定调用某个工具（Read / Edit / Bash）
  3. 工具执行结果被自动喂回模型上下文（SDK 内部完成，你看不到手写代码）
  4. 模型看到结果后决定：继续调用下一个工具，还是给出最终答案
  5. ResultMessage —— loop 结束，给出最终总结
"""

import asyncio
from dotenv import load_dotenv
import os

load_dotenv(override=True)

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
)


async def main():
    options = ClaudeAgentOptions(
        # 只允许这三个工具：读文件、改文件、跑命令
        # 这就是模型在 loop 里唯一能采取的"行动"
        allowed_tools=["Read", "Edit", "Bash"],
        # 自动接受文件编辑，方便演示（生产环境通常会做人工审批）
        permission_mode="acceptEdits",
        cwd="/home/anna/code/geek_note/agent_scaffold/06_claudecode_sdk_agentloop",
        system_prompt="你是一个严谨的 Python 工程师，修复 bug 后要用 bash 跑一下代码确认没问题。",
        max_turns=8,  # loop 最多跑 8 轮，防止无限循环
        env={
                "ANTHROPIC_BASE_URL": "https://api.moonshot.cn/anthropic",
                "ANTHROPIC_MODEL": "kimi-k2.5",
                "ANTHROPIC_SMALL_FAST_MODEL": "kimi-k2.5",
                "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            },
            setting_sources=[],
    )

    prompt = "Calc.py 里有两个可能导致除零异常的 bug，请找到并修复，修复后运行一下确认没问题。"

    print(f"=== 任务: {prompt} ===\n")

    # 这一个 async for 就是完整的 agent loop：
    # 每次循环产出一条 message，直到模型认为任务完成
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"[思考] {block.text}")
                elif isinstance(block, ToolUseBlock):
                    print(f"[行动] 调用工具: {block.name}  参数: {block.input}")
        elif isinstance(message, ResultMessage):
            print(f"\n=== Loop 结束 ===")
            print(f"总轮次: {message.num_turns}")
            print(f"最终结果: {message.result}")


if __name__ == "__main__":
    asyncio.run(main())