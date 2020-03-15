import csv
from models import OrbitPath, NearEarthObject


class NEODatabase(object):
    """
    Object to hold Near Earth Objects and their orbits.

    To support optimized date searching, a dict mapping of all orbit date
    paths to the Near Earth Objects recorded on a given day is maintained.
    Additionally, all unique instances of a Near Earth Object are contained in
    a dict mapping the Near Earth Object name to the NearEarthObject instance.
    """

    def __init__(self, filename):
        """
        :param filename: str representing the pathway of the filename
        containing the Near Earth Object data
        """
        # TODO: What data structures will be needed to store the
        # # NearEarthObjects and OrbitPaths?
        # TODO: Add relevant instance variables for this.
        self.filename = filename
        self.data_dictionary = {}

    def load_data(self, filename=None):
        """
        Loads data from a .csv file, instantiating Near Earth Objects and
        their OrbitPaths by:
           - Storing a dict of orbit date to list of NearEarthObject instances
           - Storing a dict of the Near Earth Object name to the single
            instance of NearEarthObject

        :param filename:
        :return:
        """

        if not (filename or self.filename):
            raise Exception('Cannot load data, no filename provided')

        filename = filename or self.filename

        # TODO: Load data from csv file.
        # TODO: Where will the data be stored?
        csvfile = open(self.filename, "r")
        obj = csv.DictReader(csvfile)
        for ob in obj:
            if ob["name"] in self.data_dictionary:
                temp_orb = OrbitPath(**ob)
                self.data_dictionary[ob["name"]].update_orbits(temp_orb)
            else:
                self.data_dictionary[ob["name"]] = NearEarthObject(**ob)

        return None

    def __repr__(self):
        str = ""
        for val in self.data_dictionary:
            str += self.data_dictionary[val].data()
            str += "\n"
        return str

    def return_dictionary(self):
        return self.data_dictionary
