from nredarwin.ldbws.ServiceDetailsBase import ServiceDetailsBase
from nredarwin.ldbws.ServiceLocation import ServiceLocation

import logging

log = logging.getLogger(__name__)

class ServiceItem(ServiceDetailsBase):
    """
    A single service from a bus, train or ferry departure/arrival board
    """

    field_mapping = ServiceDetailsBase.field_mapping + [
        ('is_circular_route', 'isCircularRoute'),
        ('service_id', 'serviceID'),
    ]
    
    def __init__(self, soap_data, *args, **kwargs):
        super(ServiceItem, self).__init__(soap_data, *args, **kwargs)

        #handle service location lists - these should be empty lists if there are no locations
        self._origins = [ServiceLocation(l) for l  in soap_data.origin.location] if hasattr(soap_data.origin, 'location') else []
        self._destinations = [ServiceLocation(l) for l  in soap_data.destination.location] if hasattr(soap_data.origin, 'location') else []

    @property
    def is_circular_route(self):
        """
        If True this service is following a circular route and will call again at this station.
        """
        return self._is_circular_route

    @property
    def service_id(self):
        """
        The unique ID of this service. This ID is specific to the Darwin LDB Service
        """
        return self._service_id

    @property
    def origins(self):
        """
        A list of ServiceLocation objects describing the origins of this service. A service may have more than multiple origins.
        """
        return self._origins

    @property
    def destinations(self):
        """
        A list of ServiceLocation objects describing the destinations of this service. A service may have more than multiple destinations.
        """
        return self._destinations

    @property
    def destination_text(self):
        """
        Human readable string describing the destination(s) of this service
        """
        return self._location_formatter(self.destinations)

    @property
    def origin_text(self):
        """
        Human readable string describing the origin(s) of this service
        """
        return self._location_formatter(self.origins)

    def _location_formatter(self, location_list):
        return ", ".join([str(l) for l in location_list])

    def __str__(self):
        return "Service %s" % (self.service_id)


