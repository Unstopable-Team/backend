import logging
from datetime import datetime, timedelta

import wapi
import multiprocessing

from api_fetching.query_builder import QueryBuilder

logger = logging.getLogger(__name__)


class WattsightSession:
    def __init__(self, client_id, client_secret, new_data_callback):
        self.session = wapi.Session(client_id=client_id, client_secret=client_secret)
        self.followed_curves = []
        self.is_running = True
        self.callback = new_data_callback
        self.event_processor: multiprocessing.Process = None

    def get_data(self, query: dict, data_from=None, data_to=None):
        """
        Real APIs have curves, man! Use the query to search a data curve using the query.
        :param data_from: timestamp in ms, starting date of the data to be returned
        :param data_to: timestamp in ms, end date of the data to be returned
        :param query:
        :return: the data and the name of the curve. In the case it's an instance curve, get the latest one
        """
        curves = self.session.search(**query)
        logging.info("Found {} curves. Returning the data for the first one.".format(len(curves)))

        if len(curves) == 0:
            logger.warning("Your query is flat (it has no curves). Check debug too see the actual query")
            logger.debug(query)
            return None

        return self.get_data_by_name(curves[0].name, data_from, data_to)

    def get_data_by_name(self, curve_name, data_from=None, data_to=None):
        """
        Get data from a curve using its name
        :param curve_name:
        :param data_from:
        :param data_to:
        :return: name and data as a pandas dataframe
        """
        curve = self.session.search(name=curve_name)[0]

        if data_from is not None:
            data_from = datetime.fromtimestamp(data_from // 1000)

        if data_to is not None:
            data_to = datetime.fromtimestamp(data_to // 1000)

        if curve.curve_type == "INSTANCES":
            time_series = curve.get_latest()
            if time_series is not None:
                return curve.name, time_series.to_pandas()
        elif curve.curve_type == "TIME_SERIES":
            return curve.name, curve.get_data(data_from=data_from, data_to=data_to).to_pandas()

        raise ValueError("No curve found")

    def add_curve_to_event_listener(self, query: dict = None, name=None):
        """
        Listens for events on the specified curve, identified by the query (or name). The first result of the search is used
        :param name:
        :param query:
        :return:
        """
        if query is not None:
            curves = self.session.search(**query)
        else:
            curves = self.session.search(name=name)

        if len(curves) == 0:
            logger.warning("Your query is flat (it has no curves). Check debug too see the actual query")
            logger.debug(query)
            return

        self.followed_curves.append(curves[0])

        if self.event_processor is None:
            self.event_processor = multiprocessing.Process(target=self.listen_to_curves)

        self.event_processor.terminate()
        self.event_processor.start()

    def listen_to_curves(self):
        events = self.session.events(self.followed_curves)

        for event in events:
            if not isinstance(event, wapi.events.CurveEvent):
                continue

            data_from = datetime.now() - timedelta(days=1)
            data = self.get_data_by_name(event.curve.name, data_from=data_from).tail(1)
            self.callback(event.curve.name, data)


if __name__ == '__main__':
    # query builder demo
    query = QueryBuilder()
    query.add_category("pri")
    query.add_category("intraday")
    query.add_area("de")
    query.set_data_type("a")
    query.set_15_min_frequency()
    query.set_volume_weighted_average_price("id1")
