from nredarwin.ldbws.SoapResponseBase import SoapResponseBase

import logging

log = logging.getLogger(__name__)

class CallingPoint(SoapResponseBase):
    """A single calling point on a train route"""
    field_mapping = [
        ('location_name', 'locationName'),
        ('crs', 'crs'),
        ('et', 'et'),
        ('at', 'at'),
        ('st', 'st')
    ]

    @property
    def location_name(self):
        """
        Location name
        """
        return self._location_name

    @property
    def crs(self):
        """
        The CRS code for this location 
        """
        return self._crs

    @property
    def at(self):
        """
        Actual time

        Human readable string, no guaranteed format
        """
        return self._at

    @property
    def et(self):
        """
        Estimated time

        Human readable string, no guaranteed format
        """
        return self._et

    @property
    def st(self):
        """
        Scheduled time

        Human readable string, no guaranteed format
        """
        return self._st

class CallingPointList(SoapResponseBase):
    """ A list of calling points"""
    field_mapping = [
        ('service_type', '_serviceType'),
        ('service_change_required', '_serviceChangeRequired'),
        ('association_is_cancelled', '_assocIsCancelled'),
    ]

    def __init__(self, soap_data, *args, **kwargs):
        super(CallingPointList, self).__init__(soap_data, *args, **kwargs)
        self._calling_points = self._calling_point_list(soap_data, 'callingPoint')

    def _calling_point_list(self, soap_data, src_key):
        try:
            calling_points = getattr(soap_data, src_key)
        except AttributeError:
            return []
        calling_points_list = []
        for point in calling_points:
            calling_points_list.append(CallingPoint(point))
        return calling_points_list

    @property
    def calling_points(self):
        """
        List of CallingPoint objects

        All the calling points contained within this calling point list
        """
        return self._calling_points

    @property
    def service_type(self):
        """
        Service type

        The service type of the service with these calling points (e.g. "train")
        """
        return self._service_type

    @property
    def service_change_required(self):
        """
        Service change required

        A boolean indicating whether a change is required between the through service and the
        service to these calling points.
        """
        return self._service_change_required

    @property
    def association_is_cancelled(self):
        """
        Association is cancelled

        A boolean indicating whether this association is cancelled.
        """
        return self._association_is_cancelled


