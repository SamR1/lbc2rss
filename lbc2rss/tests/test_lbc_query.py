from typing import Dict, List
from uuid import uuid4

import pytest
from lbc2rss.exceptions import InvalidParameters
from lbc2rss.lbc import LBCQuery
from pylbc.exceptions import InvalidCategory


class TestLBCQueryParameters:
    def test_it_raises_error_with_invalid_category(self) -> None:
        with pytest.raises(InvalidCategory):
            LBCQuery(category=uuid4().hex)

    def test_it_raises_error_with_invalid_real_estate_type(self) -> None:
        query = LBCQuery(category='locations')
        with pytest.raises(
            InvalidParameters, match='Invalid real estate types.'
        ):
            query.add_search_parameters(params={'types': uuid4().hex})

    @pytest.mark.parametrize(
        'coordinate,expected_coordinate',
        [('lon', 'longitude'), ('lat', 'latitude')],
    )
    def test_it_raises_error_if_a_coordinate_is_missing(
        self, coordinate: str, expected_coordinate: str
    ) -> None:
        query = LBCQuery(category='locations')
        with pytest.raises(
            InvalidParameters,
            match=f'Missing coordinate, get only {expected_coordinate}.',
        ):
            query.add_search_parameters(params={coordinate: 1})

    @pytest.mark.parametrize(
        'input_coordinates, expected_area_filter',
        [
            ({'lat': 45, 'lon': 4}, {'lat': 45.0, 'lng': 4.0, 'radius': 0},),
            (
                {'lat': '45', 'lon': '4'},
                {'lat': 45.0, 'lng': 4.0, 'radius': 0},
            ),
            (
                {'lat': 45, 'lon': 4, 'radius': 10},
                {'lat': 45.0, 'lng': 4.0, 'radius': 10000},
            ),
            (
                {'lat': '45', 'lon': '4', 'radius': '10'},
                {'lat': 45.0, 'lng': 4.0, 'radius': 10000},
            ),
        ],
    )
    def test_it_sets_coordinates_filters(
        self, input_coordinates: Dict, expected_area_filter: Dict
    ) -> None:
        query = LBCQuery(category='locations')
        query.add_search_parameters(params=input_coordinates)
        filters = query.search.get_filters()['filters']
        assert filters['location']['area'] == expected_area_filter

    @pytest.mark.parametrize(
        'cities',
        [
            'Lyon',
            'Lyon|Paris',
            '69000',
            'Lyon,69000,',
            'Lyon,6900,',
            'Lyon,69000|Paris',
            '|',
        ],
    )
    def test_it_raises_error_if_city_is_incorrect(self, cities: str) -> None:
        query = LBCQuery(category='locations')
        with pytest.raises(
            InvalidParameters,
            match=(
                r'A city must contain a name and a valid zip code \(5 digits\)'
                r', separated with a comma.'
            ),
        ):
            query.add_search_parameters(params={'cities': cities})

    @pytest.mark.parametrize(
        'cities,expected_cities_filters',
        [
            (
                'Lyon,69000',
                [{'city': 'Lyon', 'locationType': 'city', 'zipcode': '69000'}],
            ),
            (
                'Lyon,69000|L\'Arbresle,69210',
                [
                    {
                        'city': 'Lyon',
                        'locationType': 'city',
                        'zipcode': '69000',
                    },
                    {
                        'city': 'L\'Arbresle',
                        'locationType': 'city',
                        'zipcode': '69210',
                    },
                ],
            ),
        ],
    )
    def test_it_sets_cities_filters(
        self, cities: str, expected_cities_filters: List
    ) -> None:
        query = LBCQuery(category='locations')
        query.add_search_parameters(params={'cities': cities})
        filters = query.search.get_filters()['filters']
        assert filters['location']['locations'] == expected_cities_filters

    @pytest.mark.parametrize(
        'departments,expected_departments_filters',
        [
            ('69', [{'department_id': '69', 'locationType': 'department'}]),
            (
                '69|01',
                [
                    {'department_id': '69', 'locationType': 'department'},
                    {'department_id': '01', 'locationType': 'department'},
                ],
            ),
        ],
    )
    def test_it_sets_departments_filters(
        self, departments: str, expected_departments_filters: List
    ) -> None:
        query = LBCQuery(category='locations')
        query.add_search_parameters(params={'departments': departments})
        filters = query.search.get_filters()['filters']
        assert filters['location']['departments'] == departments.split('|')
        assert filters['location']['locations'] == expected_departments_filters

    @pytest.mark.parametrize(
        'input_price_params,expected_prices_filters',
        [
            ({'price_min': 200}, {'min': 200}),
            ({'price_max': 700}, {'min': 0, 'max': 700}),
            ({'price_min': 200, 'price_max': 700}, {'min': 200, 'max': 700}),
        ],
    )
    def test_it_sets_price_filters(
        self, input_price_params: Dict, expected_prices_filters: Dict
    ) -> None:
        query = LBCQuery(category='locations')
        query.add_search_parameters(params=input_price_params)
        filters = query.search.get_filters()['filters']
        assert filters['ranges']['price'] == expected_prices_filters

    @pytest.mark.parametrize(
        'input_rooms_params,expected_rooms_filters',
        [
            ({'rooms_min': 2}, {'min': 2}),
            ({'rooms_max': 3}, {'min': 0, 'max': 3}),
            ({'rooms_min': 2, 'rooms_max': 3}, {'min': 2, 'max': 3}),
        ],
    )
    def test_it_sets_rooms_filters(
        self, input_rooms_params: Dict, expected_rooms_filters: Dict
    ) -> None:
        query = LBCQuery(category='locations')
        query.add_search_parameters(params=input_rooms_params)
        filters = query.search.get_filters()['filters']
        assert filters['ranges']['rooms'] == expected_rooms_filters

    @pytest.mark.parametrize(
        'input_square_params,expected_square_filters',
        [
            ({'square_min': 40}, {'min': 40}),
            ({'square_max': 100}, {'min': 0, 'max': 100}),
            ({'square_min': 40, 'square_max': 100}, {'min': 40, 'max': 100}),
        ],
    )
    def test_it_sets_square_filters(
        self, input_square_params: Dict, expected_square_filters: Dict
    ) -> None:
        query = LBCQuery(category='locations')
        query.add_search_parameters(params=input_square_params)
        filters = query.search.get_filters()['filters']
        assert filters['ranges']['square'] == expected_square_filters

    @pytest.mark.parametrize(
        'input_keywords_params,expected_keywords_filters',
        [
            ({'keywords': 'terrasse'}, {'text': 'terrasse', 'type': 'all'}),
            (
                {'keywords': 'terrasse', 'title_only': True},
                {'text': 'terrasse', 'type': 'subject'},
            ),
        ],
    )
    def test_it_sets_keywords_filters(
        self, input_keywords_params: Dict, expected_keywords_filters: Dict
    ) -> None:
        query = LBCQuery(category='locations')
        query.add_search_parameters(params=input_keywords_params)
        filters = query.search.get_filters()['filters']
        assert filters['keywords'] == expected_keywords_filters

    @pytest.mark.parametrize(
        'sort', ['time', 'asc_time', 'time_as'],
    )
    def test_it_raises_error_if_sort_is_incorrect(self, sort: str) -> None:
        query = LBCQuery(category='locations')
        with pytest.raises(
            InvalidParameters, match='Invalid sort order.',
        ):
            query.add_search_parameters(params={'order_by': sort})

    @pytest.mark.parametrize(
        'input_sort_params,expected_sort_filters',
        [
            (
                {'order_by': 'time_desc'},
                {'sort_by': 'time', 'sort_order': 'desc'},
            ),
            (
                {'order_by': 'price_asc'},
                {'sort_by': 'price', 'sort_order': 'asc'},
            ),
        ],
    )
    def test_it_sets_sort_options(
        self, input_sort_params: Dict, expected_sort_filters: Dict
    ) -> None:
        query = LBCQuery(category='locations')
        query.add_search_parameters(params=input_sort_params)
        filters = query.search.get_filters()
        assert filters['sort_by'] == expected_sort_filters['sort_by']
        assert filters['sort_order'] == expected_sort_filters['sort_order']
