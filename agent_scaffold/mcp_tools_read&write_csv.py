import csv
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp common server", host="0.0.0.0", port=38000) # default port 8000

@mcp.tool()
def read_csv(file_path: str) -> list[dict]:
    """读取指定CSV文件的内容，返回包含字典的列表。
    smolagents 对 MCP 工具调用的一个特定限制：从 MCP Server 转换过来的 Tool 对象，在调用时不允许用位置参数，只能用关键字参数传参。smolagents 对 MCP 工具调用的一个特定限制：从 MCP Server 转换过来的 Tool 对象，在调用时不允许用位置参数，只能用关键字参数传参。
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    if not path.suffix.lower() == ".csv":
        raise ValueError(f"不是CSV文件: {file_path}")

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


@mcp.tool()
def write_md(file_path: str, content: str) -> str:
    """将markdown内容写入到指定的md文件中。"""
    path = Path(file_path)
    if path.suffix.lower() != ".md":
        raise ValueError(f"目标文件必须是.md后缀: {file_path}")

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write(content)
    return f"成功写入 {file_path}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
