from QueryBuilder import QueryBuilder
import wapi


class WattsightSession:
    def __init__(self, client_id, client_secret):
        self.session = wapi.Session(client_id=client_id, client_secret=client_secret)
        self.cat = self.session.get_categories()

    def get_data(self, query: dict):
        curves = self.session.search(**query)
        print("shit")


query = QueryBuilder()
query.add_category("pri")
query.add_category("intraday")
query.add_area("de")

WattsightSession("AbwDO8o884sQ692GrvHfXZAV5WA5UrS4", "e0RQR6gXOK.7uL6n3ybNJzYiMWOhHv8AkfNoZzqyXK9ZdgEk4_hIXbICFkrauNN_yB1HF-afjOk4Oci7nT._TD8WeHLwiDYDqd5s").get_data(query.get_query())
