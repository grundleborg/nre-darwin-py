import logging

log = logging.getLogger(__name__)

class SoapResponseBase(object):

    def __init__(self, soap_response):
        for dest_key, src_key in self.__class__.field_mapping:
            try:
                val = getattr(soap_response, src_key)
            except AttributeError:
                val = None
            setattr(self, '_' + dest_key, val)


