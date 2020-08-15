import feedparser
from lbc2rss.feed import format_item, generate_ads_feed

from .utils import FORMATTED_ITEM, SearchResult, get_results


class TestFeed:
    def test_feed_title_is_returned(self) -> None:
        feed = generate_ads_feed('locations', get_results([]), {})
        parsed = feedparser.parse(feed)
        assert (
            parsed['feed']['title']
            == 'Recherche des offres "locations" sur Leboncoin'
        )

    def test_feed_link_is_returned(self) -> None:
        feed = generate_ads_feed('locations', get_results([]), {})
        parsed = feedparser.parse(feed)
        assert (
            parsed['feed']['link']
            == 'https://www.leboncoin.fr/annonces/offres/'
        )

    def test_feed_description_is_returned(self) -> None:
        feed = generate_ads_feed('locations', get_results([]), {})
        parsed = feedparser.parse(feed)
        assert (
            parsed['feed']['description']
            == 'Résultat de la recherche des offres "locations" sur Leboncoin'
        )

    def test_feed_description_with_params_is_returned(self) -> None:
        feed = generate_ads_feed(
            'locations', get_results([]), {"cities": "Lyon|69000"}
        )
        parsed = feedparser.parse(feed)
        assert parsed['feed']['description'] == (
            'Résultat de la recherche des offres "locations" sur Leboncoin'
            ', paramètres : {\'cities\': \'Lyon|69000\'}'
        )

    def test_feed_with_entry_is_returned(self) -> None:
        feed = generate_ads_feed(
            'locations',
            get_results([SearchResult()]),
            {"cities": "Lyon|69000"},
        )
        parsed = feedparser.parse(feed)
        assert len(parsed.entries) == 1


class TestFormatItem:
    def test_it_formats_item(self) -> None:
        item = SearchResult()
        formatted_item = format_item(item)
        assert formatted_item == FORMATTED_ITEM


class TestFormatFeedItem:
    def test_feed_entry_link_is_ad_url(self) -> None:
        ad_result = SearchResult()
        feed = generate_ads_feed('locations', get_results([ad_result]), {})
        parsed = feedparser.parse(feed)
        entry = parsed.entries[0]
        assert entry.link == ad_result.url

    def test_feed_entry_title_is_ad_title(self) -> None:
        ad_result = SearchResult()
        feed = generate_ads_feed('locations', get_results([ad_result]), {})
        parsed = feedparser.parse(feed)
        entry = parsed.entries[0]
        assert entry.title == (
            f'{ad_result.real_estate_type.capitalize()} - {ad_result.title} - '
            f'{ad_result.price} €'
        )

    def test_feed_entry_date_is_ad_publication_date(self) -> None:
        ad_result = SearchResult()
        feed = generate_ads_feed('locations', get_results([ad_result]), {})
        parsed = feedparser.parse(feed)
        entry = parsed.entries[0]
        assert (
            ad_result.publication_date.strftime('%a, %d %b %Y %H:%M:%S')
            in entry.updated
        )

    def test_feed_entry_summary_is_formatted_ad(self) -> None:
        ad_result = SearchResult()
        feed = generate_ads_feed('locations', get_results([ad_result]), {})
        parsed = feedparser.parse(feed)
        entry = parsed.entries[0]
        assert entry.summary == FORMATTED_ITEM
