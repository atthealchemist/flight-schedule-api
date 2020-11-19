import sys
from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import FastAPI, Path, Query
import uvicorn

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


@app.get('/airports/{iata}',
         tags=['airports'],
         summary="Get list of airports")
def get_airports(iata: str = Path(..., description="IATA code of airport ('all' for all airports)", max_length=3),
                 page: Optional[int] = 5,
                 limit: Optional[int] = 10):
    """
    Get list of airports, could be limited by concrete count and paginated
    """
    manager = AirportManager()
    airports = manager.fetch_airports_from_json()
    pages_count = int(len(airports) / limit)
    count = limit * page
    if iata != 'all':
        airports = manager.find_airport_by_iata(iata)
        result = airports
    else:
        airports = airports[count:count + limit]
        result = dict(page=page, total_pages=pages_count, airports=airports)
    return result


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

    if printable:
        flights = str(flight_schedule)
    return dict(count=len(flights),
                date=flight_date,
                direction=direction,
                departure_airport_iata=departure_airport_iata,
                arrival_airport_iata=arrival_airport_iata,
                flights=flights)


def main():
    server = load_config(section='server')

    used_loop = 'asyncio' if 'win' in sys.platform else 'auto'
    uvicorn.run(app, host=server.get('host'), port=server.get('port'), loop=used_loop)


if __name__ == "__main__":
    main()
