import json


class AirportManager:

    def fetch_airports_from_json(self):
        with open('../../assets/airports.json', 'r+') as file:
            content = file.read()
            return json.loads(content)

    def find_airport_by_iata(self, iata):
        airport, *_ = filter(lambda a: a.get('iata_code') == iata.upper(), self.fetch_airports_from_json())
        return airport

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
