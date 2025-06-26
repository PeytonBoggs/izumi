from vertexai.preview.generative_models import GenerativeModel, Tool, ToolConfig, FunctionDeclaration, Content, Part
from rich.console import Console
from rich.markdown import Markdown
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

def get_current_weather(location: str):
    mcp_request = {
        "protocol_version": "1.0",
        "tool_id": "weather_tool",
        "method": "get_current_weather",
        "parameters": {"location": location}
    }
    
    response = requests.post("http://127.0.0.1:8000/mcp/weather", json=mcp_request)
    return response.json()["data"]

weather_tool = Tool(function_declarations=[get_weather_func])

system_instruction = """
You are a helpful AI assistant. You have access to tool that gets the current weather from a location, nothing else.

For all other topics - general questions, conversations, coding help, explanations, etc. - respond normally without using any tools.

Only call the weather function when user asks about the current weather.

For everything else, just have a normal conversation.
"""

model = GenerativeModel("gemini-2.5-pro", tools=[weather_tool], system_instruction=system_instruction)
chat = model.start_chat(history=[])

console = Console()

conversation = []
while True:
    prompt = input("Prompt input: ")

    response = chat.send_message(prompt)

    if (response.candidates[0].content.parts and 
        len(response.candidates[0].content.parts) > 0 and
        hasattr(response.candidates[0].content.parts[0], 'function_call') and
        response.candidates[0].content.parts[0].function_call):
        
        func_call = response.candidates[0].content.parts[0].function_call
        weather_data = get_current_weather(**func_call.args)
        
        response = chat.send_message(
            Content(
                role="function",
                parts=[Part.from_function_response(
                    name=func_call.name,
                    response=weather_data
                )]
            )
        )

    console.print(Markdown(response.text))