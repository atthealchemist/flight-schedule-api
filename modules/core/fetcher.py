from datetime import datetime, date
from typing import List

import requests

from modules.entities.route import FlightRoute
from modules.entities.flight import FlightInfo
from modules.core.utils import load_config


class FlightFetcher:

    def filter_flights(self, departure: str = "", arrival: str = ""):
        departure_iata = self.flight_route.departure_airport_iata
        arrival_iata = self.flight_route.arrival_airport_iata

        forward_flight = departure == departure_iata and arrival == arrival_iata
        backward_flight = departure == arrival_iata and arrival == departure_iata

        return forward_flight or backward_flight

    def fetch_flight_info(self):
        api_url = self.config.get('api_url')
        response = requests.get(
            url=api_url.format(flight_date=self.flight_date),
            headers=self.headers,
            verify=False
        )

        json_flights = response.json()

        flights_response = json_flights.get('segments')

        filtered_flights = [f for f in flights_response if self.filter_flights(departure=f.get('origin'),
                                                                               arrival=f.get('destination'))]

        for flight in filtered_flights:
            flight_info = FlightInfo.from_dict(flight)
            self._flights.append(flight_info)

    @property
    def flights(self):
        return self._flights

    def __init__(self,
                 flight_date: date = datetime.now().date(),
                 flight_route: FlightRoute = FlightRoute(
                     departure_airport_iata='VKO',
                     arrival_airport_iata='LED'
                 )):
        self._flights: List[FlightInfo] = []
        self.flight_route: FlightRoute = flight_route
        self.flight_date: date = flight_date
        self.config: dict = load_config(section='provider')
        self.headers: dict = self.config.get('headers')
