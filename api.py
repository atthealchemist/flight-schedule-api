import sys
from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import FastAPI, Path, Query
import uvicorn
from starlette.responses import PlainTextResponse

from modules.entities.route import FlightRoute
from modules.core.fetcher import FlightFetcher
from modules.core.manager import AirportManager
from modules.entities.schedule import FlightSchedule
from modules.core.utils import load_config

app = FastAPI(
    title="Pobeda Schedule API",
    description="`Schedule API for Pobeda airlines created by @thealchemist`",
    version="v1.0"
)


class Direction(str, Enum):
    BOTH = 'both'
    FORWARD = 'forward'
    BACKWARD = 'backward'


@app.get('/',
         tags=['home'],
         summary="Show current datetime",
         description="Just responding datetime.now()")
def home():
    return dict(now=str(datetime.now()))


@app.get('/airports/',
         tags=['airports'],
         summary="Get list of airports")
def get_airports(iata: Optional[str] = '',
                 country: Optional[str] = '',
                 city: Optional[str] = '',
                 page: Optional[int] = 1,
                 limit: Optional[int] = 10):
    """
    Get list of airports, could be limited by concrete count and paginated
    """
    manager = AirportManager()
    airports = manager.airports

    if country:
        airports = manager.find_airports_by_country(country)
    if city:
        airports = manager.find_airports_by_city(city)
    if iata:
        airports = manager.find_airport_by_iata(iata)
    if page and limit:
        pages_count = int(len(airports) / limit)
        count = limit * page
        if not city and not country and not iata:
            airports = airports[count:count + limit]
            airports = dict(page=page, total_pages=pages_count, airports=airports)
    return dict(count=len(airports), airports=airports)


@app.get('/schedule/{departure_airport_iata}/{arrival_airport_iata}/{flight_date}/',
         tags=['schedule'],
         summary="Create a schedule on concrete date")
def schedule(
        flight_date: str = Path(..., description="Date in YYYY-MM-DD format", max_length=10),
        departure_airport_iata: str = Path(..., max_length=3),
        arrival_airport_iata: str = Path(..., max_length=3),
        direction: Direction = Query(default=Direction.BOTH, description="Flight direction"),
        printable: bool = Query(default=False, description="Output schedule in printable format")
):
    """
    Creating a schedule for concrete flight date for concrete flight direction
    """
    fetcher = FlightFetcher(
        flight_date=datetime.strptime(flight_date, "%Y-%m-%d"),
        flight_route=FlightRoute(
            departure_airport_iata=departure_airport_iata.upper(),
            arrival_airport_iata=arrival_airport_iata.upper()
        )
    )
    fetcher.fetch_flight_info()

    flight_schedule = FlightSchedule(flight_fetcher=fetcher, direction=direction)

    flights = flight_schedule.flights

    flights = dict(
        count=len(flights),
        date=flight_date,
        direction=direction,
        departure_airport_iata=departure_airport_iata,
        arrival_airport_iata=arrival_airport_iata,
        flights=flights
    )

    if printable:
        flights = PlainTextResponse(str(flight_schedule))
    return flights


def main():
    server = load_config(section='server')

    used_loop = 'asyncio' if 'win' in sys.platform else 'auto'
    uvicorn.run(app, host=server.get('host'), port=server.get('port'), loop=used_loop)


if __name__ == "__main__":
    main()
