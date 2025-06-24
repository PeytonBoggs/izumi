from vertexai.preview.generative_models import GenerativeModel, Tool, FunctionDeclaration, Content, Part
import requests

get_weather_func = FunctionDeclaration(
    name="get_current_weather",
    description="Get current weather by location",
    parameters={
        "type": "object",
        "properties": {
            "location": {"type": "string"}
        },
        "required": ["location"]
    }
)

weather_tool = Tool(function_declarations=[get_weather_func])
model = GenerativeModel("gemini-2.5-pro", tools=[weather_tool])

def execute_weather_tool(location: str):
    mcp_request = {
        "protocol_version": "1.0",
        "tool_id": "weather_tool",
        "method": "get_current_weather",
        "parameters": {"location": location}
    }
    
    response = requests.post("http://127.0.0.1:8000/mcp/weather", json=mcp_request)
    return response.json()["data"]

conversation = [
    Content(
        role="user",
        parts=[Part.from_text("Give me a summary of the current weather in Williamsburg, VA")]
    )
]

response = model.generate_content(
    contents=conversation,
    tools=[weather_tool]
)

if response.candidates and response.candidates[0].content.parts:
    first_part = response.candidates[0].content.parts[0]
    
    if hasattr(first_part, 'function_call') and first_part.function_call:
        func_call = first_part.function_call
        
        weather_data = execute_weather_tool(func_call.args["location"])
        
        conversation.append(response.candidates[0].content)
        
        function_response = Content(
            role="user",
            parts=[
                Part.from_function_response(
                    name="get_current_weather",
                    response={
                        "location": weather_data['location'],
                        "temperature_celsius": weather_data['temperature_celsius'],
                        "humidity_percent": weather_data['humidity_percent'],
                        "wind_speed_kmh": weather_data['wind_speed_kmh']
                    }
                )
            ]
        )
        
        conversation.append(function_response)
        
        final_response = model.generate_content(
            contents=conversation,
            tools=[weather_tool]
        )
        
        print(final_response.text)
    else:
        print("No function call detected. Model response:", response.text)
else:
    print("Unexpected response format:", response)
