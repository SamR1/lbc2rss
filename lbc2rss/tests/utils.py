# flake8: noqa

from dataclasses import dataclass
from datetime import datetime
from typing import Generator, List, Tuple


@dataclass
class SearchResult:
    title: str = 'Studio 30m2'
    category: str = 'locations'
    publication_date: datetime = datetime.strptime('2020-08-15', '%Y-%m-%d')
    price_per_square: float = 22.63
    price: int = 430
    coordinates: Tuple[float, float] = (45.76686, 4.89437)
    real_estate_type: str = 'appartement'
    square: int = 19
    url: str = 'https://www.leboncoin.fr/locations/0123456789.htm'
    thumbnail = 'https://img0.leboncoin.fr/ad-thumb/0123456789.jpg'


FORMATTED_ITEM = """<blockquote>
    <p>
        <strong>Date</strong> : 2020-08-15 00:00:00<br />
        <strong>Prix</strong> : 430 €
        (<em>22.63 €/m²</em>)
        <br />
        <strong>Type</strong> : appartement<br />
        <strong>Surface</strong> : 19 m²<br />
        <br />
        <a href="https://www.leboncoin.fr/locations/0123456789.htm" target="_blank">
            <img src="https://img0.leboncoin.fr/ad-thumb/0123456789.jpg" alt="Photo de l'offre">
        </a>
    </p>
</blockquote>"""


def get_results(values: List) -> Generator:
    for value in values:
        yield value
