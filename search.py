import operator
from collections import namedtuple
from enum import Enum

from models import NearEarthObject, OrbitPath
from datetime import datetime


class DateSearch(Enum):
    """
    Enum representing supported date search on Near Earth Objects.
    """
    between = 'between'
    equals = 'equals'

    @staticmethod
    def list():
        """
        :return: list of string representations of DateSearchType enums
        """
        return list(map(lambda output: output.value, DateSearch))


class Query(object):
    """
    Object representing the desired search query operation to build. The Query
    uses the Selectors to structure the query information into a format the
    NEOSearcher can use for date search.
    """
    no = "number"
    ro = "return_object"
    Selectors = namedtuple('Selectors', ['date_search', no, 'filters', ro])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **kwargs):
        """
        :param kwargs: dict of search query parameters to determine which
        SearchOperation query to use
        """
        self.query_dict = kwargs
        self.selection = None

    def build_query(self):
        """
        Transforms the provided query options, set upon initialization, into a
        set of Selectors that the NEOSearcher can use to perform the
        appropriate search functionality

        :return: QueryBuild.Selectors namedtuple that translates the dict of
                 query options into a SearchOperation
        """

        # TODO: Translate the query parameters into a QueryBuild.Selectors
        # object
        Selectors = namedtuple('Selectors', ['date_search', 'number', 'filters', 'return_object'])
        DateSearch = namedtuple('DateSearch', ['type', 'values'])
        if "start_date" in self.query_dict and self.query_dict["start_date"] is not None:
            dates = DateSearch("between", [datetime.strptime(self.query_dict["start_date"], "%Y-%m-%d"), datetime.strptime(self.query_dict["end_date"], "%Y-%m-%d")])
        else:
            dates = DateSearch("equals", datetime.strptime(self.query_dict["date"], "%Y-%m-%d"))
        if 'filter' in self.query_dict:    
            filters = Filter.create_filter_options(self.query_dict['filter'])
        else:
            filters = {"Path" : []}
        self.selection = Selectors(dates, self.query_dict["number"], filters, self.query_dict["return_object"])

        return self.selection


class Filter(object):
    """
    Object representing optional filter options to be used in the date search
    for Near Earth Objects. Each filter is one of Filter.Operators provided
    with a field to filter on a value.
    """
    Options = {"is_hazardous": "hazard", "diameter": "size", "distance": "distance"}

    Operators = {">=": operator.ge, "<=": operator.le, "=": operator.eq}

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param field:  str representing object to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """
        self.field = field
        self.object = object
        self.operation = operation
        self.value = value

    @staticmethod
    def create_filter_options(filter_options):
        """
        Class function that transforms filter options raw input into filters

        :param input: list in format ["filter_option:operation:value_of_option", ...]
        :return: defaultdict with key of NearEarthObject or OrbitPath and
        value of empty list or list of Filters
        """
        list_of_filters = []
        if filter_options is None:
            return {"Path": []}
        for val in filter_options:
            filter_list = val.split(":")
            list_of_filters.append(Filter(filter_list[0], "NEO", filter_list[1], filter_list[2]))
        return {"Path": list_of_filters}

    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        if (len(results) == 0):
            return []
        Options = {"is_hazardous": "hazard", "diameter": "diameter_min_km", "distance": "distance"}
        Operators = {">=": operator.ge, "<=": operator.le, "=": operator.eq, ">": operator.gt, "<": operator.lt}
        return_list = []
        self.field = Options[self.field]
        if self.value != "True" and self.value != "False":
            self.value = float(self.value)
        if(type(results[0]) == OrbitPath):
            for result in results:
                result_dict = result.return_dict()
                if Operators[str(self.operation)](result_dict[self.field], self.value):
                    return_list.append(result)
        else:
            for result in results:
                temp = result.get_orbit()
                temp_dict = temp.return_dict()
                if Operators[str(self.operation)](temp_dict[self.field], self.value):
                    return_list.append(result)
        return return_list


class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects exposed by a
    generic search interface get_objects, which, based on the query
    specifications, determines how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances and their
        OrbitPath instances
        """
        self.db = db
        self.li = []

    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the
        QueryBuilder (query) calls the appropriate instance search function,
        then applys any filters, with distance as the last filter.

        Once any filters provided are applied, return the number of requested
        objects in the query.return_object specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """
        x = self.db.return_dictionary()
        if(query.date_search.type == 'equals'):
            for val in x:
                orbit_path = x[val].return_orbit_equals(query.date_search.values)
                if orbit_path is not None:
                    self.li.append(orbit_path)
        else:
            for val in x:
                return_val = x[val].return_orbit_between(query.date_search.values[0], query.date_search.values[1])
                if return_val is not None:
                    if query.return_object == "NEO":
                        self.li.append(return_val)
                    else:
                        self.li.append(return_val.get_orbit)
        filter_list = query.filters["Path"]
        for fi in filter_list:
            self.li = fi.apply(self.li)
        if len(self.li) < query.number:
            return self.li
        return self.li[:query.number]
