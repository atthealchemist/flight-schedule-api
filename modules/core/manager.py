import json


class AirportManager:

    def fetch_airports_from_json(self):
        with open('assets/airports.json', 'r+') as file:
            content = file.read()
            self.airports = json.loads(content)

    def find_airport_by_iata(self, iata):
        airports = [a for a in self.airports if a.get('iata') == iata.upper()]
        return airports

    def find_airports_by_city(self, city):
        airports = [a for a in self.airports if a.get('city').lower() == city.lower()]
        return airports

    def find_airports_by_country(self, country):
        airports = [a for a in self.airports if a.get('country').lower() == country.lower()]
        return airports

    @staticmethod
    def build_airport_name(iata):
        airport_name = "{name}, {city} ({country})"
        manager = AirportManager()
        airport, *_ = manager.find_airport_by_iata(iata)
        return airport_name.format(
            name=airport.get('name'),
            city=airport.get('city'),
            country=airport.get('country')
        )

    def __init__(self):
        self.airports = list()

        self.fetch_airports_from_json()
