from fastapi import FastAPI, HTTPException
import requests
from datetime import date
import uvicorn

app = FastAPI()

@app.get("/mlb")
async def get_mlb_data():
    try:
        today = date.today().strftime("%Y-%m-%d")
        url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today}&hydrate=linescore,team"
        
        response = requests.get(url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to get MLB data")
        
        data = response.json()
        games = []
        
        for game_date in data.get("dates", []):
            for game in game_date.get("games", []):
                teams = game.get("teams", {})
                away_team = teams.get("away", {}).get("team", {})
                home_team = teams.get("home", {}).get("team", {})
                
                linescore = game.get("linescore", {})
                status = game.get("status", {})
                
                games.append({
                    "away_team": away_team.get("name"),
                    "home_team": home_team.get("name"),
                    "away_score": linescore.get("teams", {}).get("away", {}).get("runs"),
                    "home_score": linescore.get("teams", {}).get("home", {}).get("runs"),
                    "status": status.get("detailedState"),
                    "inning": linescore.get("currentInning"),
                    "inning_state": linescore.get("inningState")
                })
        
        return {
            "date": today,
            "total_games": len(games),
            "games": games
        }
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)