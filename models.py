from datetime import datetime
from copy import deepcopy


class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object,
        only a subset of attributes used
        """
        edmink = "estimated_diameter_min_kilometers"
        edmaxk = "estimated_diameter_max_kilometers"
        cd = "close_approach_date"
        mns = "diameter_min_km"
        mxs = "diameter_max_km"
        self.neo_dict = {}
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.diameter_max_km = float(kwargs[edmink])
        self.diameter_min_km = float(kwargs[edmaxk])
        self.size = (self.diameter_max_km+self.diameter_min_km)/2
        self.is_potentially_hazardous_asteroid = kwargs["is_potentially_hazardous_asteroid"]
        self.close_approach_dates = []
        self.close_approach_dates.append(datetime.strptime(kwargs[cd], "%Y-%m-%d"))
        self.orbits = []
        orbit = OrbitPath(**kwargs)
        self.orbits.append(orbit)

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """
        self.close_approach_dates.append(orbit.return_date())
        self.orbits.append(orbit)

    def __repr__(self):
        str = f'Name :{self.name} \n'
        str += f'ID :{self.id} \n'
        str += "Dates and paths are as following : \n"
        for orb in self.orbits:
            str += orb.data()
            str += "\n"
        return str

    def data(self):
        str = f'Name :{self.name}'
        str += f' ID :{self.id}'
        str += " Dates and paths are as following :"
        for orb in self.orbits:
            str += orb.data()
            str += "||"
        return str

    def dates(self):
        """
        return: the function returns list of dates at which NEO object
                visited earth
        """
        return self.close_approach_dates

    def return_orbit_equals(self, date):
        """
              Looks for NEO on a given date
        parameter : date parameter defines the date at which NEO is to be
                    searched
        returns : NEO object if NEO visited around that date

        """
        for val in self.orbits:
            if val.return_date() == date:
                temp = self
                temp.neo_dict["date"] = val.return_date()
                temp.neo_dict["path"] = [val]
                return temp
        return None

    def return_orbit_between(self, date_one, date_two):
        """
            Looks for NEO between two dates
        parameters : two dates between which NEO is to be found
        return : returns NEO object if found, else None.
        """
        for val in self.orbits:
            if val.return_date() > date_one and val.return_date() < date_two:
                temp = deepcopy(self)
                temp.neo_dict["date"] = val.return_date()
                temp.neo_dict["path"] = [val]
                return temp
        return None

    def get_orbit(self):
        """
        returns the orbit of NEO with single orbit.
        """
        return self.orbits[0]

    def display_dict(self):
        self.neo_dict["id"] = self.id
        self.neo_dict["name"] = self.name
        self.neo_dict["diameter_max_km"] = self.diameter_max_km
        self.neo_dict["diameter_min_km"] = self.diameter_min_km
        self.neo_dict["size"] = self.size
        self.neo_dict["hazard"] = self.is_potentially_hazardous_asteroid
        self.neo_dict["date"] = self.close_approach_dates
        self.neo_dict["path"] = self.orbits
        temp_dict = deepcopy(self.neo_dict)
        path = self.get_orbit()
        temp_dict_two = path.display_dict()
        del temp_dict["path"]
        return_dict = {**temp_dict, **temp_dict_two}
        return return_dict


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a
        subset of attributes used
        """
        edmaxk = "estimated_diameter_max_kilometers"
        edmink = "estimated_diameter_min_kilometers"
        cd = "close_approach_date"
        mns = "diameter_min_km"
        mxs = "diameter_max_km"
        self.orbit_dict = {}
        self.close_approach_date = datetime.strptime(kwargs[cd], "%Y-%m-%d")
        self.diameter_max_km = float(kwargs[edmink])
        self.diameter_min_km = float(kwargs[edmaxk])
        self.size = (self.diameter_min_km+self.diameter_max_km)/2
        self.speed = kwargs["kilometers_per_hour"]
        self.is_potentially_hazardous_asteroid = kwargs["is_potentially_hazardous_asteroid"]
        self.miss_distance_kilometers = float(kwargs["miss_distance_kilometers"])
        self.neo_name = kwargs["name"]

    def __repr__(self):
        """
            returns string representation form of OrbitPath object.
        """
        str = f'Name :{self.neo_name} ||'
        str += f' Date :{self.close_approach_date} ||'
        str += f' Size :{self.size} ||'
        str += f' Miss Distance :{self.miss_distance_kilometers} ||'
        str += f' Is hazardous : {self.is_potentially_hazardous_asteroid}'
        return str

    def data(self):
        str = f'Date :{self.close_approach_date} ||'
        str += f' Size(in KM) :{self.size} ||'
        str += f' Miss Distance(in KM) :{self.miss_distance_kilometers} ||'
        str += f' Is hazardous : {self.is_potentially_hazardous_asteroid}'
        return str

    def return_date(self):
        return self.close_approach_date

    def return_dict(self):
        self.orbit_dict["diameter_max_km"] = self.diameter_max_km
        self.orbit_dict["diameter_min_km"] = self.diameter_min_km
        self.orbit_dict["hazard"] = self.is_potentially_hazardous_asteroid
        self.orbit_dict["size"] = self.size
        self.orbit_dict["date"] = self.close_approach_date
        self.orbit_dict["speed"] = self.speed
        self.orbit_dict["distance"] = self.miss_distance_kilometers
        self.orbit_dict["name"] = self.neo_name
        return self.orbit_dict

    def display_dict(self):
        self.orbit_dict["diameter_max_km"] = self.diameter_max_km
        self.orbit_dict["diameter_min_km"] = self.diameter_min_km
        self.orbit_dict["hazard"] = self.is_potentially_hazardous_asteroid
        self.orbit_dict["size"] = self.size
        self.orbit_dict["date"] = self.close_approach_date
        self.orbit_dict["speed"] = self.speed
        self.orbit_dict["distance"] = self.miss_distance_kilometers
        self.orbit_dict["name"] = self.neo_name
        return self.orbit_dict
