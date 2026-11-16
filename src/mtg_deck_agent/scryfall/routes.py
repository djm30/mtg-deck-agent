from enum import StrEnum


class Route(StrEnum):
    SEARCH = "/cards/search"
    NAMED = "/cards/named"
    RANDOM = "/cards/random"
    COLLECTION = "/cards/collection"
    CARD_BY_ID = "/cards/{id}"
    SETS = "/sets"


# Scryfall's 2/s endpoints
SLOW_ROUTES = (Route.SEARCH, Route.NAMED, Route.RANDOM, Route.COLLECTION)
