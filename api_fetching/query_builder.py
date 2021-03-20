import logging

logger = logging.getLogger(__name__)


class QueryBuilder:
    """
    Query builder for wattsight API
    """
    def __init__(self):
        self.query = {}

    def add_area(self, area):
        """
        ISO names. Accepts only one, except if the exc (exchange) category is present, then it makes 2
        :param area:
        :return:
        """
        if ("category", "exc") in self.query.items() and "area" in self.query:
            self.query["area"] += "," + area
        else:
            self.query["area"] = area

    def add_category(self, category):
        """
        e.g. price (pri), intraday
        :param category:
        :return:
        """
        if "category" in self.query:
            self.query["category"] += "," + category
        else:
            self.query["category"] = category

    def set_data_type(self, data_type):
        """
        Pick "a" for actual, "f" for forecast, whatever
        :param data_type:
        :return:
        """
        self.query["data_type"] = data_type

    def set_custom_frequency(self, frequency):
        """
        Pick min15 for 15min, h for hour, whatever, but consider using the dedicated methods
        :return:
        """
        self.query["frequency"] = frequency

    def set_15_min_frequency(self):
        """
        Data updates every 15min
        :return:
        """
        self.set_custom_frequency("min15")

    def set_hourly_frequency(self):
        """
        Data updates every hour
        :return:
        """
        self.set_custom_frequency("h")

    def set_volume_weighted_average_price(self, frequency=""):
        """
        VWAP, only works for price. If the frequency is not specified, the value is for the whole trading life cycle.
        Possible values for frequency: id1 (within the last hour), id3 (3 hours), id30min (30min)
        :return:
        """
        if "pri" not in self.query["category"]:
            logger.warning("Cannot set VWAP for a query that's not a price")
            return
        self.add_category("vwap")
        if frequency is not "":
            self.add_category(frequency)

    def get_query(self):
        final_query = self.query.copy()
        self.query = {}
        return final_query
