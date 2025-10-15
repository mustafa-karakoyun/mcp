from typing import Any, Dict

from weather_agent import WeatherAgent

# Minimal MCP stdio server using the Python MCP SDK
try:
    from mcp import Server
    from mcp.server.stdio import stdio_server
except Exception as exc:  # pragma: no cover
    # If MCP SDK is missing, provide a clear error when run directly
    raise SystemExit(
        "mcp paketi yüklü değil. Lütfen 'pip install -r requirements.txt' komutunu çalıştırın."
    ) from exc


agent = WeatherAgent()
server = Server("weather-agent")


@server.tool()
def get_weather(city: str) -> Dict[str, Any]:
    """Fetch current weather data for a given city name."""
    return agent.get_weather(city)


if __name__ == "__main__":
    with stdio_server() as (read, write):
        server.run(read, write)
