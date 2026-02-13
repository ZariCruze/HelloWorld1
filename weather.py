# importujemy bibliotekę requests do wysyłania zapytań HTTP
import requests

# współrzędne geograficzne Piotrkowa Trybunalskiego
LATITUDE = 51.4054
LONGITUDE = 19.7031

# słownik mapujący kody pogodowe WMO na opisy po polsku
WEATHER_CODES = {
    0: "Bezchmurnie",
    1: "Głównie bezchmurnie",
    2: "Częściowe zachmurzenie",
    3: "Pochmurno",
    45: "Mgła",
    48: "Mgła szronowa",
    51: "Mżawka lekka",
    53: "Mżawka umiarkowana",
    55: "Mżawka gęsta",
    61: "Deszcz lekki",
    63: "Deszcz umiarkowany",
    65: "Deszcz silny",
    71: "Śnieg lekki",
    73: "Śnieg umiarkowany",
    75: "Śnieg silny",
    80: "Przelotny deszcz lekki",
    81: "Przelotny deszcz umiarkowany",
    82: "Przelotny deszcz silny",
    95: "Burza",
    96: "Burza z gradem lekkim",
    99: "Burza z gradem silnym",
}

# budujemy URL do API open-meteo.com
# current= określa jakie dane chcemy pobrać
url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}&longitude={LONGITUDE}"
    f"&current=temperature_2m,relative_humidity_2m,weather_code"
)

# requests.get() wysyła zapytanie GET do API i zwraca odpowiedź
response = requests.get(url)

# sprawdzamy czy zapytanie się powiodło (kod 200 = OK)
if response.status_code == 200:
    # .json() zamienia odpowiedź z formatu JSON na słownik Pythona
    dane = response.json()
    current = dane["current"]

    temperatura = current["temperature_2m"]
    wilgotnosc = current["relative_humidity_2m"]
    kod_pogody = current["weather_code"]

    # pobieramy opis pogody ze słownika, lub "Nieznany" jeśli kodu nie ma
    opis = WEATHER_CODES.get(kod_pogody, "Nieznany kod pogody")

    print("🌤️  Aktualna pogoda w Piotrkowie Trybunalskim:")
    print(f"🌡️  Temperatura: {temperatura}°C")
    print(f"💧 Wilgotność: {wilgotnosc}%")
    print(f"☁️  Pogoda: {opis}")
else:
    print(f"Błąd pobierania danych: {response.status_code}")
