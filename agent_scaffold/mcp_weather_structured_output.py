from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Service")


class WeatherInfo(BaseModel):
    location: str = Field(description="The location name")
    temperature: float = Field(description="Temperature in Celsius")
    conditions: str = Field(description="Weather conditions")
    humidity: int = Field(description="Humidity percentage", ge=0, le=100)


@mcp.tool(
    name="get_weather_info",
    description="获取指定地点的天气信息并作为结构化数据输出",
)
def get_weather_info(city: str) -> WeatherInfo:
    return WeatherInfo(
        location=city,
        temperature=22.5,
        conditions="partly cloudy",
        humidity=65,
    )
    
if __name__ == "__main__":
    mcp.run(transport="streamable-http")