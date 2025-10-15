import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

class WeatherAgent:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city: str) -> Dict[str, Any]:
        if not city or not isinstance(city, str):
            return {"error": "Geçerli bir şehir adı giriniz."}

        if not self.api_key:
            return {"error": "OPENWEATHER_API_KEY eksik. Lütfen .env dosyasına ekleyin."}

        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "tr",
        }

        try:
            res = requests.get(self.base_url, params=params, timeout=10)
        except requests.exceptions.RequestException:
            return {"error": "Ağ isteği başarısız oldu. İnternet bağlantınızı kontrol edin."}

        if res.status_code == 200:
            data = res.json()
            try:
                desc = data["weather"][0]["description"].capitalize()
                temp = data["main"]["temp"]
                feels = data["main"]["feels_like"]
            except (KeyError, IndexError, TypeError):
                return {"error": "Beklenmeyen API yanıtı alındı."}

            return {
                "city": city,
                "temp": f"{temp}°C",
                "feels_like": f"{feels}°C",
                "condition": desc,
            }

        if res.status_code == 401:
            return {"error": "API anahtarı geçersiz veya yetkisiz (401)."}
        if res.status_code == 404:
            return {"error": "Şehir bulunamadı (404)."}

        try:
            detail = res.json().get("message")
        except ValueError:
            detail = None
        return {"error": f"API hatası: {res.status_code}" + (f" - {detail}" if detail else "")}

if __name__ == "__main__":
    agent = WeatherAgent()
    result = agent.get_weather("Samsun")
    print(result)
