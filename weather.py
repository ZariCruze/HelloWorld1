# importujemy bibliotekę requests do wysyłania zapytań HTTP
import requests
# json — do zapisywania i odczytywania danych w formacie JSON
import json
# os — do sprawdzania czy plik istnieje na dysku
import os
# datetime — do pobierania aktualnej daty i godziny
from datetime import datetime

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

# ścieżka do pliku z historią sprawdzeń pogody
HISTORY_FILE = "weather_history.json"

# --- WYŚWIETLANIE HISTORII ---
# os.path.exists() sprawdza czy plik istnieje na dysku
if os.path.exists(HISTORY_FILE):
    # open() otwiera plik, "r" oznacza tryb odczytu
    # "with" automatycznie zamyka plik po zakończeniu bloku
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        # json.load() wczytuje dane JSON z pliku i zamienia na listę/słownik
        historia = json.load(f)

    # [-5:] pobiera ostatnie 5 elementów z listy (slice)
    ostatnie = historia[-5:]

    if ostatnie:
        print("📋 Ostatnie sprawdzenia pogody:")
        for wpis in ostatnie:
            print(f"   {wpis['data']} — {wpis['temperatura']}°C, "
                  f"{wpis['wilgotnosc']}%, {wpis['pogoda']}")
        print()

# budujemy URL do API open-meteo.com
# current= określa jakie dane chcemy pobrać
url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}&longitude={LONGITUDE}"
    f"&current=temperature_2m,relative_humidity_2m,weather_code"
)

# try/except przechwytuje błędy i pozwala na nie zareagować
# zamiast wyświetlać techniczny komunikat, pokazujemy przyjazną wiadomość
try:
    # requests.get() wysyła zapytanie GET do API i zwraca odpowiedź
    # timeout=10 oznacza, że czekamy maksymalnie 10 sekund na odpowiedź
    response = requests.get(url, timeout=10)

    # raise_for_status() wyrzuca błąd jeśli kod odpowiedzi to 4xx lub 5xx
    response.raise_for_status()

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

    # --- ZAPISYWANIE DO HISTORII ---
    # wczytujemy istniejącą historię lub tworzymy pustą listę
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            historia = json.load(f)
    else:
        historia = []

    # tworzymy nowy wpis jako słownik z danymi pogodowymi i datą
    nowy_wpis = {
        "data": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "temperatura": temperatura,
        "wilgotnosc": wilgotnosc,
        "pogoda": opis,
    }

    # append() dodaje element na koniec listy
    historia.append(nowy_wpis)

    # zapisujemy zaktualizowaną historię do pliku JSON
    # "w" oznacza tryb zapisu (nadpisuje plik)
    # ensure_ascii=False pozwala zapisywać polskie znaki
    # indent=2 formatuje JSON z wcięciami dla czytelności
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(historia, f, ensure_ascii=False, indent=2)

# ConnectionError — brak połączenia z internetem lub serwer niedostępny
except requests.ConnectionError:
    print("❌ Brak połączenia z internetem. Sprawdź swoje połączenie i spróbuj ponownie.")

# Timeout — serwer nie odpowiedział w wyznaczonym czasie
except requests.Timeout:
    print("❌ Serwer pogodowy nie odpowiada. Spróbuj ponownie za chwilę.")

# HTTPError — serwer zwrócił kod błędu (np. 404, 500)
except requests.HTTPError as e:
    print(f"❌ Serwer pogodowy zwrócił błąd (kod {e.response.status_code}). Spróbuj ponownie później.")

# ValueError/JSONDecodeError — odpowiedź nie jest poprawnym JSON-em
except ValueError:
    print("❌ Otrzymano nieprawidłowe dane z serwera. Spróbuj ponownie później.")

# KeyError — brak oczekiwanych pól w danych (nieoczekiwany format odpowiedzi)
except KeyError as e:
    print(f"❌ Dane pogodowe mają nieoczekiwany format (brak pola {e}). Spróbuj ponownie później.")
