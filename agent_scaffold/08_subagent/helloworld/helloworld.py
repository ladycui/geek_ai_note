import asyncio
import os
from claude_agent_sdk import (
    query,
    tool,
    create_sdk_mcp_server,
    ClaudeAgentOptions,
    AgentDefinition,
)

from dotenv import load_dotenv

load_dotenv(override=True)

# 用 @tool 定义一个真正会被子agent执行的小函数
# 参数分别是：工具名、工具描述、输入参数schema（这里不需要参数，传空字典）
@tool("say_hello", "打印一行日志，并返回一句问候语", {})
async def say_hello(args):
    # 这行 print 会在你本地终端里真实打印出来，
    # 说明子agent确实调用并执行了这个函数
    print("[say_hello 函数被执行] 这是子agent内部调用的真实 Python 代码")

    return {
        "content": [
            {"type": "text", "text": "Hello World! 这是函数返回的问候语。"}
        ]
    }


# 把上面的函数注册成一个"MCP工具服务"，供子agent使用
greeter_tools_server = create_sdk_mcp_server(
    name="greeter-tools",
    version="1.0.0",
    tools=[say_hello],
)


async def main():
    async for message in query(
        prompt="请用 greeter 子agent 打招呼",
        options=ClaudeAgentOptions(
            # mcp__{server名}__{工具名} 是固定的命名规则
            allowed_tools=["Agent", "mcp__greeter-tools__say_hello"],
            mcp_servers={"greeter-tools": greeter_tools_server},
            agents={
                "greeter": AgentDefinition(
                    description="负责打招呼的助手。当用户想要问候或说 hello world 时使用。",
                    prompt="""你是一个友好的问候助手。
不管收到什么请求，你都必须调用 say_hello 工具来完成问候，
然后把工具返回的文本原样告诉用户，不要自己编造内容。
""",
                    tools=["mcp__greeter-tools__say_hello"],
                    model="kimi-k2.5",
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
        print(type(message).__name__, message)


asyncio.run(main())