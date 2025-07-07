from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import requests
import uvicorn
import os

load_dotenv()
GMAPS_API_KEY = os.getenv('GMAPS_API_KEY')

app = FastAPI()

@app.get("/distance/{pointa}/{pointb}")
async def get_distance(pointa: str, pointb: str):
    try:
        response = requests.get(f"https://maps.googleapis.com/maps/api/distancematrix/json?destinations={pointb}&origins={pointa}&units=imperial&key={GMAPS_API_KEY}")

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to get distance")

        data = response.json()

        rows = data.get("rows", [])
        elements = rows[0]["elements"] if rows and "elements" in rows[0] else []
        if not elements or elements[0].get("status") != "OK":
            raise HTTPException(status_code=400, detail="No route found or invalid locations.")

        return {
            "origin_addresses": data.get("origin_addresses"),
            "destination_addresses": data.get("destination_addresses"),
            "distance": elements[0]["distance"]["text"],
            "duration": elements[0]["duration"]["text"]
        }
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)