import requests
from bs4 import BeautifulSoup

def get_coordinates_from_wikipedia(city_name: str):
    url = f'https://pl.wikipedia.org/wiki/{city_name}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    latitudes = soup.select('.latitude')
    longitudes = soup.select('.longitude')

    lat = float(latitudes[-1].text.replace(",", "."))
    lon = float(longitudes[-1].text.replace(",", "."))
    return [lat, lon]


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
    def __init__(self, first_name: str, last_name: str, city: str = None):
        self.first_name = first_name
        self.last_name = last_name
        self.clinic = None
        self.patients = []
        self.coords = self.get_coordinates()

    def add_patient(self, patient):
        self.patients.append(patient)
        patient.doctor = self


class Patient:
    def __init__(self, first_name: str, last_name: str, city: str):
        self.first_name = first_name
        self.last_name = last_name
        self.doctor = None
        self.coords = self.get_coordinates()


class Client:
    def __init__(self, name: str, city: str):
        self.name = name
        self.clinic = None
        self.coords = self.get_coordinates()
