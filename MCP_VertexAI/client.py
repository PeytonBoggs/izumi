from vertexai.preview.generative_models import GenerativeModel, Tool, FunctionDeclaration, Content, Part
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
    response = requests.get(f"http://127.0.0.1:8000/weather/{location}")
    response.raise_for_status()
    return response.json()

weather_tool = Tool(function_declarations=[get_weather_func])

get_mlb_func = FunctionDeclaration(
    name="get_mlb",
    description="Get current MLB games",
    parameters={
        "type": "object",
        "properties": {}
    }
)

def get_mlb():
    response = requests.get(f"http://127.0.0.1:8001/mlb")
    response.raise_for_status()
    return response.json()

mlb_tool = Tool(function_declarations=[get_mlb_func])

tools = Tool(function_declarations=[get_weather_func, get_mlb_func])

system_instruction = """
You are a helpful AI assistant. You have access to two tools: one that gets the current weather from a location, and one that gets information about current MLB games.

For all other topics - general questions, conversations, coding help, explanations, etc. - respond normally without using any tools.

Only call the functions when user asks a question where your answer could be enhanced by that extra information.

You are also very smart; if the user asks what the weather is at a certain baseball game, you can look up the baseball game happening, unserstand where that game is being played by the home team, and then look up the temperature for that location.
"""

generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 1024,
}

model = GenerativeModel("gemini-2.0-flash-lite-001", tools=[tools], system_instruction=system_instruction, generation_config=generation_config)
chat = model.start_chat(history=[])
console = Console()

while True:
    prompt = input("Prompt input: ")

    response = chat.send_message(prompt)

    if (response.candidates[0].content.parts and 
        len(response.candidates[0].content.parts) > 0 and
        hasattr(response.candidates[0].content.parts[0], 'function_call') and
        response.candidates[0].content.parts[0].function_call):
        
        func_call = response.candidates[0].content.parts[0].function_call

        if func_call.name == "get_current_weather":
            function_data = get_current_weather(**func_call.args)
        elif func_call.name == "get_mlb":
            function_data = get_mlb()
        else:
            function_data = {"error": "Unknown function"}
        
        response = chat.send_message(
            Content(
                role="function",
                parts=[Part.from_function_response(
                    name=func_call.name,
                    response=function_data
                )]
            )
        )

    console.print(Markdown(response.text))