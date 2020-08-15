import re
from typing import Dict, Generator

import pylbc
from lbc2rss.exceptions import InvalidParameters
from pylbc.exceptions import InvalidEstateType


class LBCQuery:
    def __init__(self, category: str) -> None:
        self.search = pylbc.Search()
        self.search.set_category(category)

    def add_search_parameters(self, params: Dict) -> None:
        if not params:
            raise InvalidParameters('No parameters provided.')

        real_estate_types = params.get('types', 'maison|appartement').split(
            '|'
        )
        try:
            self.search.set_real_estate_types(real_estate_types)
        except InvalidEstateType:
            raise InvalidParameters('Invalid real estate types.')

        if 'lat' in params or 'lon' in params:
            if 'lat' not in params:
                raise InvalidParameters(
                    'Missing coordinate, get only longitude.'
                )
            if 'lon' not in params:
                raise InvalidParameters(
                    'Missing coordinate, get only latitude.'
                )
            self.search.set_coordinates(
                lat=params['lat'],
                lng=params['lon'],
                radius=params.get('radius', 0),
            )
        elif 'cities' in params:
            for city in params['cities'].split('|'):
                if not re.match(
                    r'^(.)[^,]*,[^,]*(?:[0-8]\d|9[0-8])\d{3}$', city
                ):
                    raise InvalidParameters(
                        'A city must contain a name and a valid zip code '
                        '(5 digits), separated with a comma.'
                    )
                city_name, city_zip_code = city.split(',')
                self.search.add_city(city_name, city_zip_code)
        elif 'departments' in params:
            self.search.set_departments(params['departments'].split('|'))

        self.search.set_price(
            mini=params.get('price_min'), maxi=params.get('price_max')
        )
        self.search.set_rooms(
            mini=params.get('rooms_min'), maxi=params.get('rooms_max')
        )
        self.search.set_square(
            mini=params.get('square_min'), maxi=params.get('square_max')
        )

        if 'keywords' in params:
            self.search.set_query(
                params['keywords'], titleonly=params.get('title_only', False)
            )

        if 'order_by' in params:
            try:
                by, order = params['order_by'].split('_')
            except ValueError:
                raise InvalidParameters('Invalid sort order.')
            if by not in ['time', 'price'] or order not in ['asc', 'desc']:
                raise InvalidParameters('Invalid sort order.')
            self.search.set_sorting(by=by, order=order)

    def get_results(self) -> Generator:
        return self.search.iter_results()
