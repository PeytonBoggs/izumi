from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/weather/{location}")
async def get_weather(location: str):
    try:
        geocode_url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1"
        geocode_headers = {"User-Agent": "Weather-Server/1.0"}
        geocode_response = requests.get(geocode_url, headers=geocode_headers)
        
        if geocode_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to get location data")
        
        geocode_data = geocode_response.json()
        if not geocode_data:
            raise HTTPException(status_code=404, detail="Location not found")
        
        lat, lon = geocode_data[0]["lat"], geocode_data[0]["lon"]
        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation_probability,wind_speed_10m&wind_speed_unit=mph&temperature_unit=fahrenheit&precipitation_unit=inch"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        current = weather_data.get("current", {})
        
        return {
            "location": location,
            "temperature_fahrenheit": current.get("temperature_2m"),
            "humidity_percent": current.get("relative_humidity_2m"),
            "precipitation_probability": current.get("precipitation_probability"),
            "wind_speed_mph": current.get("wind_speed_10m")
        }
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))