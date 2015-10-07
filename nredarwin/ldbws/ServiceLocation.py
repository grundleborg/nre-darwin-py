from nredarwin.ldbws.SoapResponseBase import SoapResponseBase

import logging

log = logging.getLogger(__name__)

class ServiceLocation(SoapResponseBase):
    """
    A single location from a service origin/destination list
    """
    field_mapping = [
        ('location_name', 'locationName'),
        ('crs', 'crs'),
        ('via', 'via'),
        ('future_change_to', 'futureChangeTo'),
        ('association_is_cancelled', 'assocIsCancelled'),
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
        The CRS code of the location
        """
        return self._crs

    @property
    def via(self):
        """
        An optional string that should be displayed alongside the location_name. This provides additional context regarding an ambiguous route.
        """
        return self._via

    @property
    def future_change_to(self):
        """
        An optional string that indicates a service type (Bus/Ferry/Train) which will replace the current service type in the future.
        """
        return self._future_change_to

    @property
    def association_is_cancelled(self):
        """
        This origin or destination can no longer be reached because the association has been cancelled.
        """
        return self._association_is_cancelled
    
    def __str__(self):
        if self.via:
            return "%s %s" % (self.location_name, self.via)
        else:
            return self.location_name


