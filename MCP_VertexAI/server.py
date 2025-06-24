from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class MCPRequest(BaseModel):
    protocol_version: str
    tool_id: str
    method: str
    parameters: dict

class MCPResponse(BaseModel):
    protocol_version: str
    tool_id: str
    status: str
    data: dict = None
    error_message: str = None

@app.post("/mcp/weather")
async def weather_tool(request: MCPRequest):
    location = request.parameters.get("location")

    if not location:
        return MCPResponse(
            protocol_version=request.protocol_version,
            tool_id=request.tool_id,
            status="error",
            error_message="Missing location parameter"
        )
    
    try:
        geocode_url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1"
        geocode_headers = {"User-Agent": "MCP-Server/1.0 (prboggs@wm.edu)"}
        geocode_response = requests.get(geocode_url, headers=geocode_headers)

        if geocode_response.status_code != 200 or not geocode_response.text.strip():
            return MCPResponse(
                protocol_version=request.protocol_version,
                tool_id=request.tool_id,
                status="error",
                error_message="Failed to get geocoding data"
            )

        geocode_data = geocode_response.json()

        if not geocode_data:
            return MCPResponse(
                protocol_version=request.protocol_version,
                tool_id=request.tool_id,
                status="error",
                error_message="Location not found"
            )

        latitude = geocode_data[0]["lat"]
        longitude = geocode_data[0]["lon"]

        open_meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=auto"

        response = requests.get(open_meteo_url)
        data = response.json()

        current_weather = data.get("current", {})

        return MCPResponse(
            protocol_version=request.protocol_version,
            tool_id=request.tool_id,
            status="success",
            data={
                "location": location,
                "temperature_celsius": current_weather.get("temperature_2m"),
                "humidity_percent": current_weather.get("relative_humidity_2m"),
                "wind_speed_kmh": current_weather.get("wind_speed_10m")
            }
        )
    except Exception as e:
        return MCPResponse(
            protocol_version=request.protocol_version,
            tool_id=request.tool_id,
            status="error",
            error_message=str(e)
        )

