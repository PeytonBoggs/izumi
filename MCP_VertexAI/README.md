This is a use case example for the Izumi paper, demonstrating communication between a client that contains an LLM and multiple servers. The client file initializes a Gemini model chat, which decides whether or not to use its tools based on user input. These tools send API requests to their respective servers, who gather information to enhance the response of the LLM.

To run the client: python client.py

To run the weather server: python server_weather.py (starts server on localhost:8000)

To run the MLB server: python server_mlb.py (starts server on localhost:8001)