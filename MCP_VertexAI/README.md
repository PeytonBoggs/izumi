This is a test of using MCP to communicate between a client and a server. The client file calls to a Gemini model and to the server file, which contains endpoints to a weather API. The Gemini model can use this tool to retrieve up to date weather information and generate a summary for it.

To run the server: python -m uvicorn server:app --reload

To run the client: python client.py