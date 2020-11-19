from datetime import datetime
from string import Template

from fetcher import FlightFetcher
from schedule import FlightSchedule


def main():
    fetcher = FlightFetcher()
    fetcher.fetch_flight_info()

    schedule = FlightSchedule(flight_fetcher=fetcher)
    schedule.print()

    # print_flight_schedule(flight_date=datetime(2020, 11, 19), from_moscow=True)


if __name__ == "__main__":
    main()
