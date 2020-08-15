from typing import Dict, Generator

from feedgenerator import Rss201rev2Feed
from pylbc import SearchResult

FEED_ITEM_TEMPLATE = """<blockquote>
    <p>
        <strong>Date</strong> : {ad.publication_date}<br />
        <strong>Prix</strong> : {ad.price} €
        (<em>{ad.price_per_square:.2f} €/m²</em>)
        <br />
        <strong>Type</strong> : {ad.real_estate_type}<br />
        <strong>Surface</strong> : {ad.square} m²<br />
        <br />
        <a href="{ad.url}" target="_blank">
            <img src="{ad.thumbnail}" alt="Photo de l'offre">
        </a>
    </p>
</blockquote>"""


def format_item(item: SearchResult) -> str:
    return FEED_ITEM_TEMPLATE.format(ad=item)


def format_feed_item(item: SearchResult, feed: Rss201rev2Feed) -> str:
    return feed.add_item(
        title=(
            f'{item.real_estate_type.capitalize()} - {item.title} - '
            f'{item.price} €'
        ),
        link=item.url,
        pubdate=item.publication_date,
        description=format_item(item),
    )


def generate_ads_feed(category: str, results: Generator, params: Dict) -> str:
    feed = Rss201rev2Feed(
        title=f'Recherche des offres "{category}" sur Leboncoin',
        link='https://www.leboncoin.fr/annonces/offres/',
        description=(
            f'Résultat de la recherche des offres "{category}" sur Leboncoin'
            f'{f", paramètres : {str(params)}" if params else ""}'
        ),
        language='fr',
    )

    for item in results:
        format_feed_item(item, feed)

    return feed.writeString('UTF-8')
