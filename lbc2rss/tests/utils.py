# flake8: noqa

from dataclasses import dataclass
from datetime import datetime
from typing import Generator, List, Tuple


@dataclass
class SearchResult:
    title: str = 'Studio 30m2'
    category: str = 'locations'
    body: str = "Studio à louer au calme"
    publication_date: datetime = datetime.strptime('2020-08-15', '%Y-%m-%d')
    publication_date_str: str = '2020-08-15 00:00:00'
    price_per_square: float = 22.63
    price: int = 430
    charges_included: str = 'oui'
    coordinates: Tuple[float, float] = (45.759723, 4.842223)
    city_label: str = 'Lyon, 69000'
    real_estate_type: str = 'appartement'
    square: int = 19
    url: str = 'https://www.leboncoin.fr/locations/0123456789.htm'
    thumbnail = 'https://img0.leboncoin.fr/ad-thumb/0123456789.jpg'
    images = [
        'https://img0.leboncoin.fr/ad-thumb/0101010101.jpg',
        'https://img0.leboncoin.fr/ad-thumb/2323232323.jpg',
        'https://img0.leboncoin.fr/ad-thumb/4545454545.jpg',
    ]


FORMATTED_ITEM = """<blockquote>
    <p>
        <strong>Date</strong> : 2020-08-15 00:00:00<br />
        <strong>Prix</strong> : 430 €
        (charges comprises: oui,
        <em>prix au m²: 22.63 €/m²</em>)
        <br />
        <strong>Type</strong> : appartement<br />
        <strong>Surface</strong> : 19 m²<br />
        <strong>Description</strong> : Studio à louer au calme<br />
        <br /><img src="https://img0.leboncoin.fr/ad-thumb/0101010101.jpg" alt="Photo de l'offre"><br />
        <br /><img src="https://img0.leboncoin.fr/ad-thumb/2323232323.jpg" alt="Photo de l'offre"><br />
        <br /><img src="https://img0.leboncoin.fr/ad-thumb/4545454545.jpg" alt="Photo de l'offre"><br />

    </p>
</blockquote>"""


def get_results(values: List) -> Generator:
    for value in values:
        yield value
