import json
import os
import time
from configparser import ConfigParser
from dataclasses import asdict, dataclass
from typing import List, Optional
from datetime import datetime

import requests

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

config = ConfigParser()
config.read(os.path.join(__location__, "config.ini"))
base = config.get("Api", "base")
station = config.get("Api", "station")
user_agent = config.get("Api", "userAgent")
output_directory = config.get("Directory", "outputDirectory")

url = f"{base}?stationGlobalId={station}&transportTypes=SBAHN"


@dataclass
class Connection:
    plannedDepartureTime: int
    realtime: bool
    delayInMinutes: int
    destination: str
    cancelled: bool
    sev: bool
    year: str
    month: str
    day: str
    time_of_day: str


@dataclass
class AnalysisJson:
    status: int
    connections: Optional[List[Connection]]
    error_msg: Optional[str]


def current_milli_time() -> str:
    return str(round(time.time() * 1000))


def main() -> None:
    request_time = str(int(time.time()))
    headers = {"user-agent": user_agent}
    r = requests.get(url + current_milli_time(), headers=headers)
    analysisJson = AnalysisJson(r.status_code, None, "")

    if r.status_code == requests.codes.ok:
        connections: List[Connection] = []
        for c in r.json():
            year = datetime.fromtimestamp(c["plannedDepartureTime"] / 1000).strftime(
                "%Y"
            )
            month = datetime.fromtimestamp(c["plannedDepartureTime"] / 1000).strftime(
                "%m"
            )
            day = datetime.fromtimestamp(c["plannedDepartureTime"] / 1000).strftime(
                "%d"
            )
            time_of_day = datetime.fromtimestamp(
                c["plannedDepartureTime"] / 1000
            ).strftime("%H:%M")
            conn = Connection(
                c["plannedDepartureTime"],
                c["realtime"],
                c["delayInMinutes"],
                c["destination"],
                c["cancelled"],
                c["sev"],
                year,
                month,
                day,
                time_of_day,
            )
            connections.append(conn)
        analysisJson.connections = connections
    else:
        analysisJson.error_msg = r.reason

    with open(f"{output_directory}/{request_time}.json", "w") as outfile:
        json.dump(asdict(analysisJson), outfile)


if __name__ == "__main__":
    main()
