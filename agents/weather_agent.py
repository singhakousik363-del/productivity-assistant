import urllib.request

def run_weather_agent(command: str) -> str:
    command_lower = command.lower()
    
    city = "Mumbai"
    cities = ["delhi", "mumbai", "bangalore", "chennai", "kolkata",
              "hyderabad", "pune", "ahmedabad", "london", "new york",
              "singapore", "tokyo", "sydney", "dubai"]
    for c in cities:
        if c in command_lower:
            city = c.title()
            break

    try:
        url = f"https://wttr.in/{city}?format=%C+%t+%h+humidity&m"
        req = urllib.request.Request(url, headers={"User-Agent": "Wget/1.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            weather = response.read().decode("utf-8").strip()
        return f"Weather in {city}: {weather}"
    except Exception as e:
        return (
            f"Weather in {city}: Unable to fetch live data right now.\n"
            f"Tip: Check weather.com or Google for '{city} weather' for accurate info."
        )
