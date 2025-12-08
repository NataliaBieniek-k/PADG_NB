from bs4 import BeautifulSoup
import requests


def get_coordinates_from_wikipedia(city):
    try:
        url = f'https://pl.wikipedia.org/wiki/{city}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        lat_elem = soup.select('.latitude')
        lon_elem = soup.select('.longitude')

        if not lat_elem or not lon_elem:
            return None

        lat = float(lat_elem[-1].text.replace(",", "."))
        lon = float(lon_elem[-1].text.replace(",", "."))
        return [lat, lon]
    except Exception:
        return None


class Clinic:
    def __init__(self, name: str, city: str):
        self.name = name
        self.city = city
        self.coords = self.get_coordinates()
        self.doctors = []
        self.clients = []
        self.marker = None

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
        self.marker = None

    def get_coordinates(self):
        return get_coordinates_from_wikipedia(self.city)

    def add_patient(self, patient):
        self.patients.append(patient)
        patient.doctor = self

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.city})"


class Patient:
    def __init__(self, first_name: str, last_name: str, city: str):
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.doctor = None
        self.coords = self.get_coordinates()
        self.marker = None

    def get_coordinates(self):
        return get_coordinates_from_wikipedia(self.city)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.city})"


class Client:
    def __init__(self, name: str, city: str):
        self.name = name
        self.city = city
        self.clinic = None
        self.coords = self.get_coordinates()
        self.marker = None

    def get_coordinates(self):
        return get_coordinates_from_wikipedia(self.city)