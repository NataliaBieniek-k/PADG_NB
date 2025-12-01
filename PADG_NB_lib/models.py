import requests
from bs4 import BeautifulSoup

def get_coordinates_from_wikipedia(city: str):
    try:
        url = f"https://pl.wikipedia.org/wiki/{city}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)

        html = BeautifulSoup(response.text, "html.parser")

        lat = html.select_one(".latitude")
        lon = html.select_one(".longitude")

        if not lat or not lon:
            raise ValueError("Brak koordynatów")

        latitude = float(lat.text.replace(",", "."))
        longitude = float(lon.text.replace(",", "."))

        return [latitude, longitude]

    except Exception:
        return [52.2297, 21.0122]


class Clinic:
    def __init__(self, name: str, city: str):
        self.name = name
        self.city = city
        self.coords = self.get_coordinates()
        self.doctors = []
        self.clients = []

    def get_coordinates(self):
        return get_coordinates_from_wikipedia(self.city)

    def add_doctor(self, doctor):
        self.doctors.append(doctor)
        doctor.clinic = self

    def add_client(self, client):
        self.clients.append(client)
        client.clinic = self


class Doctor:
    def __init__(self, first_name: str, last_name: str, city: str):
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.clinic = None
        self.patients = []
        self.coords = self.get_coordinates()

    def get_coordinates(self):
        return get_coordinates_from_wikipedia(self.city)

    def add_patient(self, patient):
        self.patients.append(patient)
        patient.doctor = self


class Patient:
    def __init__(self, first_name: str, last_name: str, city: str):
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.doctor = None
        self.coords = self.get_coordinates()

    def get_coordinates(self):
        return get_coordinates_from_wikipedia(self.city)


class Client:
    def __init__(self, name: str, city: str):
        self.name = name
        self.city = city
        self.clinic = None
        self.coords = self.get_coordinates()

    def get_coordinates(self):
        return get_coordinates_from_wikipedia(self.city)
