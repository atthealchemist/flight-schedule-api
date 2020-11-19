import json
from dataclasses import dataclass
from string import Template

from manager import AirportManager
from utils import parse_time_from_date_string, calculate_flight_duration


@dataclass
class FlightInfo:
    flight_number: str
    departure_airport: str
    departure_airport_iata: str
    arrival_airport: str
    arrival_airport_iata: str
    departure_time: str
    arrival_time: str
    duration: str
    terminal: str
    delayed: bool = False

    @staticmethod
    def from_dict(info):
        return FlightInfo(
            flight_number="{}{}".format(info.get('transport').get('carrierCode'), info.get('transport').get('number')),
            departure_airport=AirportManager.build_airport_name(info.get('origin')),
            departure_airport_iata=info.get('origin'),
            arrival_airport=AirportManager.build_airport_name(info.get('destination')),
            arrival_airport_iata=info.get('destination'),
            departure_time=parse_time_from_date_string(info.get('std')),
            arrival_time=parse_time_from_date_string(info.get('sta')),
            duration=calculate_flight_duration(info.get('std'), info.get('sta')),
            delayed=bool(info.get('delay_Departure')),
            terminal=info.get('terminal', 'Not assigned')
        )

    def __str__(self):
        flight_info_template = Template(
            """
        [$flight_departure_time - $flight_arrival_time] $flight_departure_airport -> $flight_arrival_airport <$flight_number> 
        """.strip()
        )

        substituted_flight_info = flight_info_template.safe_substitute(
            flight_number=self.flight_number,
            flight_departure_airport=self.departure_airport,
            flight_arrival_airport=self.arrival_airport,
            flight_departure_time=self.departure_time,
            flight_arrival_time=self.arrival_time
        )

        return substituted_flight_info
