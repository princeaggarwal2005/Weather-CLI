import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


base_url="http://api.weatherapi.com/v1"

while True:
    inp=int(input("""Press 1 for forecast, 2 for current weather, 3 to exit..\n"""))
    if inp in [1,2]:
        c="/forecast.json" if inp==1 else "/current.json"

        query=input("Enter the city or coordinates you wish to check:\n") 
        alerts=input("Do you wish to see weather alerts? Yes or No?:\n")
        days = int(input("Enter the number of days for the forecast...\n")) if inp==1 else None
        aqi=input("Do you wish to see the aqi? Yes or no?\n")

        payload={}

        if inp==2:
            payload.update({"key":os.getenv("WEATHER_API"),"q":query,"alerts":alerts.lower(),"aqi":aqi.lower()})
        elif inp==1:
            payload.update({"key":os.getenv("WEATHER_API"),"q":query, "days":days,"alerts":alerts.lower(),"aqi":aqi.lower()})


        r=requests.get(base_url+c,params=payload)
        data=json.loads(r.text)
        current=data["current"]

        response =  {"Location":data["location"],"Temperature in Celsius":current.get("temp_c"), 
                    "Windspeed and Direction": f"""{current.get("wind_kph")} {current.get("wind_dir")}""",
                    "Precipitation": f"""{current.get("precip_in")} inches or {current.get("precip_mm")} mm""",
                    "Humidity":current.get("humidity"),
                    "Cloud Cover": current.get("cloud"),
                    "Feels Like": current.get("feelslike_c")} if aqi.lower()=="no" else {"Location":data["location"],"Temperature in Celsius":current.get("temp_c"), 
                    "Windspeed and Direction": f"""{current.get("wind_kph")} {current.get("wind_dir")}""",
                    "Precipitation": f"""{current.get("precip_in")} inches or {current.get("precip_mm")} mm""",
                    "Humidity":current.get("humidity"),
                    "Cloud Cover": current.get("cloud"),
                    "Feels Like": current.get("feelslike_c"),
                    "AQI": current.get("air_quality")}

        for keys,values in response.items():
            if keys!="AQI":
                print(f"{keys} : {values}")
            if keys=="AQI":
                print("AQI:")
                for keys, values in response.get("AQI").items():
                    print(f"\t{keys} : {values}")
    if inp==3:
        break