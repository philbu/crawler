import json
import os
import time
from configparser import ConfigParser
from dataclasses import asdict, dataclass
from typing import List, Optional

import requests

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

config = ConfigParser()
config.read(os.path.join(__location__, 'config.ini'))
base = config.get("Api", "base")
from_station = config.get("Api", "fromStation")
to_station = config.get("Api", "toStation")
user_agent = config.get("Api", "userAgent")
output_directory = config.get("Directory", "outputDirectory")

url = f"{base}?fromStation={from_station}&toStation={to_station}&sapTickets=false&transportTypeCallTaxi=false&time="


@dataclass
class Connection:
    departure: int
    arrival: int
    labels: List[str]
    delays: List[int]
    arr_delays: List[int]
    cancelled: List[bool]


@dataclass
class AnalysisJson:
    status: str
    connections: Optional[List[Connection]]
    error_msg: Optional[str]


def current_milli_time():
    return str(round(time.time() * 1000))


def main():
    request_time = str(int(time.time()))
    headers = {"user-agent": user_agent}
    r = requests.get(url + current_milli_time(), headers=headers)
    analysisJson = AnalysisJson(r.status_code, None, "")

    # with open("test1.json", "w") as outfile:
    #    json.dump(r.json(), outfile)
    if r.status_code == requests.codes.ok:
        connections: List[Connection] = []
        if "connectionList" in r.json():
            for connection in r.json()["connectionList"]:
                departure = connection["departure"]
                arrival = connection["arrival"]
                labels = []
                delays = []
                arr_delays = []
                cancelled = []
                if "connectionPartList" in connection:
                    for connection_part in connection["connectionPartList"]:
                        labels.append(connection_part.get("label", ""))
                        delays.append(connection_part.get("delay", 0))
                        arr_delays.append(connection_part.get("arrDelay", 0))
                        cancelled.append(connection_part.get("cancelled", False))
                conn = Connection(
                    departure, arrival, labels, delays, arr_delays, cancelled
                )
                connections.append(conn)
        analysisJson.connections = connections
    else:
        analysisJson.error_msg = r.reason

    with open(f"{output_directory}/{request_time}.json", "w") as outfile:
        json.dump(asdict(analysisJson), outfile)


if __name__ == "__main__":
    main()
