# importujemy moduł datetime, który pozwala pracować z datą i czasem
from datetime import datetime

# input() wyświetla tekst w nawiasie i czeka aż użytkownik wpisze odpowiedź
# wpisana wartość zostaje zapisana w zmiennej "imie"
imie = input("Jak masz na imię? ")

# datetime.now() pobiera aktualną datę i godzinę
# strftime() formatuje datę jako tekst, np. "12.02.2026 14:30"
teraz = datetime.now().strftime("%d.%m.%Y %H:%M")

# print() wypisuje tekst na ekranie
# f"..." to f-string, który pozwala wstawiać zmienne w tekst za pomocą {nazwa_zmiennej}
print(f"Cześć {imie}! To mój pierwszy program napisany z Claude Code")
print(f"Dzisiaj jest: {teraz}")

# len() zwraca długość (liczbę znaków) tekstu
liczba_liter = len(imie)
print(f"Twoje imię ma {liczba_liter} liter.")
