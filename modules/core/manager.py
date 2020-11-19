import json


class AirportManager:

    def fetch_airports_from_json(self):
        with open('assets/airports.json', 'r+') as file:
            content = file.read()
            return json.loads(content)

    def find_airport_by_iata(self, iata):
        airport, *_ = filter(lambda a: a.get('iata') == iata.upper(), self.fetch_airports_from_json())
        return airport

    def find_airports_by_city(self, city):
        airports = filter(lambda a: a.get('city').lower() == city.lower(), self.fetch_airports_from_json())
        return list(airports)

    def find_airports_by_country(self, country):
        airports = filter(lambda a: a.get('country').lower() == country.lower(), self.fetch_airports_from_json())
        return list(airports)

    @staticmethod
    def build_airport_name(iata):
        airport_name = "{name}, {city} ({country})"
        manager = AirportManager()
        airport = manager.find_airport_by_iata(iata)
        return airport_name.format(
            name=airport.get('name'),
            city=airport.get('city'),
            country=airport.get('country')
        )

    def __init__(self):
        pass
