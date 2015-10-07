from nredarwin.ldbws.SoapResponseBase import SoapResponseBase

import logging

log = logging.getLogger(__name__)

class ServiceDetailsBase(SoapResponseBase):
    #The generic stuff that both service details classes have
    field_mapping = [
        ('sta', 'sta'),
        ('eta', 'eta'),
        ('std', 'std'),
        ('etd', 'etd'),
        ('platform', 'platform'),
        ('operator_name', 'operator'),
        ('operator_code', 'operatorCode'),
    ]


    @property
    def scheduled_arrival(self):
        raise NotImplementedError()

    @property
    def estimated_arrival(self):
        raise NotImplementedError()
        
    @property
    def scheduled_departure(self):
        raise NotImplementedError()

    @property
    def estimated_departure(self):
        raise NotImplementedError()

    @property
    def sta(self):
        """
        Scheduled Time of Arrival. This is optional and may be present for station boards which include arrivals.

        This is a human readable string rather than a proper datetime object and may not be a time at all
        """
        return self._sta

    @property
    def eta(self):
        """
        Estimated Time of Arrival. This is optional and may be present when an sta (Scheduled Time of Arrival) is available.

        This is a human readable string rather than a proper datetime object and may not be a time at all
        """
        return self._eta

    @property
    def std(self):
        """
        Scheduled Time of Departure. This is optional and may be present for station boards which include departures

        This is a human readable string rather than a proper datetime object and may not be a time at all
        """
        return self._std

    @property
    def etd(self):
        """
        Estimated Time of Departure. This is optional and may be present for results which contain an std (Scheduled Time of Departure)

        This is a human readable string rather than a proper datetime object and may not be a time at all
        """
        return self._etd

    @property
    def platform(self):
        """
        The platform number for the service at this station. Optional.
        """
        return self._platform

    @property
    def operator_name(self):
        """
        The name of the train operator
        """
        return self._operator_name

    @property
    def operator_code(self):
        """
        The National Rail abbreviation for the train operator
        """
        return self._operator_code

    #TODO -Adhoc alerts, datetime inflators - if possible


