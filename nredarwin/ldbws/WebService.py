from nredarwin.ldbws.ServiceDetails import ServiceDetails
from nredarwin.ldbws.StationBoard import StationBoard

from functools import partial
from suds.client import Client
from suds.sax.element import Element
from suds import WebFault

import logging
import os

log = logging.getLogger(__name__)
#TODO - timeouts and error handling
DARWIN_WEBSERVICE_NAMESPACE = ('com','http://thalesgroup.com/RTTI/2010-11-01/ldb/commontypes')

class DarwinLdbSession(object):
    """
    A connection to the Darwin LDB web service
    """

    def __init__(self, wsdl=None, api_key=None, timeout=5):
        """
        Constructor

        Keyword arguments:
        wsdl -- the URL of the Darwin LDB WSDL document. Will fall back to using the DARWIN_WEBSERVICE_WSDL environment variable if not supplied
        api_key -- a valid API key for the Darwin LDB webservice. Will fall back to the DARWIN_WEBSERVICE_API_KEY if not supplied
        timeout -- a timeout in seconds for calls to the LDB Webservice (default 5)
        """
        if not wsdl:
            wsdl = os.environ['DARWIN_WEBSERVICE_WSDL']
        if not api_key:
            api_key = os.environ['DARWIN_WEBSERVICE_API_KEY']
        self._soap_client = Client(wsdl)
        self._soap_client.set_options(timeout=timeout)
        #build soap headers
        token3 = Element('AccessToken', ns=DARWIN_WEBSERVICE_NAMESPACE)
        token_value = Element('TokenValue', ns=DARWIN_WEBSERVICE_NAMESPACE)
        token_value.setText(api_key)
        token3.append(token_value)
        self._soap_client.set_options(soapheaders=(token3))

    def _base_query(self):
        return self._soap_client.service['LDBServiceSoap']

    def get_station_board(self, crs, rows=10, include_departures=True, include_arrivals=False, destination_crs=None, origin_crs=None):
        """
        Query the darwin webservice to obtain a board for a particular station and return a StationBoard instance

        Positional arguments:
        crs -- the three letter CRS code of a UK station

        Keyword arguments:
        rows -- the number of rows to retrieve (default 10)
        include_departures -- include departing services in the departure board (default True)
        include_arrivals -- include arriving services in the departure board (default False)
        destination_crs -- filter results so they only include services calling at a particular destination (default None)
        origin_crs -- filter results so they only include services originating from a particular station (default None)
        """
        #Determine the darwn query we want to make
        if include_departures and include_arrivals:
            query_type = 'GetArrivalDepartureBoard'
        elif include_departures:
            query_type = 'GetDepartureBoard'
        elif include_arrivals:
            query_type = 'GetArrivalBoard'
        else:
            raise ValueError("get_station_board must have either include_departures or include_arrivals set to True")
        #build a query function
        q = partial(self._base_query()[query_type], crs=crs, numRows=rows)
        if destination_crs:
            if origin_crs:
                log.warn("Station board query can only filter on one of destination_crs and origin_crs, using only destination_crs")
            q = partial(q, filterCrs=destination_crs, filterType='to')
        elif origin_crs:
            q = partial(q, filterCrs=origin_crs, filterType='from')
        try:
            soap_response = q()
        except WebFault:
            raise WebServiceError
        return StationBoard(soap_response)

    def get_service_details(self, service_id):
        """
        Get the details of an individual service and return a ServiceDetails instance.

        Positional arguments:
        service_id: A Darwin LDB service id
        """
        try:
            soap_response = self._soap_client.service['LDBServiceSoap']['GetServiceDetails'](serviceID=service_id)
        except WebFault:
            raise WebServiceError
        return ServiceDetails(soap_response)


class WebServiceError(Exception):
    pass


