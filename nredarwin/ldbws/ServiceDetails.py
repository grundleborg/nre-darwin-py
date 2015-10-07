from nredarwin.ldbws.ServiceDetailsBase import ServiceDetailsBase
from nredarwin.ldbws.CallingPoints import CallingPointList

import logging

log = logging.getLogger(__name__)

class ServiceDetails(ServiceDetailsBase):
    """
    In depth details of a single service
    """

    field_mapping = ServiceDetailsBase.field_mapping + [
        ('is_cancelled', 'isCancelled'),
        ('disruption_reason', 'disruptionReason'),
        ('overdue_message', 'overdueMessage'),
        ('ata', 'ata'),
        ('atd', 'atd'),
        ('location_name', 'locationName'),
        ('crs', 'crs'),
        ('generated_at', 'generatedAt'),
    ]
   
    def __init__(self, soap_data, *args, **kwargs):
        super(ServiceDetails, self).__init__(soap_data, *args, **kwargs)
        self._previous_calling_point_lists = self._calling_point_lists(soap_data, 'previousCallingPoints')
        self._subsequent_calling_point_lists = self._calling_point_lists(soap_data, 'subsequentCallingPoints')

    def _calling_point_lists(self, soap_data, src_key):
        try:
            calling_points = getattr(getattr(soap_data, src_key), 'callingPointList')
        except AttributeError:
            return []
        lists = []
        for sublist in calling_points:
            lists.append(CallingPointList(sublist))
        return lists

    @property
    def is_cancelled(self):
        """
        True if this service is cancelled at this location.
        """
        return self._is_cancelled

    @property
    def disruption_reason(self):
        """
        A string containing a disruption reason for this service, if it is delayed or cancelled.
        """
        return self._disruption_reason

    @property
    def overdue_message(self):
        """
        A string that describes an overdue event
        """
        return self._overdue_message

    @property
    def ata(self):
        """
        Actual Time of Arrival.

        A human readable string, not guaranteed to be a machine-parsable time
        """
        return self._ata

    @property
    def atd(self):
        """
        Actual Time of Departure.

        A human readable string, not guaranteed to be a machine-parsable time
        """
        return self._atd

    @property
    def location_name(self):
        """
        Location Name

        The name of the location from which the details of this service are being accessed
        and to which the service attributes such as times correspond.
        """
        return self._location_name

    @property
    def crs(self):
        """
        The CRS code corresponding to the location_name property.
        """
        return self._crs

    @property
    def generated_at(self):
        """
        The time at which the service details were generated. 
        """
        return self._generated_at

    @property
    def previous_calling_point_lists(self):
        """
        A list of CallingPointLists.

        The first CallingPointList is all the calling points of the through train from its origin up
        until immediately before here, with any additional CallingPointLIsts (if they are present)
        containing the calling points of associated trains which join the through train from their
        respective origins through to the calling point at which they join with the through train.
        """
        return self._previous_calling_point_lists

    @property
    def subsequent_calling_point_lists(self):
        """
        A list of CallingPointLists.

        The first CallingPointList is all the calling points of the through train after here until
        its destination, with any additional CallingPointLists (if they are present) containing the
        calling points of associated trains which split from the through train from the calling
        point at which they split off from the through train until their respective destinations.
        """
        return self._subsequent_calling_point_lists

    @property
    def previous_calling_points(self):
        """
        A list of CallingPoint objects.

        This is the list of all previous calling points for the service, including all associated
        services if multiple services join together to form this service.
        """
        return [cp for cpl in self._previous_calling_point_lists for cp in cpl.calling_points]

    @property
    def subsequent_calling_points(self):
        """
        A list of CallingPoint objects.

        This is the list of all subsequent calling points for the service, including all associated
        services if the service splits into multiple services.
        """
        return [cp for cpl in self._subsequent_calling_point_lists for cp in cpl.calling_points]


