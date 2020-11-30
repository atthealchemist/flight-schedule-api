from modules.core.utils import fetch_airports_from_json, image_to_base64


class AirportManager:

    def fetch_airports(self):
        self.airports = fetch_airports_from_json()

    def find_airports(self, query):
        airports = list(filter(query, self.airports))
        if self.fetch_images:
            airports = [dict(a, image=image_to_base64("./assets/images/{iata}.jpg".format(
                iata=a.get('iata').lower()))) for a in airports]
        return airports

    def find_airport_by_iata(self, iata):
        return self.find_airports(lambda a: a.get('iata') == iata.upper())

    def find_airports_by_city(self, city):
        return self.find_airports(lambda a: a.get('city').lower() == city.lower())

    def find_airports_by_country(self, country):
        return self.find_airports(lambda a: a.get('country').lower() == country.lower())

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

    def __init__(self, fetch_images=False):
        self.airports = list()
        self.fetch_images = fetch_images
        self.fetch_airports()
