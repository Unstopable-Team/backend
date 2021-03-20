import logging
from datetime import datetime

import wapi

from api_fetching.query_builder import QueryBuilder

logger = logging.getLogger(__name__)


class WattsightSession:
    def __init__(self, client_id, client_secret):
        self.session = wapi.Session(client_id=client_id, client_secret=client_secret)

    def get_data(self, query: dict, data_from=None, data_to=None):
        """
        Real APIs have curves, man! Use the query to search a specific data curve using the query.
        :param data_from: timestamp in ms, starting date of the data to be returned
        :param data_to: timestamp in ms, end date of the data to be returned
        :param query:
        :return:
        """
        curves = self.session.search(**query)
        logging.info("Found {} curves. Returning the data for the first one.".format(len(curves)))

        if data_from is not None:
            data_from = datetime.fromtimestamp(data_from // 1000)

        if data_to is not None:
            data_to = datetime.fromtimestamp(data_to // 1000)

        if curves[0].curve_type == "INSTANCES":
            time_series = curves[0].get_latest()
            if time_series is not None:
                return time_series.to_pandas()
        elif curves[0].curve_type == "TIME_SERIES":
            return curves[0].get_data(data_from=data_from, data_to=data_to).to_pandas()

        raise ValueError("No curve found")


if __name__ == '__main__':
    query = QueryBuilder()
    query.add_category("pri")
    query.add_category("intraday")
    query.add_area("de")
    query.set_data_type("a")
    query.set_15_min_frequency()
    query.set_volume_weighted_average_price("id1")

