from nredarwin.ldbws.ServiceItem import ServiceItem
from nredarwin.ldbws.SoapResponseBase import SoapResponseBase

import logging

log = logging.getLogger(__name__)

class StationBoard(SoapResponseBase):
    """
    An abstract representation of a station departure board
    """

    field_mapping = [
        ('generated_at', 'generatedAt'),
        ('crs', 'crs'),
        ('location_name', 'locationName'),
        ('filter_location_name', 'filterLocationName'),
        ('filter_crs', 'filterCrs'),
        ('filter_type', 'filterType'),
        ('platform_available', 'platformAvailable'),
        ('are_services_available', 'areServicesAvailable'),
    ]

    service_lists = [
        ('train_services', 'trainServices'),
        ('bus_services', 'busServices'),
        ('ferry_services', 'ferryServices')
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(StationBoard,self).__init__(soap_response, *args, **kwargs)
        #populate service lists - these are specific to station board objects, so not included in base class
        for dest_key, src_key in self.__class__.service_lists:
            try:
                service_rows = getattr(getattr(soap_response, src_key), 'service')
            except AttributeError:
                setattr(self, '_' + dest_key, [])
                continue

            setattr(self, '_' + dest_key, [ServiceItem(s) for s  in service_rows])
        #populate nrcc_messages
        if hasattr(soap_response, 'nrccMessages') and hasattr(soap_response.nrccMessages, 'message'):
            #TODO - would be nice to strip HTML from these, especially as it's not compliant with modern standards
            self._nrcc_messages = soap_response.nrccMessages.message
        else:
            self._nrcc_messages = []

    @property
    def generated_at(self):
        """
        The time at which the station board was generated. 
        """
        return self._generated_at

    @property
    def crs(self):
        """
        The CRS code for the station. 
        """
        return self._crs

    @property
    def location_name(self):
        """
        The name of the station.
        """
        return self._location_name

    @property
    def train_services(self):
        """
        A list of train services that appear on this board. Empty if there are none
        """
        return self._train_services

    @property
    def bus_services(self):
        """
        A list of bus services that appear on this board. Empty if there are none
        """
        return self._bus_services

    @property
    def ferry_services(self):
        """
        A list of ferry services that appear on this board. Empty if there are none
        """
        return self._ferry_services

    @property
    def nrcc_messages(self):
        """
        An optional list of important messages that should be displayed with the station board. Messages may include HTML hyperlinks and paragraphs.        """
        return self._nrcc_messages

    @property
    def filter_location_name(self):
        """
        If a filter was requested, the location name of the filter location.
        """
        return self._filter_location_name

    @property
    def filter_crs(self):
        """
        If a filter was requested, the CRS code of the filter location.
        """
        return self._filter_crs

    @property
    def filter_type(self):
        """
        If a filter was requested, the type of filter.
        """
        return self._filter_type

    @property
    def platform_available(self):
        """
        An optional value that indicates if platform information is available. If this value is
        present with the value "true" then platform information will be returned in the service
        lists. If this value is not present, or has the value "false", then the platform
        "heading" should be suppressed in the user interface for this station board.
        """
        return self._platform_available

    @property
    def are_services_available(self):
        """
        An optional value that indicates if services are currently available for this station
        board. If this value is present with the value "false" then no services will be
        returned in the service lists. This value may be set, for example, if access to a
        station has been closed to the public at short notice, even though the scheduled
        services are still running. It would be usual in such cases for one of the nrccMessages
        to describe why the list of services has been suppressed.
        """
        return self._are_services_available

    def __str__(self):
        return "%s - %s" % (self.crs, self.location_name)


