import feedparser
from lbc2rss.feed import generate_ads_feed


class TestFeed:
    def test_feed_title_is_returned(self) -> None:
        feed = generate_ads_feed('locations')
        parsed = feedparser.parse(feed)
        assert (
            parsed['feed']['title']
            == 'Recherche des offres "locations" sur Leboncoin'
        )

    def test_feed_link_is_returned(self) -> None:
        feed = generate_ads_feed('locations')
        parsed = feedparser.parse(feed)
        assert (
            parsed['feed']['link']
            == 'https://www.leboncoin.fr/annonces/offres/'
        )

    def test_feed_description_is_returned(self) -> None:
        feed = generate_ads_feed('locations')
        parsed = feedparser.parse(feed)
        assert (
            parsed['feed']['description']
            == 'Résultat de la recherche des offres "locations" sur Leboncoin'
        )
