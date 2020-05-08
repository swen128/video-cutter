from csv import DictReader
from typing import Iterator, Dict
from datetime import timedelta


def read_csv(path) -> Iterator[Dict[str, str]]:
    with open(path, encoding='utf-8-sig') as file:
        for row in DictReader(file):
            yield row


def parse_timestamp(time: str) -> timedelta:
    h, m, s = [int(x, base=10) for x in time.strip().split(':')]
    return timedelta(hours=h, minutes=m, seconds=s)
