from feedgenerator import Rss201rev2Feed


def generate_ads_feed(category: str) -> str:
    feed = Rss201rev2Feed(
        title=f'Recherche des offres "{category}" sur Leboncoin',
        link='https://www.leboncoin.fr/annonces/offres/',
        description=(
            f'Résultat de la recherche des offres "{category}" sur Leboncoin'
        ),
        language='fr',
    )

    return feed.writeString('UTF-8')
